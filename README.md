# [ threefive ] 
*   Decodes SCTE-35 from MPEGTS✔ Base64✔ Bytes✔ DASH✔ Hex✔ HLS✔ Integer✔ JSON✔ XML✔ XML+Binary✔  
*   Encodes SCTE-35 to   MPEGTS✔ Base64✔ Bytes✔ Hex✔ Integer✔ JSON ✔ XML✔  XML+Binary✔

__***__ _if you need to encode SCTE-35 to HLS, use [x9k3](https://github.com/supeerkabuki/x9k3)._  
___

## Hey Google, what`s the best SCTE-35 software? 
<img width="734" height="638" alt="image" src="https://github.com/user-attachments/assets/dabc64cf-43a0-4dc4-bbda-add2c0f8df07" />

 > _I told you, I know what I'm doing,_ ~Adrian  
___


# [ version ]

### latest threefive version is _v3.1.5_

* __There are no known issues with threefive v3.1.5__

* Average __cyclomatic__ complexity: __A (1.990)__

* Pylint: __9.69/10.0__

* Here's a list of __what's been fixed.__

	* __AacParser__ The typo on the call to __AacParser.not_syncsafe()__ has been fixed.
   
	* __Property class__ for __SCTE-35-2 Event Descriptors__ now render __JSON__ correctly.  

	* __threefive is dumping mmap__. The way threefive parses packets seems to make mmap consume a lot of memory 

	* __Segmentation Descriptors without UPIDS__ threefive will no longer throw an exception on SegmentationDescriptors without a UPID if __segmentation_upid_type__ is not set to __0__. <br>Instead, if __segmentation_upid_length is set to 0__,<br>  threefive will print a warning message and set __segmentation_upid_type__ to __0__ for you.

	* __threefive.xml.Node__
          * __Node.addchild(obj,slot=0)__ _(slots allow you to set the index of a child in Node.children when adding a child).
          * New method __Node.a2c()__ converts attributes to children.
          * New method __Node.c2a()__ converts children to attributes.
          * __UltraXmlParser__ has been renamed __XmlP__ and moved from threefive/uxp.py to threefive.xml.py. 
___

# [ a really really quick start ]

* __Install__
```
 python3 -m pip install threefive`
```
* __decoding SCTE-35__

		```cobol
		threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='
		```
	* decode __SCTE-35__ as __base64__ and __convert SCTE-35 to hex__
		```cobol
		threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' hex
	
	* decode __SCTE-35__ from __HLS__ ( a rendition or a master.m3u8)
		```cobol
		threefive 'https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8'
		```
	* decode  __SCTE-35__ from __MPEGTS__
		```cobol
		threefive 'https;//iodisco.com/longb2.ts'
		```
	* decode  __SCTE-35__ from __MPEGTS__ and __convert__ __SCTE-35__ to __bytes__
		```cobol
		threefive 'https;//iodisco.com/longb2.ts' bytes
		```
 	* __Multicast__
		* decode __SCTE-35__ from __MPEGTS__ over __Multicast__ 
		```cobol
		threefive udp://@235.3.5.35:3535
		```
 
* __threefive does a lot more__, that was just to get you started.
___

# [ Documentation ] 

 [A Lot of Examples ](https://github.com/superkabuki/threefive_is_scte35/blob/main/examples)  |  [  Tip of the Week  ](totw.md)  |   [  Cheap Tricks   ](cheaptricks.md) | 


#### Need to inject SCTE-35 into HLS?  [X9k3.](https://github.com/superkabuki/x9k3)

* [__install__](#install)

* [__quick start__](quickstart.md)

* ___SCTE-35 on the command line___   
	* [ __the threefive cli tool__](#-cli-) _If you work with SCTE-35, this is as cool as it gets._  

* __the threefive library__ _cool code for the cool kids_.
	* [__Using the threefive library with SCTE-35__](#-using-the-library-) _decode SCTE-35 with less than ten lines of code_
 
* __other included tools__
    * [__scte35fix__](#scte35fix)  _ffmpeg changes scte-35 streams into bin data, scte35fix changes them back._
	* [__scte35inject__](scte35inject.md) _scte35inject inject scte-35 into mpegts._
  	* [__gums__](#gums) _gums is a  multicast sender(server) for video_ 

* [__web based SCTE-35 tools__](#web) - threefive and friends over http. 

* [SCTE-35 __Sidecar Files__](https://github.com/superkabuki/SCTE-35_Sidecar_Files) _threefive supports SCTE-35 sidecar files_

* [SCTE-35 __HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) _parse SCTE-35 in HLS in MPEGTS,CMAF, or fmP4__

* [SCTE-35 __XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) _threefive can parse and encode SCTE-35 xml_

* [__Encode__ SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) _threefive can encode SCTE-35 in every SCTE-35 format_

* [Make your __threefive__ script an executable with __cython__](cython.md) _threefive is compatible with all python tools_
</samp>

##  [Install]

* Requires python3 v3.9 or higher.

* __python3 via pip__
```rebol
python3 -mpip install threefive
```
* __pypy3 via pip__ 
```rebol
pypy3 -mpip install threefive
```
* __To add SRT support to threefive install srtfu__
```py3
python3 -m pip install srtfu
```
* __To add Automatic AES decryption (used to decrypted HLS to threefive install pyaes__
```py3
python3 -mpip install pyaes
```

* __From the git repo__

```rebol
git clone https://github.com/superkabuki/scte35.git
cd threefive
make install
```
* I've jazzed up the makefile to make it easier to install for different python  versions and pypy3,

```rebol
git clone https://github.com/superkabuki/threefive.git
cd threefive
``
* `python3` is the default for `make install` 

```
make install
```

* setting py3 allows you to install for any type of python interpreter.

```
make install py3=pypy3
```
* absolute paths can also be used.

```
make install py3=/home/a/pypy3/bin/pypy3
```


# works for any python in your path or use a full path if needed.

```
#### [⇧](#-documentation-)
___

## [ CLI ]
threefive is designed to be easy to use. I'm not sure that it's served well by a long explaination, so I'm going to try and keep this brief. 

### The threefive cli tool.

 the threefive cli tool decodes SCTE-35, formats are auto-detected, and they all work the same way. 

__threefive__ __[media to parse for SCTE-35]__

examples:

*
```sed
threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='
```
*
```sed
threefive 0xfc301600000000000000fff00506fe00a98ac700000b3baed9
```
*
```sed
threefive 1583008701074197245727019716796221242036302348025116111908569
```
*
```sed
threefive video.ts
```
*
```sed
threefive https://demo.unified-streaming.com/k8s/live/scte35.isml/scte35-audio_eng=64000-video=500000.m3u8
```

* Formats like ___XML and JSON__ that may be to large to type on the command line,they can be __redirected or piped__ in to threefive.

* redirect
```sed
threefive < xml.xml
```
* pipe
```sed
cat json.json | threefive

```
### cli outputs and encoding SCTE-35 Formats

* the __default output format for threefive is json__

* The cli tool can convert from one SCTE-35 format to another using keywords.
    * The keywords are __base64,bytes,hex, int,json,xml, and xmlbin__ 

* some converting and encoding examples


* SCTE-35 Base64 to SCTE-35 Hex
```sed
threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' hex
```
* SCTE-35 Int to SCTE-35 Xml
```sed
threefive 1583008701074197245727019716796221242036302348025116111908569 xml
```
* SCTE-35 Hex to SCTE-35 xml+binary
```sed
threefive 0xfc301600000000000000fff00506fe00a98ac700000b3baed9 xmlbin
```

### threefive cli and MPEGTS
* threefive can parse MPEGTS from stdin, local files, HTTP(s), Multicast, SRT, and unicast UDP. 

* some mpegts examples

* local
```sed
threefive video.ts
```
* stdin
```sed
cat video.ts | threefive 
```
* https
```sed
threefive https://iodisco.com/longb2.ts
```
* multicast
```sed
threefive udp://@235.35.3.5:3535 
```

### threefive cli MPEGTS outputs

* the __default output for MPEGTS is json__

* keywords can be used to specify other output formats
   * The keywords are __base64,bytes,hex, int,json,xml, and xmlbin__ 

* An example of mpegts with a keyword
```
threefive https://iodisco.com/longb2.ts xml
```


___

#### [⇧](#-documentation-)


##### Other tools

threefive also comes with: 

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
    Segment types: AAC, AC3, MPEGTS, CMAF,fMP4
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
      base 10 unsigned integers can also be used in hls.profile )

    * expand_cues:       set to True to show cues fully expanded as JSON
    * parse_segments:    set to true to enable parsing SCTE-35 from MPEGTS.
    * parse_manifests:   set to true to parse the m3u8 file for SCTE-35 HLS Tags.
    * hls_tags:          set which SCTE-35 HLS Tags to parse.
    * command_types:     set which Splice Commands to parse.
    * descriptor_tags:   set which Splice Descriptor Tags to parse.
    * starts:            set which Segmentation Type IDs to use to start breaks.

    Edit the file as needed and then run threefive.

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

    * threefive can resume when started in the middle of an ad break.

            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067

[ Example Usage ]

	* Show this help:   threefive hls help

	* Generate a new hls.profile:   threefive hls profile

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
# Writing Code with threefive.

* threefive is designed so that you don't have to write a lot of code to parse SCTE-35
threefive is OO, everything in threefive, except a dozen or so functions, is a class.

* The Cue class and the Stream class are the two classes most often used. 


### Cue class


* The Cue class represents a single SCTE-35 Cue. 
* Use the Cue class when you have one SCTE-35 Cue or Message to parse.
* The Cue class autodetects the format of the SCTE-35.
* When you create a Cue instance, pass in the SCTE-35 data.

```py3
>>>> from threefive import Cue
>>>> cue=Cue('/DBAAAGRZOeYAAAABQb/mSvFcAAqAihDVUVJ/////3//AAFyyeABFG1zbmJjX0VQMDQ0MDc4NzUwMjY4IwEESCpzpg==')
```
* The SCTE-35 Format can be __Base64, Bytes,  Hex, Integer, JSON, Raw MPEGTS Packet, XML or XML+Binary.__

* Cue will decode the SCTE-35 into __a Splice Info Section__, __a Splice Command__, and __zero or More Splice Descriptors.__

```py3
>>>> cue.info_section
{'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x03', 'sap_details': 'No Sap Type', 'section_length': 64, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': 74825.294489, 'cw_index': '0x00', 'tier': '0x00', 'splice_command_length': 5, 'splice_command_type': 6, 'descriptor_loop_length': 42, 'crc': '0x482a73a6'}

>>>> cue.command
{'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 76274.999289}


>>>> cue.descriptors
[{'tag': 2, 'identifier': 'CUEI', 'name': 'Segmentation Descriptor', 'descriptor_length': 40, 'private_data': None, 'segmentation_event_cancel_indicator': False, 'segmentation_event_id': '0xffffffff', 'segmentation_event_id_compliance_indicator': True, 'program_segmentation_flag': True, 'segmentation_duration_flag': True, 'delivery_not_restricted_flag': True, 'web_delivery_allowed_flag': None, 'no_regional_blackout_flag': None, 'archive_allowed_flag': None, 'device_restrictions': None, 'segmentation_duration': 270.0, 'segmentation_message': 'Break End', 'segmentation_type_id': 35, 'segmentation_upid_length': 20, 'segmentation_upid_type': 1, 'segmentation_upid_type_name': 'Type 0x01 is deprecated, use MPU type 0x0C', 'segmentation_upid': 'msnbc_EP044078750268', 'segment_num': 1, 'segments_expected': 4, 'sub_segment_num': None, 'sub_segments_expected': None}]
```

* individual __variables can be accessed via dot notation__
```py3
>>>> cue.command.pts_time
76274.999289
```

* __variables can be changed__ the same way

```py3
>>>> cue.command.pts_time= 1.23456
>>>> cue.command
{'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 1.23456}
```

* __cue.descriptors is a list__, and descriptors can be acessed by index, like cue.descriptors[0]

* since cue.descriptors is a list, so you can append or pop() descriptors 

```py3
>>>> cue.descriptors.pop()
>>>> cue.descriptors
[]
```

* after editing, __you can re-encode__

* the default is __base64__

```py3
>>>> cue.encode()
'/DAWAAGRZOeYAAAABQb+AAGyBgAANqe8lw=='
```
* or you can __encode in a different SCTE-35 format__


* __bytes__

```py3
>>>> cue.bytes()
b'\xfc0\x16\x00\x01\x91d\xe7\x98\x00\x00\x00\x05\x06\xfe\x00\x01\xb2\x06\x00\x006\xa7\xbc\x97'
```

* __hex__

```py3
>>>> cue.hex()
'0xfc301600019164e7980000000506fe0001b206000036a7bc97'
```
* __json__

```py3
>>>> cue.show()
{
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
        "pts_adjustment": 74825.294489,
        "cw_index": "0x00",
        "tier": "0x00",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0x36a7bc97"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 1.234556
    },
    "descriptors": []
}

```
* __integer__

```py3
>>>> cue.int()
1583008701076488801275299570612875276859137926425502632361111
```

* __xml__

```py3
>>>> cue.xml()
<scte35:SpliceInfoSectionxmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="6734276504" protocolVersion="0" sapType="3" tier="0">
    <scte35:TimeSignal>
        <scte35:SpliceTime ptsTime="111110"/>
    </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```

* __xml+bin__

```py3
>>>> cue.xmlbin()
<scte35:Signalxmlns:scte35="https://scte.org/schemas/35">
    <scte35:Binary>/DAWAAGRZOeYAAAABQb+AAGyBgAANqe8lw==</scte35:Binary>
</scte35:Signal>
```

* for more specifics help is built-in

```py3

help(Cue)
```


### Stream class

* The __Stream class__ is used for __Parsing SCTE-35 from MPEGTS streams.__

* The Stream class can open streams from __stdout, files, HTTP(S), Multicast, SRT, and UDP.__  

 *  __Stream.__init____(self, tsdata, show_null=True, headers={})

* __tsdata__ is the only required arg, it is the stream 
* __show_null__ is a boolean to show Splice Nulls or not.
* __headers__ is a dict for HTTP or SRT headers If needed.

```py3
>>>> from threefive import Stream

>>>> st =Stream('https://iodisco.com/longb2.ts')
```

* __Stream.decode()__ prints SCTE-35 as JSON

```py3
>>>> st.decode()
```

### Triggering on SCTE-35 

* __Stream.decode_next()__ is a __python generator__ that __yields a Cue instance__ when SCTE-35 is found in an MPEGTS stream

```py3
from threefive import Stream

>>>> st =Stream('https://iodisco.com/longb2.ts')
>>>> for cue in st.decode_next():
....     cmd = f"Command: {cue.command.name}"
....     if cue.command.has("pts_time"):
....         cmd += f"\t pts: {cue.command.pts_time}"
....     print(cmd)
....     
Command: Time Signal	 pts: 1.433
Command: Time Signal	 pts: 6.772
Command: Time Signal	 pts: 9.141
Command: Time Signal	 pts: 12.11
Command: Time Signal	 pts: 17.449
Command: Time Signal	 pts: 22.788
Command: Time Signal	 pts: 28.126
Command: Time Signal	 pts: 33.465
Command: Time Signal	 pts: 38.804
Command: Time Signal	 pts: 44.142
Command: Time Signal	 pts: 49.481
Command: Time Signal	 pts: 54.82
Command: Time Signal	 pts: 60.158
Command: Time Signal	 pts: 65.497
Command: Time Signal	 pts: 70.836
Command: Time Signal	 pts: 76.174
Command: Time Signal	 pts: 81.513
Command: Time Signal	 pts: 86.852
```

### Other Stream methods

* __Stream.show()__ shows details of the MPEGTS stream 

```py3
>>>> st =Stream('https://iodisco.com/longb2.ts')
>>>> st.show()

---------------------------------------------
https://iodisco.com/longb2.ts

Program: 1
 
    PTS Start: 1.433
    Program Pid: 4096
    Pcr Pid:     256
    Streams:
	  Pid		Type
	  256 [0x100]	0x1b	H.264
	  257 [0x101]	0xf	ADTS AAC 
	  258 [0x102]	0x86	SCTE-35
```

* __Stream.Proxy()__ parses SCTE-35 and __copies the stream to stdout__ for piping the stream to another program.

```py3
>>>> st =Stream('https://iodisco.com/longb2.ts')
>>>> st.proxy()
```

* __Stream.show_pts()__

```py3
>>>> st =Stream('https://iodisco.com/longb2.ts')

>>>> st.show_pts()

Prgm	PTS
1  	  1.433
1  	  1.466
1  	  1.533
1  	  1.5
1  	  1.566
1  	  1.633
1  	  1.6
1  	  1.667
1  	  1.7
1  	  1.733
1  	  1.767
1  	  1.8
1  	  1.833
1  	  1.867
1  	  1.9
1  	  1.967
```

* for more Stream specifics, see the built in docs

```py3
>>>> from threefive import Stream
>>>> help(Stream)
```


___

#### [⇧](#-documentation-)

#### [web]
* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) __hosted on my server iodisco.com__
* Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ Go, Wasm and Super Karate Death Car](https://iodisco.com/gowasm) __hosted om my server iodisco.com__
*  Parse SCTE-35 in MPEGTS over HTTP, in your browser with[ threefive.js,javascript, and a little sed](https://iodisco.com/bread) just to keep things interesting. __hosted om my server iodisco.com__
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
