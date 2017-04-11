# Authors: Josh Myer <www.joshisanerd.com>, Veeresh Taranalli <veeresht@gmail.com>, Ian Daniher <itdaniher@gmail.com>
# License: BSD 3-Clause

from streamer import *
from scipy import signal

import numpy
import math
import cmath
import pprint

def rrcosfilter(N, alpha, Ts, Fs):
    """ rrcos filter for reducing ISI by VT """
    T_delta = 1/float(Fs)
    time_idx = ((numpy.arange(N)-N/2))*T_delta
    sample_num = numpy.arange(N)
    h_rrc = numpy.zeros(N, dtype=float)
    for x in sample_num:
        t = (x-N/2)*T_delta
        if t == 0.0:
            h_rrc[x] = 1.0 - alpha + (4*alpha/numpy.pi)
        elif alpha != 0 and t == Ts/(4*alpha):
            h_rrc[x] = (alpha/numpy.sqrt(2))*(((1+2/numpy.pi)* \
                    (numpy.sin(numpy.pi/(4*alpha)))) + ((1-2/numpy.pi)*(numpy.cos(numpy.pi/(4*alpha)))))
        elif alpha != 0 and t == -Ts/(4*alpha):
            h_rrc[x] = (alpha/numpy.sqrt(2))*(((1+2/numpy.pi)* \
                    (numpy.sin(numpy.pi/(4*alpha)))) + ((1-2/numpy.pi)*(numpy.cos(numpy.pi/(4*alpha)))))
        else:
            h_rrc[x] = (numpy.sin(numpy.pi*t*(1-alpha)/Ts) +  \
                    4*alpha*(t/Ts)*numpy.cos(numpy.pi*t*(1+alpha)/Ts))/ \
                    (numpy.pi*t*(1-(4*alpha*t/Ts)*(4*alpha*t/Ts))/Ts)
    return time_idx, h_rrc

def symbol_recovery_24(xr, xdi, xdq):
    """ period 24 pll by VT """
    # binarize the phase modulation
    bi = (numpy.real(xr) >= 0) + 0
    # pll parameters
    period = 24
    halfPeriod = period / 2
    corr = period / 24.
    phase = 0

    res = []
    pin = 0

    stats = {0: 0, 1: 1}
    oddity = 0

    latestXrSquared = [0]*8
    lxsIndex = 0
    theta = [0]
    shift = 0

    # pll
    for i in range(1, len(bi)):
        if bi[i-1] != bi[i]:
            if phase < halfPeriod-2:
                phase += corr
            elif phase > halfPeriod+2:
                phase -= corr
        if phase >= period:
            phase -= period
            latestXrSquared[lxsIndex] = (xdi[i] + 1j * xdq[i])**2
            lxsIndex += 1
            if lxsIndex >= len(latestXrSquared):
                lxsIndex = 0
            th = shift + cmath.phase(sum(latestXrSquared)) / 2
            if abs(th - theta[-1]) > 2:
                if th < theta[-1]:
                    shift += math.pi
                    th += math.pi
                else:
                    shift -= math.pi
                    th -= math.pi
            theta.append(th)
            oddity += 1
            if oddity == 2:
                oddity = 0
                yp = (xdi[i] + 1j * xdq[i])
                ypp = cmath.exp(-1j * th) * yp
                # bit decode
                nin = 1 * (ypp.real > 0)
                stats[nin] += 1
                res.append(pin ^ nin)
                pin = nin
        phase += 1
    return res

def rds_crc(message, m_offset, mlen):
    """ public domain (?) minimum viable implementation of rds crc by grc authors etc """
    POLY = 0x5B9 # 10110111001, g(x)=x^10+x^8+x^7+x^5+x^4+x^3+1
    PLEN = 10
    SYNDROME=[383, 14, 303, 663, 748]
    OFFSET_NAME=['A', 'B', 'C', 'D', 'C\'']
    reg = 0

    if((mlen != 16)and(mlen != 26)):
        raise ValueError
    # start calculation
    for i in range(mlen):
        reg=(reg<<1)|(message[m_offset+i])
        if(reg&(1<<PLEN)):
            reg=reg^POLY
    for i in range(PLEN,0,-1):
        reg=reg<<1
        if(reg&(1<<PLEN)):
            reg=reg^POLY
    checkword=reg&((1<<PLEN)-1)
    # end calculation
    for i in range(0,5):
            if(checkword==SYNDROME[i]):
                #print "checkword matches syndrome for offset", OFFSET_NAME[i]
                return OFFSET_NAME[i]

    return None

def _collect_bits(bitstream, offset, n):
    """Helper method to collect a string of n bits, MSB, into an int"""
    retval = 0
    for i in range(n):
        retval = retval*2 + bitstream[offset+i]
    return retval

def decode_A(bitstream, offset):
    """Trivial RDS block A decoder"""
    return _collect_bits(bitstream, offset, 16)

def decode_B(bitstream, offset):
    """Trivial RDS block B decoder"""
    retval = {}

    retval["group_type"] = _collect_bits(bitstream, offset, 4)
    retval["version_AB"] = "B" if bitstream[offset+4] else "A"
    retval["traffic_prog_code"] = bitstream[offset+5]
    retval["prog_type"] = _collect_bits(bitstream, offset+6,5)

    if retval["group_type"] == 2:
        retval["text_segment"] = _collect_bits(bitstream, offset+12, 4)
    elif retval["group_type"] == 0:
        retval["pi_segment"] = _collect_bits(bitstream, offset+14, 2)

    return retval

def decode_C(bitstream, offset):
    """Trivial RDS block C decoder"""
    c0 = _collect_bits(bitstream, offset, 8)
    c1 = _collect_bits(bitstream, offset+8, 8)

    return ( chr(c0), chr(c1))

def decode_Cp(bitstream, offset):
    """Stub RDS block C decoder"""
    return None

def decode_D(bitstream, offset):
    """Trivial RDS block D decoder"""
    return decode_C(bitstream, offset)

# A lookup table to make it easier to dispatch to subroutines in the code below
decoders = { "A": decode_A, "B": decode_B, "C": decode_C, "C'": decode_Cp, "D": decode_D }

def decode_one(bitstream, offset):
    s = rds_crc(bitstream, offset, 26)
    if None == s:
        return None

    return (s, decoders[s](bitstream, offset))

def accumulate_radiotext(parses, cur_state = None):
    """A state machine that accumulates the radio text messages

    This takes in a whole list of packet-qualifying blocks (ie:
    a list of blocks, but which have been filtered down such that
    they always come in ABCD or ABC'D order, and each quad is
    adjacent in the bitstream).

    Returns a list of states of the radio text as it progresses
    through consuming the input packets.
    """
    if cur_state == None:
        cur_state = ["_"] * 64

    retval = [ "".join(cur_state) ]

    cursor = None
    for blkid, decode in parses:
        if blkid == "B":
            if decode['group_type'] == 2:
                cursor = decode['text_segment'] * 4
            else:
                cursor = None
        if None != cursor:
            if blkid == "C":
                cur_state[cursor] = decode[0]
                cur_state[cursor+1] = decode[1]
                retval.append("".join(cur_state))
            elif blkid == "D":
                cur_state[cursor+2] = decode[0]
                cur_state[cursor+3] = decode[1]
                retval.append("".join(cur_state))

            if blkid == "A" or blkid == "D":
                cursor = None
    return retval

def accumulate_b0text(parses, cur_state = None):
    if cur_state == None:
        cur_state = ["_"] * 8

    retval = [ "".join(cur_state) ]

    cursor = None
    for blkid, decode in parses:
        if blkid == "B":
            if decode['group_type'] == 0:
                cursor = decode['pi_segment'] * 2
            else:
                cursor = None
        if None != cursor:
            if blkid == "D":
                cur_state[cursor] = decode[0]
                cur_state[cursor+1] = decode[1]
                retval.append("".join(cur_state))
            if blkid == "A" or blkid == "D":
                cursor = None
    return retval

basebandBP = signal.remez(512, np.array([0, 53000, 54000, 60000, 61000, 256e3/2]), np.array([0, 1, 0]), Hz = 256000)
filtLP = signal.remez(400, [0, 2400, 3000, 228e3//4], [1, 0], Hz=228e3//2)
smooth = 1/200. * numpy.ones(200)
pulseFilt = rrcosfilter(300, 1, 1/(2*1187.5), 228e3//2) [1]

def demodulate_array(h):
    i = h[1:] * np.conj(h[:-1])
    j = np.angle(i)

    k = signal.convolve(j, basebandBP)

    # resample from 256kHz to 228kHz
    rdsBand = signal.resample(k, int(len(k)*228e3/256e3))

    # length modulo 4
    rdsBand = rdsBand[:(len(rdsBand)//4)*4]
    c57 = numpy.tile( [1., -1.], len(rdsBand)//4 )

    xi = rdsBand[::2] * c57
    xq = rdsBand[1::2] * (-c57)

    xfi = signal.convolve(xi, filtLP)
    xfq = signal.convolve(xq, filtLP)
    xsfi = signal.convolve(xfi, pulseFilt)
    xsfq = signal.convolve(xfq, pulseFilt)

    if len(xsfi) % 2 == 1:
        xsfi = xsfi[:-1]
        xsfq = xsfq[:-1]

    xdi = (xsfi[::2] + xsfi[1::2]) / 2
    xdq = xsfq[::2]

    angles = numpy.where(xdi >= 0, numpy.arctan2(xdq, xdi), numpy.arctan2(-xdq, -xdi))

    theta = (signal.convolve(angles, smooth)) [-len(xdi):]

    xr = (xdi + 1j * xdq) * numpy.exp(-1j * theta)

    res = symbol_recovery_24(xr, xdi, xdq)
    my_hits = []
    for i in range(len(res)-26):
        h = rds_crc(res, i, 26)
        if h:
            my_hits.append( (i, h) )

    hit_parses = []
    for i in range(len(my_hits)-3):
        if my_hits[i][1] == "A":
            bogus = False
            for j,sp in enumerate("ABCD"):
                if 26*j != my_hits[i+j][0] - my_hits[i][0]:
                    bogus = True
                if my_hits[i+j][1] != sp:
                    bogus = True
            if not bogus:
                for j in range(4):
                    hit_parses.append( (my_hits[i+j][0], decode_one(res, my_hits[i+j][0])))

    pprint.pprint(set(accumulate_radiotext([ b for (a,b) in hit_parses])))
    pprint.pprint(set(accumulate_b0text([ b for (a,b) in hit_parses])))

if __name__ == "__main__":
    import sys
    f = open(sys.argv[-1].encode('utf-8'), 'rb')
    g = cbor.loads(f.read())
    h = decompress(**g)
    demodulate_array(h)
