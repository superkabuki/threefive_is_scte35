

# threefive
 the industry leading SCTE-35 parser/decoder/encoder.  <BR>
  welcome to the show. 
___
* __Latest__ version is  __v3.0.93__  _Released 06/11/2026_
*   __Decodes SCTE-35__ from `MPEGTS`✔ `Base64`✔ `Bytes`✔ `DASH`✔ `Hex` ✔ `HLS`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔  
*   __Encodes SCTE-35__ to `MPEGTS`✔ `Base64`✔ `Bytes`✔ `Hex`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔

___
#  [A Lot of Examples ](https://github.com/superkabuki/threefive_is_scte35/blob/main/examples)  |  [  Tip of the Week  ](totw.md)  |   [  Cheap Tricks   ](cheaptricks.md)
___
# [ Issues ]
> I maintain threefive by myself, so mistakes are possible. if you find a bug, open an issue, and I will fix it.
> I don't respond well to demands unless you're paying me, but If you're cool, I'll be cool.   
___
# [ Documentation ]
#### Need to inject SCTE-35 into HLS?  [X9k3.](https://github.com/superkabuki/x9k3)
* [__web based SCTE-35 tools__](#web) - threefive and friends over http. 
* [__install__](#install)
* [__quick start__](quickstart.md)
* ___SCTE-35 on the command line___   
	* [ __the threefive cli tool__](#-cli-) _If you work with SCTE-35, this is as cool as it gets.  
* __other included tools__
    * [__scte35bump__](#scte35bump) _adjust SCTE-35 PTS in MPEGTS streams_ 
    * [__scte35fix__](#scte35fix)  _ffmpeg changes scte-35 streams into bin data, scte35fix changes them back._
	* [__scte35inject__](scte35inject.md) _scte35inject inject scte-35 into mpegts._
  	* [__gums__](#gums) _gums is a  multicast sender(server) for video_ 
* __the threefive library__ _cool code for the cool kids_.
 	* [__Using the threefive.Cue class__](lib.md) 
	* [__Using the threefive library__](#-using-the-library-) _decode SCTE-35 with less than ten lines of code_
 	* * [threefive __Classes__](#classes) _threefive is OO, made to subclass_
		* [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) _this class you'll use often_ 
		* [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) _this is the class for parsing MPEGTS_
* [SCTE-35 __Sidecar Files__](https://github.com/superkabuki/SCTE-35_Sidecar_Files) _threefive supports SCTE-35 sidecar files_
* [SCTE-35 __HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) _parse SCTE-35 in HLS__
* [SCTE-35 __XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) _threefive can parse and encode SCTE-35 xml_
* [__Encode__ SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) _threefive can encode SCTE-35 in every SCTE-35 format_
* [Make your __threefive__ script an executable with __cython__](cython.md) _threefive is compatible with all python tools_
</samp>

####  [Install]
* __threefive__ is curretnly tested on python-3.11, python-3.14, python-3.14t, pypy-7.3.11 and pypy-7.3.22

* __threefive__ is some of the __fastest code__ you'll see on __python3__. 
* __python3 via pip__
```rebol
python3 -mpip install threefive
```

* __threefive__ runs __five times faster on pypy3__,
* __threefive on pypy3__ can parse __mpegts__ at __over 1.5 GigaBytes__ a second, __single-threaded__.
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
#### [⇧](#-documentation-)
___

## [ CLI ]
* The threefive cli tool parses these SCTE-35 formats.  
  * Base64
  * Hex
  * HLS
  * Integers
  * JSON
  * MPEGTS
  * XML
  * XMLBinary.

* Formats are auto-detected.
___

* __Parse SCTE-35 Cues__ 
  *  __SCTE-35 Inputs:__  base64, hex, int, JSON,int,xml,and xmlbin.
  *  __SCTE-35 Outputs:__ base64, bytes, hex, int,JSON, xml, and xmlbin.
  *  __Any Input can be used with Any Output__
  *  The __default output__ is JSON

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

* __Parse SCTE-35 from HLS__  
```awk
threefive https://example.com/master.m3u8
```
___

* __Parse SCTE-35 from MPEGTS__
	* SCTE-35 can be parsed from MPEGTS over a variety of protocols.
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


#### [⇧](#-documentation-)

* [__Additional functionality__]
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

#### [⇧](#-documentation-)


##### Other tools
threefive also comes with: 
##### scte35bump 

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

##### [⇧](#-documentation-)

##### gums
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

#### [⇧](#-documentation-)

#### HLS

* parse HLS for SCTE-35. Supports all HLS SCTE-35 tags.

```js
$ threefive hls help
```
```smalltalk

[ Input ]

A m3u8 URI as input.

[what is supported]

    M3U8 formats: master, rendition
    Segment types: AAC, AC3, MPEGTS
    Video codecs: mpeg2, h.264, h.265
	Audio codecs: mpeg2, aac, ac3, mp3
    Protocols: File, Http(s), Multicast, SRT, Stdin, UDP
    Encryption: AES-128 (automatic)

[ SCTE-35 ]

  SCTE-35 Embedded Cues as well as all SCTE-35 HLS Tags can be parsed.

  [ Supported HLS Tags ]

	* #EXT-OATCLS-SCTE35
    * #EXT-X-CUE-OUT-CONT
    * #EXT-X-DATERANGE
    * #EXT-X-SCTE35
    * #EXT-X-CUE-IN
    * #EXT-X-CUE-OUT

[ SCTE-35 Parsing Profiles ]

    SCTE-35 parsing can be fine tuned by setting a parsing profile.

    running the command:  threefive hls profile

    will generate a default profile and write a file named hls.profile
    in the current working directory.

    a@fu:~$ cat hls.profile

    expand_cues = False
    parse_segments = False
    parse_manifests = True
    hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,
    #EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
    command_types = 0x6,0x5
    descriptor_tags = 0x2
    starts = 0x22,0x30,0x32,0x34,0x36,0x44,0x46

    ( Integers are show in hex (base 16),
      base 10 unsigned integers can also be used in .35rc )

    * expand_cues:       set to True to show cues fully expanded as JSON
    * parse_segments:    set to true to enable parsing SCTE-35 from MPEGTS.
    * parse_manifests:   set to true to parse the m3u8 file for SCTE-35 HLS Tags.
    * hls_tags:          set which SCTE-35 HLS Tags to parse.
    * command_types:     set which Splice Commands to parse.
    * descriptor_tags:   set which Splice Descriptor Tags to parse.
    * starts:            set which Segmentation Type IDs to use to start breaks.

    Edit the file as needed and then run threefive hls.

[ Profile Formatting Rules ]

    * Values do not need to be quoted.
    * Multiple values are separated by a commas.
    * No partial line comments. Comments must be on a separate lines.
    * Comments can be started with a # or //
    * Integers can be base 10 or base 16

[ Output Files ]
	scte35 hls creates a few output files.

	* Profile rules applied to the output:

		* hls.m3u8  - live playable rewrite of the m3u8 with the profile SCTE-35 rules.
        * hls.sidecar - list of ( pts, HLS SCTE-35 tag ) pairs

	* Profile rules not applied to the output:

		* hlsflat.m3u8  - hls live streams are flattened out into a vod playlist.
                     When the live m3u8  first loads, every line is written to hlsflat.m3u8
                     Wnen a live m3u8 is reloaded, everything except the headers
                    is appended to hlsflat.m3u8. This give you a VOD style m3u8
                    so you can fast forward or rewind while playing.
                    GREAT for debugging SCTE-35 live hls.

[ Cool Features ]

    * threefive hls can resume when started in the middle of an ad break.

            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067

[ Example Usage ]

	* Show this help:   scte35hls help

	* Generate a new hls.profile:   scte35hls profile

	* parse an m3u8:    scte35hls  https://example.com/out/master.m3u8


```

#### [⇧](#-documentation-)

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

#### [⇧](#-documentation-)

## [ Using the library ]
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

#### [⇧](#-documentation-)

#### [web]
* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) __hosted on my server iodisco.com__
* Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ Go, Wasm and Super Karate Death Car](https://bigcorp.ltd/gowasm) __hosted om my server bigcorp.ltd__
*  Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ threefive.js,javascript, and a little sed](https://bigcorp.ltd/bread) just to keep things interesting. __hosted om my server bigcorp.ltd__
* [ SCTE-35 __Online Parser__ powered by threefive](http://www.domus1938.com/scte35parser) _another online parser powered by threefive_ not hosted on my servers.
* [SCTE-35 __As a Service__](sassy.md) _if you can make an http request, you can parse SCTE-35, no install needed._
__hosted on my server iodisco.com__
___

#### [⇧](#-documentation-)

#### [XML]
* [XML](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) __New__! _updated 05/01/2025_

#### [HLS]
* [Advanced Parsing of SCTE-35 in HLS with threefive](https://github.com/superkabuki/threefive/blob/main/hls.md) All HLS SCTE-35 tags, Sidecar Files, AAC ID3 Header Timestamps, SCTE-35 filters... Who loves you baby?

 #### [⇧](#-documentation-)
 
####  [Classes]
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

#### [⇧](#-documentation-)

#### [threefive now supports SRT]

* _( You have to unmute the audio )_

https://github.com/user-attachments/assets/a323ea90-867f-480f-a55f-e9339263e511

<BR> 

* [more SRT and threefive info](srt.md)


* _checkout [SRTfu](https://github.com/superkabuki/srtfu)_

___

#### [⇧](#-documentation-)

##### [more]

* [Encode SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) Some encoding code examples. 
___

# [⇧](#-documentation-)
