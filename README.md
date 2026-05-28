# [ threefive ]


## https://github.com/superkabuki/threefive

## threefive is the only tool that supports SCTE-35-1 and SCTE-35-2 

*   __Decodes SCTE-35__ from `MPEGTS`✔ `Base64`✔ `Bytes`✔ `DASH`✔ `Hex` ✔ `HLS`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔  
*   __Encodes SCTE-35__ to `MPEGTS`✔ `Base64`✔ `Bytes`✔ `Hex`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔
___

## [ News ]

* threefive now has support for SCTE-35-2. __Event Descriptors__ and __Property__ types from __the recently published 2026 SCTE-35 Specification can be decoded, modified, and encoded with threefive.   
___

## [ Latest version is  v3.0.89 ]
### Super Speed up with threefive v3.0.89
* One of my test for threefive is a 3.7 GB file with 286 SCTE-35 Cues.
* v3.0.89 cuts parsing time over 50% in every python interpreter. 

|interpreter| threefive v3.0.87| threefive v3.0.89|
|-----------|------------------|------------------|
|pypy3.9    |   4.13 seconds   |  __1.96 seconds__    |
|python3.11 |   11.81 seconds  |  __4.618 seconds__   |
|python3.14 |   14.33 seconds  |  __6.010 seconds__   |





___
##  [ Examples ]
* [aac_id3header.py](aac_id3header.py) - use the __threefive.aac.AacParser__ class to parse __HLS AAC__ segments for __PTS__ in __ID3 header tags__. _(__Updated__ 01/07/2026)_
* [id3.aac](id3.aac) test file for __aac_id3header.py__   _(__New!__ 01/12/2026)_
* [base64toxmlbin.py](base64toxmlbin.py) - __convert__ __base64__ encoded __SCTE-35__ to __xml+binary__ encoded SCTE-35 and back.
* [cue2vtt.py](cue2vtt.py) - display __SCTE-35__ in  __WebVTT__ subtitles to __verify__ __SCTE-35__ __splice points__.
* [decodenext.py](decodenext.py) - parse __MPEGTS__ streams for __SCTE-35__ using __Stream.decode_next()__.  _(__Updated__ 01/12/2026)_
* [dtmf.py](dtmf.py) - parse __base64__ __SCTE-35__ with a __DTMF__ descriptor and __re-encode__ to __SCTE-35__ in __Hex__ format.
* [edit_break_duration.py](edit_break_duration.py) - change the __SCTE-35__ __break duration__ and __re-encode__ __SCTE-35__.
* [event_descriptors.py](event_descriptors.py) - The __Event Descriptor__ examples from the __2026 SCTE-35 part 2 specification__. _(__New!__ 05/10/2026)_
* [encode_time_signal.py](encode_time_signal.py) - __encode__ a __SCTE-35__ __Cue__ with a __TimeSignal__ from scratch.
* [parsehlstags.py](parsehlstags.py) - use the __TagParser__ class to parse __HLS tags__ from a __m3u8__ file and group the tags by segment.
* [proxy.py](proxy.py) - how to use the __Stream.proxy()__ method for parsing __SCTE-35__ and __piping__ video.
* [quickstream.py](quickstream.py) - how to __add SCTE-35 parsing__ for __MPEGTS__ streams to __your application__.
* [spliceinsert.py](spliceinsert.py) - a __SCTE-35__ __Splice Insert__ example.  
* [upid_custom_output.py](upid_custom_output.py) - __customizing Upid data output__ for a variety of __Upids__. _(__New!__ 01/11/2026)_
* [custom_upid_handling.py](custom_upid_handling.py) -  Custom __user defined UPID__ handling example. _(__New!__ 01/11/2026)_
___


# [ Documentation ]
#### Need to inject SCTE-35 into HLS?  [X9k3.](https://github.com/superkabuki/x9k3)
* [__web based SCTE-35 tools__](#web) - threefive and friends over http. 
* [__install__](#install)
* [__quick start__](https://github.com/superkabuki/threefive_is_scte35/blob/main/README.md#quick-start)
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
# [⇧](#-documentation-)
___

# [⇧](#-documentation-)

## [Quick Start] 
<i>These examples show how to parse SCTE-35<BR> 
from various SCTE-35 data formats, with both the cli and with the library.</i> 
 <details><summary>MPEGTS</summary>
 
* MPEGTS streams can be  Files, Http(s), Multicast,SRT, UDP Unicast, or  stdin. 
* __cli__

```js
threefive https://example.com/video.ts
```
* wildcards work too.
```js
threefive /mpegts/*.ts
```

* __lib__
```py3

from threefive import Stream
stream = Stream('https://example.com/video.ts')
stream.decode()

```
</details>
<details><summary>Base64</summary>

* __cli__
```js
threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```
* __lib__
```py3

from threefive import Cue
data = '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
cue=Cue(data)
cue.show()
```

</details>


<details><summary>Bytes</summary>

* __cli__
	* Bytes don't work on the cli

* __lib__
```py3

from threefive import Cue
data =  b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\xc0D\xa0\x00\x00\x00\xb5k\x88'
cue=Cue(data)
cue.show()
```

</details>

<details><summary>Hex</summary>

* Can be a hex literal or hex string or bytes.

* __cli__
```js
threefive  0xfc301600000000000000fff00506fed605225b0000b0b65f3b
```
* __lib__
```py3

from threefive import Cue
data =  0xfc301600000000000000fff00506fed605225b0000b0b65f3b
cue=Cue(data)
cue.show()
```

</details>


<details><summary>Int</summary>

* Can be a literal integer or string or bytes.

* __cli__
```js
threefive  1583008701074197245727019716796221243043855984942057168199483
```
* __lib__
```py3

from threefive import Cue
data =  1583008701074197245727019716796221243043855984942057168199483
cue=Cue(data)
cue.show()
```


</details>


<details><summary>JSON</summary>

* __cli__
	* 	put JSON SCTE-35 in a file and redirect it into threefive
    *   cat files to threefive works too.
    *   echo JSON or type JSON on the command line.
   
```js
threefive  < json.json
```
* __lib__

```py3

 from threefive import Cue
 data = '''{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xb56b88"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 140.005333
    },
    "descriptors": []
}
'''
cue=Cue(data)
cue.show()
```

</details>


<details><summary><u>Xml</u></summary>

* __cli__
	* put xml SCTE-35 in a [file](xml.xml) and redirect it into threefive
    * cat files to threefive works too.
    * echo xml or type xml on the command line.
     
	```js
	threefive < xml.xml
	```
* __lib__
```py3
from threefive import Cue
data =  '''
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35" 
        ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="12600480"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
'''
cue=Cue(data)

cue.show()
```


</details>



<details><summary>Xml+binary</summary>

* __cli__
	* write xml+binary to a [file](xmlbin.xml) and redirect it to threefive
    * cat files to threefive works too.
    * echo xml+binary or type xml+binary on the command line.
```js
threefive < xmlbin.xml
```
* __lib__
```py3

from threefive import Cue
data = '''<scte35:Signal xmlns:scte35="https://scte.org/schemas/35">
    <scte35:Binary>/DAWAAAAAAAAAP/wBQb+AMBEoAAAALVriA==</scte35:Binary>
</scte35:Signal>
'''
cue=Cue(data)
cue.show()
```

</details>

</samp>

___

# [⇧](#-documentation-)

### [CLI]
The threefive cli tool is able to parse SCTE-35 from MPEGTS Streams,Base64,Hex,Integers,JSON XML,and XMLBinary.
The format is auto-detected.

# [⇧](#-documentation-)

#### [ Parse SCTE-35 from MPEGTS ]
SCTE-35 can be parsed from MPEGTS over a variety of protocols.
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

# [⇧](#-documentation-)

#### [ Parse SCTE-35 Cues ]

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

___

# [⇧](#-documentation-)

#### [__Additional functionality__]
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

___

# [⇧](#-documentation-)


### Other tools
threefive also comes with: 
#### scte35bump 

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
___

# [⇧](#-documentation-)

#### gums
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

# [⇧](#-documentation-)

#### scte35hls

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

# [⇧](#-documentation-)

#### __scte35fix__
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
___

# [⇧](#-documentation-)

### [Using the library]
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
___

# [⇧](#-documentation-)

### [web]
* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) __hosted on my server iodisco.com__
* Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ Go, Wasm and Super Karate Death Car](https://bigcorp.ltd/gowasm) __hosted om my server bigcorp.ltd__
*  Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ threefive.js,javascript, and a little sed](https://bigcorp.ltd/bread) just to keep things interesting. __hosted om my server bigcorp.ltd__
* [ SCTE-35 __Online Parser__ powered by threefive](http://www.domus1938.com/scte35parser) _another online parser powered by threefive_ not hosted on my servers.
* [SCTE-35 __As a Service__](sassy.md) _if you can make an http request, you can parse SCTE-35, no install needed._
__hosted on my server iodisco.com__
___

# [⇧](#-documentation-)

### [XML]
* [XML](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) __New__! _updated 05/01/2025_

### [HLS]
* [Advanced Parsing of SCTE-35 in HLS with threefive](https://github.com/superkabuki/threefive/blob/main/hls.md) All HLS SCTE-35 tags, Sidecar Files, AAC ID3 Header Timestamps, SCTE-35 filters... Who loves you baby?

 # [⇧](#-documentation-)
 
###  [Classes]
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

# [⇧](#-documentation-)

### [threefive now supports SRT]

* _( You have to unmute the audio )_

https://github.com/user-attachments/assets/a323ea90-867f-480f-a55f-e9339263e511

<BR> 

* [more SRT and threefive info](srt.md)


* _checkout [SRTfu](https://github.com/superkabuki/srtfu)_

___

# [⇧](#-documentation-)

### [more]

* [Encode SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) Some encoding code examples. 
___

# [⇧](#-documentation-)
