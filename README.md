This application decodes live RadioText / RDS / RBDS FM radio metadata, such as station callsign and the currently display'ed radio text. This is a reasonably effective alternative to [Windytan's awesome application, Redsea](https://github.com/windytan/redsea).

I set out to build a framework for localisation and timestamping a system based on nothing but a RTLSDR receiver, and at this point, we're pretty close.

The project started with an amalgamation of [joshisanerd's work on RDS decoding](http://www.joshisanerd.com/projects/sdr_snippets/gnuradio_and_ipython//2%20Broadcast%20FM%20RDS%20Decode.html#Extracting-the-RDS-Text) and [ChristopheJacquet's Pydemod demo code](https://github.com/ChristopheJacquet/Pydemod/blob/master/src/demodulate_rds.py) but has been pretty much rewritten from scratch at this point.

Also useful was the GRC implementation of caculating the RDS block checksums.

See the following for additional information on the protocols and technology in play:

* [pyFmRadio - Radio Broadcast Data System & Radio Data System](http://davidswiston.blogspot.com/2014/12/pyfmradio-radio-broadcast-data-system.html)
* [Redsea 0.7, a lightweight RDS decoder](http://www.windytan.com/2016/10/redsea-07-lightweight-rds-decoder.html)
* [Specification of the radio data system (RDS) for VHF/FM sound broadcasting in the frequency range from 87,5 to 108,0 MHz](http://www.interactive-radio-system.com/docs/EN50067_RDS_Standard.pdf)
