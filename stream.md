# threefive.Stream class

##   Stream class for parsing MPEG-TS data.

### class threefive.Stream

* The threefive.Stream class is used for parsing SCTE-35 from MPEGTS streams.

###   Stream(tsdata, show_null=True, headers={})
    
* __tsdata__ is a file or stdin or http(s) or multicast or SRT or UDP stream
 
*  __set show_null__ =False to exclude Splice Nulls

* __headers__ is a dict of Http(s) or SRT headers (if needed).        

___

#### func=show_cue

* Many of  threefive.Stream's methods accept an optional func arg.
    * func is a function that accepts once arg, a SCTE-35 cue.
    * func is called whenever a SCTE-35 message is found.
    * the default is show_cue, it calls cue.show() to print the SCTE-35 JSON to stderr.

```py3
def show_cue(cue):
    cue.show()
```

## Commonly Used Methods
* Below are the methods most often used with __threefive.Stream__.
	* [decode](#decodeself-funcshow_cue)
	* [decode_next](#decode_nextself)
	* [decode_pcr](#decode_pcrself-funcshow_cue)
	* [decode_pids](#decode_pidsself-scte35_pidsnone-funcshow_cue)
	* [mpdecode](#mpdecodeself-funcshow_cue)
	* [proxy](#proxyself-funcshow_cue)
	* [rt](#rtself-funcshow_cue)
	* [show](#showself)

####   decode(self, func=show_cue)
       Stream.decode reads self.tsdata to find SCTE35 packets.
       func can be set to a custom function that accepts
       a threefive.Cue instance as it's only argument.
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.decode()
```      


####   decode_next(self)
       Stream.decode_next returns the next
       SCTE35 cue as a threefive.Cue instance.

```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       for cue in strm.decode_next():
           print(cue.xml())
```   
   
####   decode_pcr(self, func=show_cue)
       decode_pcr same as decode() but also includes pcr values

```py3       
       from threefive import Stream
       strm = Stream("vid.ts",show_null=False)
       strm.decode_pcr()
```   

####   decode_pids(self, scte35_pids=None, func=show_cue)
       Stream.decode_pids takes a list of SCTE-35 Pids parse
       and an optional call back function to run when a Cue is found.
       if scte35_pids is not set, all threefive pids will be parsed.
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.decode_pids(scte35_pids=[256,512,1033])
```   

####   mpdecode(self, func=show_cue)
       mpdecode decode with multiprocessing
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.mpdecode()
```   


   
####   proxy(self, func=show_cue)
     Stream.decode_proxy writes all ts packets are written to stdout
       for piping into another program like mplayer.
       SCTE-35 cues are print2`ed to stderr.
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.proxy()
```   

   
####   rt(self, func=show_cue)
       rt  all ts packets are written to stdout
       for piping into another program in real time.
       SCTE-35 cues are print2`ed to stderr.
       decode SCTE-35.  the arg func can be set to
       a function that accepts one arg, a Cue instance.
       func is called everytime a Cue is found in the stream.
       the default func, show_cue calls Cue.show().
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.rt()
```   

####   show(self)
       displays mpegts programs and  stream types
```py3       
       from threefive import Stream
       strm = Stream("vid.ts")
       strm.show()
```   
   

