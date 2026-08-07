# Secure Reliable Transport in threefive
# threefive supports the default "live" mode for SRT.
Secure Reliable Transport __works just like everything else__ 
Just pass in the srt url.

* __parse SCTE35 from an SRT stream and return SCTE35 as JSON__
```sh
threefive srt://127.0.0.1:4201 
```
* __parse SRT stream and create a SCTE35 sidecar file__
```sh
threefive srt://10.11.12.13:1415 sidecar
```
* __Create a threefive.Stream instance and parse an SRT stream for SCTE35__
```py3
from threefive import Stream

strm =Stream('srt://206.125.170.41:9000')
strm.decode()
```

