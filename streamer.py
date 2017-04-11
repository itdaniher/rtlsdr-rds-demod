# BSD 3 clause
# Authors: Ian Daniher <itdaniher@gmail.com>
import numpy as np

import fm

import multiprocessing
import asyncio
import time

import cbor
import blosc
import asyncio_redis
from asyncio_redis.encoders import BaseEncoder

class CborEncoder(BaseEncoder):
    native_type = object
    def encode_from_native(self, data):
        return cbor.dumps(data)
    def decode_to_native(self, data):
        return cbor.loads(data)

compress = lambda in_: (in_.size, in_.dtype, blosc.compress_ptr(in_.__array_interface__['data'][0], in_.size, in_.dtype.itemsize, clevel = 1, shuffle = blosc.BITSHUFFLE, cname = 'lz4'))

def decompress(size, dtype, data):
    out = np.empty(size, dtype)
    blosc.decompress_ptr(data, out.__array_interface__['data'][0])
    return out

def packed_bytes_to_iq(samples, out = None):
    if out is None:
        iq = np.empty(len(samples)//2, 'complex64')
    else:
        iq = out
    bytes_np = np.ctypeslib.as_array(samples)
    iq.real, iq.imag = bytes_np[::2], bytes_np[1::2]
    iq /= (255/2)
    iq -= (1 + 1j)
    if out is None:
        return iq

async def process_samples(sdr):
    connection = await asyncio_redis.Connection.create('localhost', 6379, encoder = CborEncoder())
    (block_size, max_blocks) = (1024*32, 127)
    samp_size = block_size // 2
    count = 0 
    last = time.time()
    block = []
    async for byte_samples in sdr.stream(block_size, format = 'bytes'):
        complex_samples = np.empty(samp_size, 'complex64')
        packed_bytes_to_iq(byte_samples, complex_samples)
        block.append(np.copy(complex_samples))
        count += 1
        if count > max_blocks:
            timestamp = time.time()
            block.append(np.copy(complex_samples))
            size, dtype, compressed = compress(np.concatenate(block))
            info = {'size': size, 'dtype': dtype.name, 'data': compressed}
            await connection.set(timestamp, info)
            await connection.lpush('timestamps', [timestamp])
            await connection.expireat(timestamp, int(timestamp+600))
            print('flushing:', time.time()-last, count)
            block = []
            count = 0
        last = time.time()

async def blocker_main():
    from rtlsdr import rtlsdraio
    sdr = rtlsdraio.RtlSdrAio()

    print('Configuring SDR...')
    sdr.rs = 256000
    sdr.fc = 89.7e6 
    sdr.gain = 50 
    print('  sample rate: %0.3f MHz' % (sdr.rs/1e6))
    print('  center frequency %0.6f MHz' % (sdr.fc/1e6))
    print('  gain: %s dB' % sdr.gain)

    print('Streaming bytes...')
    await process_samples(sdr)
    await sdr.stop()
    print('Done')
    sdr.close()

async def decoder_main():
    connection = await asyncio_redis.Connection.create('localhost', 6379, encoder = CborEncoder())
    while True:
        timestamp = await connection.brpop(['timestamps'], 360)
        timestamp = timestamp.value
        info = await connection.get(timestamp)
        fm.demodulate_array(decompress(**info))

def spawner(future_yielder):
    def loopwrapper(main):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(main())
        loop.run_forever()
    multiprocessing.Process(target = loopwrapper, args = (future_yielder,)).start()

if __name__ == "__main__":
    spawner(blocker_main)
    asyncio.ensure_future(decoder_main())
    asyncio.get_event_loop().run_forever()
