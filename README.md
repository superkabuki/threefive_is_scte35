### Try [threefive.js](https://github.com/keithah/threefive.js)


___

# [ threefive ]
## https://github.com/superkabuki/threefive

### threefive is the industry leading SCTE-35 tool. 
#### Need to inject SCTE-35 into HLS?  [X9k3.](https://github.com/superkabuki/x9k3) 

*   __Decodes SCTE-35__ from `MPEGTS`✔ `Base64`✔ `Bytes`✔ `DASH`✔ `Hex` ✔ `HLS`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔
  
*   __Encodes SCTE-35__ to `MPEGTS`✔ `Base64`✔ `Bytes`✔ `Hex`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔
___
## Breaking News: Make threefive run twice as fast with python3.11 and python3.14 
* This parses SCTE-35 from an MPEGTS stream using a multiprocessing pool and multiple threefive.Stream instances.
*  Works great with python3.11 and 3.14
* Test it
	* `time python3 chunkymp.py video.ts`
	* compare with `time threefive video.ts`

* chunkymp.py
  
```py3
import multiprocessing
import sys
from threefive import Stream, reader

pkt_size=188
chunk_size= pkt_size*3500

def chunk_parser(chunk):
    """
    chunk_parser parse a chunk
    """
    st=Stream(None)
    return [cue for cue in [st._parse(pkt) for pkt in st.packetize( chunk)] if cue]


def chunker(file_path):
    """
    chunker chunk generator
    """
    with reader(file_path) as r:
        while True:
            chunk = r.read(chunk_size)
            if not chunk:
                break
            yield chunk

if __name__ == '__main__':
    file_path = sys.argv[1]  
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()-1) as pool:
        results = pool.imap(chunk_parser, chunker(file_path),chunksize=1)
        for cues in results:
             _=[cue.show() for cue in cues]
```


---

## The State of Stuff:
<pre>
I would like to announce that have once again officially flip-flopped my position on including PCR values.
Firstly, SCTE-35 does not use PCR timestamps. 
Secondly, there is no guarantee that the PCR and PTS values remain in sync or 
even related in any way. 
Often when video is spliced or re-encoded, 
the original PCR values will remain while the PTS is recalculated. 
The reason threefive can parse raw video despite being written in a scripting language 
is because I've spent a lot of time working on the performance. 
Performance wise I have also noticed PCR is parsed a lot more frequently than PTS. 
Profiling threefive with one of my test files shows 1,604,796 calls to parse the PTS
and 8,022,706 calls to parse PCR. That's a big difference. 
Running that same test file and parsing PCR and PTS takes roughly fourteen seconds, 
parsing only PTS with the test file takes ten seconds. 
It seems like an easy choice, 
improve perfomance by not parsing data that really isn't relavant to the task at hand. 
However, I can think of a few guys who will not take this decision well, 
so to keep them from sending me death threats, in the next release of threefive, 
calling Stream.decode() will not include PCR values, 
but calling Stream.decode_pcr() will include both PCR and PTS values.

I think that is reasonable. If you don't, open an issue and make your case.
	
</pre>

# Tip of the week.
## Q. How do I get a list of all of the SCTE-35 cues in a stream?
## A. Call Stream.decode_next(), it's a python generator.
```py3
from threefive import Stream

strm=Stream('https://example.com/video.ts')
list_o_cues=[]
for cue in strm.decode_next():    
	list_o_cues.append(cue)       # these will be threefive.Cue instances

# then you can do stuff like

_=[cue.show() for cue in list_o_cues]

for cue in list_o_cues:
	print(cue.xml())

```	

### [ News ]

* __threefive no longer uses setuptools for packaging__ and I know you don't care.
* __Python3 vs. Pypy3__ [__parsing SCTE35 with threefive__](https://github.com/superkabuki/threefive_is_scte35#python3-vs-pypy3-running-threefive) (watch the cool video) 
* __threefive now supports__ [__Secure Reliable Transport__](https://github.com/superkabuki/threefive_is_scte35/blob/main/README.md#threefive-now-supports-srt)  (watch the cool video)
___

## [ Latest version is  v3.0.83 ]

*  threefive cyclomatic complexity score is 1.9337094499294782 _( that's better than the Python standard library)_ .
* __threefive now has NO External Dependencies__
	* SRT and AES support is now optional 
* __threefive is fully python v3.14 compliant__
* __No more setup tools!__ threefive now uses a __toml file and a Makefile__ to generate packages,
	* I'm just trying to fit in with the cool python kids. 
* __New__ the threefive cli tool has spun off several new cli tools. I had to split the cli up, the help was just way too long. 
	* In addition to the __threefive__ cli you also get: 
		* __scte35bump__  _adjust scte-35 pts in mpegts streams_ 
 		* __scte35fix__   _change bin data streams back to scte-35_
  		* __scte35hls__  _parse scte-35 from hls tags and segments_
    	* __scte35inject__ _inject scte-35 packets into mpegts streams_
     	* __gums__ _(the Grande Unified unicast and Multicast Server)_
___        
#  [__[ Examples ]__](https://github.com/superkabuki/threefive/tree/main/examples)



# [ Documentation ]

* __use threefive on the web__
	* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) hosted on my server_
	* [ SCTE-35 __Online Parser__ powered by threefive](http://www.domus1938.com/scte35parser) _another online parser powered by threefive_
	* [SCTE-35 __As a Service__](sassy.md) _if you can make an http request, you can parse SCTE-35, no install needed._

* [__install__](#install) 
* __command line tools__
	* [ __threefive__](#cli) _decode SCTE-35 on the command line_
  	* [__scte35bump__](#scte35bump) _adjust SCTE-35 PTS in MPEGTS streams_ 
    * [__scte35fix__](#scte35fix)  _ffmpeg changes scte-35 streams into bin data, scte35fix changes them back._
  	* [__scte35hls__](#scte35hls) _scte35hls parses hls and ABR hls for scte-35. All hls scte-35 tags are supported__ 
	* [__scte35inject__](scte35inject.md) _scte35inject inject scte-35 into mpegts._
  	* [__gums__](#gums) _gums is a  multicast sender(server) for video_ 
* __library__
 	* [__Using the threefive.Cue class__](https://github.com/superkabuki/threefive/blob/main/lib.md) 
	* [__Using the threefive library__](#using-the-library) _decode SCTE-35 with less than ten lines of code_
 	* * [threefive __Classes__](#classes) _threefive is OO, made to subclass_
		* [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) _this class you'll use often_ 
		* [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) _this is the class for parsing MPEGTS_

* [SCTE-35 __Sidecar Files__](https://github.com/superkabuki/SCTE-35_Sidecar_Files) _threefive supports SCTE-35 sidecar files_
* [SCTE-35 __HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) _parse SCTE-35 in HLS__
* [SCTE-35 __XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) _threefive can parse and encode SCTE-35 xml_
* [__Encode__ SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) _threefive can encode SCTE-35 in every SCTE-35 format_
* [Make your __threefive__ script an executable with __cython__](cython.md) _threefive is compatible with all python tools_
</samp>

##  [Install]
* __python3 via pip__
```rebol
python3 -mpip install threefive
```
* __pypy3 via pip__ 
```rebol
pypy3 -mpip install threefive
```
* __To add SRT support__
```py3
python3 -m pip install srtfu
```
* __To add Automatic AES decryption__
```py3
python3 -mpip install pyaes
```

* __From the git repo__

```rebol
git clone https://github.com/superkabuki/scte35.git
cd threefive
make install
```
* I've jazzed up the makefile to make it easier to install for different python  versions and pypy3
```rebol
git clone https://github.com/superkabuki/scte35.git
cd threefive

make install py3=pypy3

# OR

make install py3=python3.14

# works for any python in your path or use a full path if needed.

```

___


## [Quick Start] 
## [CLI]
* The default action is to read a SCTE-35 input and write a SCTE-35 output.
---

## [ Parse SCTE-35 from MPEGTS ]
  
* __SCTE-35 Input__: MPEGTS
*  __Protocols__: pipes, files, stdin, http(s), multicast,SRT and UDP.
* __SCTE-35 Output__: JSON _(default)_ base64, bytes, hex, int, xml, and xmlbin.

|SCTE-35 Input  | Protocol   | SCTE-35 Output     | Command                                             |
|-------|------------|-----------|---------------------------------------------------------|
|__MPEGTS__|file|__JSON__   | __threefive__ video.ts										 |  
|__.__|https|__base64__ | __threefive__ https://example.com/video.ts  __base64__      |
|__.__|multicast|__bytes__ | __threefive__ udp://@235.3.5:3535  __bytes__      |
|__.__|SRT|__hex__ | __threefive__ srt://1.2.3.4:4201  __hex__      |
|__.__|UDP|__int__ | __threefive__ udp://10.10.10.10:1011  __int__      |
|__.__|Pipe|__xml__| cat video.ts \| __threefive__  __xml__                           |
|__.__|stdin|__xml+bin__| __threefive__  __xmlbin__ < video.ts|
___
## [ Parse SCTE-35 Cues ]

  *  The __default output__ is JSON
  *  __SCTE-35 Inputs:__  base64, hex, int, JSON,int,xml,and xmlbin.
  *  __SCTE-35 Outputs:__ base64, bytes, hex, int,JSON, xml, and xmlbin.
  *  __Any Input can be used with Any Output__

> __Here are several examples.__

|SCTE-35 Input  |  SCTE-35 Output     | Command                                             |
|-------|-----------|---------------------------------------------------------|
|__base64__|__JSON__    | __threefive__ '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' |
|__.__|__bytes__    | __threefive__ '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' __bytes__|
|__.__|__hex__    | __threefive__ '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' __hex__|
|__.__|__xml__    | __threefive__ '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' __xml__|
|__hex__  | __JSON__  | __threefive__ 0xfc301600000000000000fff00506fe00a98ac700000b3baed9|
|__.__  | __base64__  | __threefive__ 0xfc301600000000000000fff00506fe00a98ac700000b3baed9 __base64__ |
|__.__  | __int__  | __threefive__ 0xfc301600000000000000fff00506fe00a98ac700000b3baed9 __int__ |
|__.__  | __xmlbin__  | __threefive__ 0xfc301600000000000000fff00506fe00a98ac700000b3baed9 __xmlbin__ |
| __int__ | __JSON__    | __threefive__ 1583008701074197245727019716796221242036302348025116111908569  |  
|__.__ | __hex__    | __threefive__ 1583008701074197245727019716796221242036302348025116111908569 __hex__ |  
|__.__ | __xml__    | __threefive__ 1583008701074197245727019716796221242036302348025116111908569 __xml__ |
|__JSON__ |__base64__    | __threefive__  < json.json  __base64__                         |
|__.__  |__bytes__    | __threefive__  < json.json  __bytes__                         |
|__.__  |__xml__    | __threefive__  < json.json  __xml__                         |
|__xml__   |__JSON__   | __threefive__   < xml.xml                                   |
|__xmlbin__|__int__    | __threefive__   < xmlbin.xml __int__                        |

---
## [__Additional functionality__]
* threefive has several additional features, mostly related to MPEGTS streams.
* threefive has built in help, just type `threefive help`
* This table shows how to use them.

| Description                              | How To Use                                       |
|------------------------------------------|---------------------------------------------------------|
| Inject __SCTE35__ packets                |threefive __inject__ -i in.video -s sidecar.txt -o out.ts|
| Show raw __SCTE35__ packets              |threefive __packets__ udp://@235.35.3.5:3535             |
| Copy MPEGTS stream to stdout at realtime speed| threefive __rt__ input.ts | mplayer -				|
| Create __SCTE35__ sidecar file           |threefive __sidecar__ video.ts                           |
| Show streams in mpegts stream            | threefive __show__ https://example.com/video.ts         |
| Show __iframes__ in mpegts stream        |threefive __iframes__ srt://10.10.1.3:9000               |
| Show __PTS__ values from mpegts stream   | threefive __pts__ udp://192.168.1.10:9000               |
|__Proxy__ the __mpegts__ stream to stdout |threefive __proxy__ https://wexample.com/video.ts        |
|                                          |                                                         |
|                                          |                                                         |
---

## Other tools
threefive also comes with: 
### scte35bump 

* bump adjusts SCTE-35 PTS in an MPEGTS stream

```js
$ scte35bump -h
usage: scte35bump [-h] [-i INFILE] [-o OUTFILE] [-s SECS]

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Input source, stdin, file, http(s), udp, or multicast
                        mpegts [default: sys.stdin.buffer]
  -o OUTFILE, --outfile OUTFILE
                        Output file [default: sys.stdout.buffer]
  -s SECS, --secs SECS  Adjustment to apply to SCTE-35 Cues. [default: 0.0]

scte35bump is part of threefive.
```

---

### gums
*  the Grande Udp Multicast Server

```js
$ gums -h
usage: gums [-h] [-i INPUT] [-a ADDR] [-b BIND_ADDR] [-t TTL]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" or "https://futzu.com/xaa.ts"
                        [default: sys.stdin.buffer]
  -a ADDR, --addr ADDR  Destination IP:Port [default: 235.35.3.5:3535]
  -b BIND_ADDR, --bind_addr BIND_ADDR
                        Local IP to bind [default: 0.0.0.0]
  -t TTL, --ttl TTL     Multicast TTL (1 - 255) [default: 32]

gums is part of threefive.
```
### scte35hls

* parse HLS for SCTE-35. Supports all HLS SCTE-35 tags.

```js
$ scte35hls -h

[ threefive hls ]

[ Help ]

    To display this help:
	scte35hls help

[ Input ]
    threefive hls takes an m3u8 URI as input.
    M3U8 formats supported:
        * master  ( When a master.m3u8 used,
                   threefive hls parses the first rendition it finds )
        * rendition
    Segment types supported:
    * AAC
    * AC3
    * MPEGTS
    *codecs:
        * video
            * mpeg2, h.264, h.265
        * audio
            * mpeg2, aac, ac3, mp3
```

### __scte35fix__
* when ffmpeg changes a SCTE-35 stream to bin data stream, scte35fix changes it back. 

```js
$ scte35fix -h

  scte35fix checks MPEGTS for SCTE-35 Streams
  that have been change to bin data (type 0x06)
  and changes them back to SCTE-35 (type 0x86) streams.
  Output files are created in the current directory
  and prefixed with 'sixfix-'.
  Only bin data streams containing SCTE-35 will be converted.
  Multiple files can be specified on the command line.
  Wild cards work too.

  Example Usage:
        scte35fix video.ts
        scte35fix video1.ts video2.ts
        scte35fix video*.ts
        scte35fix https://example.com/video.ts
        scte35fix srt://10.10.10.13:4201
scte35fix is part of threefive.
```

## [XML]
* [XML](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) __New__! _updated 05/01/2025_

## [HLS]
* [Advanced Parsing of SCTE-35 in HLS with threefive](https://github.com/superkabuki/threefive/blob/main/hls.md) All HLS SCTE-35 tags, Sidecar Files, AAC ID3 Header Timestamps, SCTE-35 filters... Who loves you baby?
##  [SCTE-35 As a Service]
* Decode SCTE-35 without installing anything. If you can make an https request, you can use [__Sassy__](sassy.md) to decode SCTE-35. . 
##  [Classes]
* The python built in help is always the most up to date docs for the library.

```py3

a@fu:~/build7/threefive$ pypy3

>>>> from threefive import Stream
>>>> help(Stream)

```

* [Class Structure](https://github.com/superkabuki/threefive/blob/main/classes.md)
* [Cue Class](https://github.com/superkabuki/threefive/blob/main/cue.md)  Cue is the main SCTE-35 class to use. 
* [Stream Class](https://github.com/superkabuki/threefive/blob/main/stream.md)  The Stream class handles MPEGTS SCTE-35 streams local, Http(s), UDP, and Multicast.

___

### [threefive now supports SRT]

* _( You have to unmute the audio )_

https://github.com/user-attachments/assets/a323ea90-867f-480f-a55f-e9339263e511

<BR> 

* [more SRT and threefive info](srt.md)


* _checkout [SRTfu](https://github.com/superkabuki/srtfu)_

___

## [more]

* [Online SCTE-35 Parser](https://iodisco.com/scte35)  Supporte Base64, Bytes,Hex,Int, Json, Xml, and Xml+binary.

* [Encode SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) Some encoding code examples. 
___


## __Python3 vs Pypy3 running threefive__

* __( You have to unmute the audio )__

https://github.com/user-attachments/assets/9e88fb38-6ad0-487a-a801-90faba9d72c6



___

# Using the library
* Let me show you how easy threefive is to use.

* reading SCTE-35 xml from a file
```py3
a@fu:~/threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import reader
>>>> from threefive import Cue
>>>> data =reader('/home/a/xml.xml').read()
```
* load it into a threefive.Cue instance
```py3
>>>> cue = Cue(data)
```
* Show the data as JSON
```py3
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 92,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 60,
        "crc": "0x7632935"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": false,
        "break_duration": 180.0,
        "splice_event_id": 1073743095,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": false,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 12,
        "avails_expected": 5
    },
    "descriptors": [
        {
            "tag": 0,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 12,
            "descriptor_length": 8
        },
        {
            "tag": 0,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 13,
            "descriptor_length": 8
        },
      

    ]
}
```
* convert the data back to xml
```py3
>>>> print(cue.xml())
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1073743095" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="12" availsExpected="5" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="false" duration="16200000"/>
   </scte35:SpliceInsert>
   <scte35:AvailDescriptor providerAvailId="12"/>
   <scte35:AvailDescriptor providerAvailId="13"/>
   <scte35:AvailDescriptor providerAvailId="14"/>
   <scte35:AvailDescriptor providerAvailId="15"/>
   <scte35:AvailDescriptor providerAvailId="16"/>
   <scte35:AvailDescriptor providerAvailId="17"/>
</scte35:SpliceInfoSection>
```
* convert to xml+binary
```py3
>>>> print(cue.xmlbin())
<scte35:Signal xmlns:scte35="https://scte.org/schemas/35">
    <scte35:Binary>/DBcAAAAAAAAAP/wDwVAAAT3f69+APcxQAABDAUAPAAIQ1VFSQAAAAwACENVRUkAAAANAAhDVUVJAAAADgAIQ1VFSQAAAA8ACENVRUkAAAAQAAhDVUVJAAAAEQdjKTU=</scte35:Binary>
</scte35:Signal>
```
* convert to base64
```py3
>>>> print(cue.base64())
/DBcAAAAAAAAAP/wDwVAAAT3f69+APcxQAABDAUAPAAIQ1VFSQAAAAwACENVRUkAAAANAAhDVUVJAAAADgAIQ1VFSQAAAA8ACENVRUkAAAAQAAhDVUVJAAAAEQdjKTU=
```
* convert to hex
```py3
>>>> print(cue.hex())
0xfc305c00000000000000fff00f05400004f77faf7e00f7314000010c05003c0008435545490000000c0008435545490000000d0008435545490000000e0008435545490000000f000843554549000000100008435545490000001107632935
```
* show just the splice command
```py3
>>>> cue.command.show()
{
    "command_length": 15,
    "command_type": 5,
    "name": "Splice Insert",
    "break_auto_return": false,
    "break_duration": 180.0,
    "splice_event_id": 1073743095,
    "splice_event_cancel_indicator": false,
    "out_of_network_indicator": true,
    "program_splice_flag": false,
    "duration_flag": true,
    "splice_immediate_flag": false,
    "event_id_compliance_flag": true,
    "unique_program_id": 1,
    "avail_num": 12,
    "avails_expected": 5
}
```
* edit the break duration
```py3
>>>> cue.command.break_duration=30
>>>> cue.command.show()
{
    "command_length": 15,
    "command_type": 5,
    "name": "Splice Insert",
    "break_auto_return": false,
    "break_duration": 30,
    "splice_event_id": 1073743095,
    "splice_event_cancel_indicator": false,
    "out_of_network_indicator": true,
    "program_splice_flag": false,
    "duration_flag": true,
    "splice_immediate_flag": false,
    "event_id_compliance_flag": true,
    "unique_program_id": 1,
    "avail_num": 12,
    "avails_expected": 5
}
```

* re-encode to base64 with the new duration
```py3
>>>> cue.base64()
'/DBcAAAAAAAAAP/wDwVAAAT3f69+ACky4AABDAUAPAAIQ1VFSQAAAAwACENVRUkAAAANAAhDVUVJAAAADgAIQ1VFSQAAAA8ACENVRUkAAAAQAAhDVUVJAAAAEe1FB6g='
```
* re-encode to xml with the new duration
```py3
>>>> print(cue.xml())
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1073743095" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="12" availsExpected="5" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="false" duration="2700000"/>
   </scte35:SpliceInsert>
   <scte35:AvailDescriptor providerAvailId="12"/>
   <scte35:AvailDescriptor providerAvailId="13"/>
   <scte35:AvailDescriptor providerAvailId="14"/>
   <scte35:AvailDescriptor providerAvailId="15"/>
   <scte35:AvailDescriptor providerAvailId="16"/>
   <scte35:AvailDescriptor providerAvailId="17"/>
</scte35:SpliceInfoSection>
```
* show just the descriptors
```py3
>>>> _ = [d.show() for d in cue.descriptors]
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 12,
    "descriptor_length": 8
}
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 13,
    "descriptor_length": 8
}
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 14,
    "descriptor_length": 8
}
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 15,
    "descriptor_length": 8
}
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 16,
    "descriptor_length": 8
}
{
    "tag": 0,
    "identifier": "CUEI",
    "name": "Avail Descriptor",
    "provider_avail_id": 17,
    "descriptor_length": 8
}
```
* pop off the last descriptor and re-encode to xml
```py3

>>>> cue.descriptors.pop()
{'tag': 0, 'identifier': 'CUEI', 'name': 'Avail Descriptor', 'private_data': None, 'provider_avail_id': 17, 'descriptor_length': 8}
>>>> print(cue.xml())
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1073743095" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="12" availsExpected="5" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="false" duration="2700000"/>
   </scte35:SpliceInsert>
   <scte35:AvailDescriptor providerAvailId="12"/>
   <scte35:AvailDescriptor providerAvailId="13"/>
   <scte35:AvailDescriptor providerAvailId="14"/>
   <scte35:AvailDescriptor providerAvailId="15"/>
   <scte35:AvailDescriptor providerAvailId="16"/>
</scte35:SpliceInfoSection>
```


## [ The Cli tool ]

#### The cli tool installs automatically with pip or the Makefile.

* [__SCTE-35 Inputs__](#inputs)
* [__SCTE-35 Outputs__](#outputs)
* [Parse __MPEGTS__ streams for __SCTE-35__](#streams)
* [Display __MPEGTS__ __iframes__](#iframes)
* [Display raw __SCTE-35 packets__ from __video streams__](#packets)

#### `Inputs`

* Most __inputs__ are __auto-detected.__ 
* __stdin__ is __auto selected__ and __auto detected.__
* __SCTE-35 data is printed to stderr__
* __stdout is used when piping video__
* mpegts can be specified by file name or URI.
```rebol
threefive udp://@235.2.5.35:3535
```
* If a file comtains a SCTE-35 cue as a string( base64,hex,int,json,or xml+bin), redirect the file contents.
```rebol

  threefive < json.json  

 ```

* quoted strings(( base64,hex,int,json or xml+bin), can be passed directly on the command line as well.

```awk

threefive '/DAWAAAAAAAAAP/wBQb+ztd7owAAdIbbmw=='

```


| Input Type |     Cli Example                                                                                             |
|------------|-------------------------------------------------------------------------------------------------------------|
| __Base64__     |  `threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='`
| __Hex__        |`threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b`|
| __HLS__         |`threefive hls https://example.com/master.m3u8`                                                             |
| __JSON__        |`threefive < json.json`  |
| __Xmlbin__      | `js threefive < xmlbin.xml`                                                                                 |

# `Streams`

|Protocol       |  Cli Example                                                                                                                                       |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|  __File__         |   `threefive video.ts`                                                                                                                            |
|  __Http(s)__      |   `threefive https://example.com/video.ts`                                                                                                        |
|  __Stdin__        |  `threefive < video.ts`            |
|  __UDP Multicast__|  `threefive udp://@235.35.3.5:9999`                                                                          |
|  __UDP Unicast__  |                                                                      `threefive udp://10.0.0.7:5555`                                              |


#### Outputs
* output type is determined by the key words __base64, bytes, hex, int, json, and xmlbin__.
* __json is the default__.
* __Any input  can be returned as any output__
  * examples __Base64 to Hex__ etc...) 


| Output Type | Cli Example         |
|-------------|----------------------------------------------------------|
|__Base 64__     |                                                                                                                                                                    `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  base64  `                                                                                                                                                                                                                                                                                                                                         |
| __Bytes__       |                                                                                 `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  bytes`                                                                                                                                                                                                                                                                                                                                                                                                                               |
| __Hex__         | `threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  hex`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| __Integer__     |                                                                                                                                                                                                                                                       `threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  int`   |
| __JSON__        |                                                                                                                                                                                                                                                                                                              `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b json ` |
| __Xml+bin__     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b xmlbin   `      |`
___
#### `Iframes`
* Show iframes PTS in an MPEGTS video

```smalltalk
threefive iframes https://example.com/video.ts
```
___

#### `packets`   
* Print raw SCTE-35 packets from multicast mpegts video

```smalltalk
threefive packets udp://@235.35.3.5:3535
```
___
#### `proxy`   
* Parse a https stream and write raw video to stdout

```smalltalk
threefive proxy video.ts
```
___
#### `pts`    
* Print PTS from mpegts video

```smalltalk
threefive pts video.ts
```
___
#### `sidecar`  
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt

```smalltalk
threefive sidecar video.ts
```
___

#### `show`  

* Probe mpegts video _( kind of like ffprobe )_

```smalltalk
 threefive show video.ts
```
___
#### `version`     
* Show version

```smalltalk
 threefive version
```
___
#### `help`        
* Help
```rebol
 threefive help
```
___




## [iodisco.com/scte35](https://iodisco.com/scte35)





 <svg width="100" height="100">
  <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
</svg> 

 <img width="258" height="256" alt="image" src="https://github.com/user-attachments/assets/642cb803-9465-408e-bb6e-03549eb22d78" />

___
 [__Install__](#install) |[__SCTE-35 Cli__](#the-cli-tool) |  [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) | [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) | [__Online SCTE-35 Parser__](https://iodisco.com/scte35) | [__SCTE-35 Examples__](https://github.com/superkabuki/threefive/tree/main/examples)
 | [__SCTE-35 XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) | [__threefive runs Four Times Faster on pypy3__](https://pypy.org/) 
