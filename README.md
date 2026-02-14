#### Need to inject SCTE-35 into HLS?  [X9k3.](https://github.com/superkabuki/x9k3) 


# [ threefive ]
## https://github.com/superkabuki/threefive

### threefive is the industry leading SCTE-35 tool. 

*   __Decodes SCTE-35__ from `MPEGTS`✔ `Base64`✔ `Bytes`✔ `DASH`✔ `Hex` ✔ `HLS`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔
  
*   __Encodes SCTE-35__ to `MPEGTS`✔ `Base64`✔ `Bytes`✔ `Hex`✔ `Integers`✔ `JSON`✔ `XML`✔ `XML+Binary`✔

*   __Injects SCTE-35 Packets__ into `MPEGTS`✔.

*   __Network support__ for `HTTP(s)`✔ `Multicast`✔ `UDP`✔ `SRT`✔

*   __Built-in__ `Multicast Server`✔

*   __Automatic__ `AES decryption`✔

___


### [ News ]
   
* __Python3 vs. Pypy3__ [__parsing SCTE35 with threefive__](https://github.com/superkabuki/threefive_is_scte35#python3-vs-pypy3-running-threefive) (watch the cool video)
 
* __threefive now supports__ [__Secure Reliable Transport__](https://github.com/superkabuki/threefive_is_scte35/blob/main/README.md#threefive-now-supports-srt)

* [__threefive does Multicast very well__](#-threefive-streams-multicast-its-easy-), both as a sender and receiver.  
___

## [ Latest version is  v3.0.73 ]
* [__Super low cyclomatic complexity score__](cyclomatic.md)
* __Cli tool__ new features
	* New  __bump__ keyword to adjust SCTE-35 PTS. Supports positive and negative adjustments.
    * New __rt__  keyword parses SCTE-35, writes a SCTE-35 sidecar file, and outputs the MPEGTS stream to stdout at realtime speed.   
* __threefive hls__ can now handle __SCTE-35 as Integer values in HLS tags__
* All __ansi color codes striped__ when output is not a tty._
*  __threefive.Cue.xmlbin()__ now returns a __threefive.xml.Node instance like__ __threefive.Cue.xml()__. 
* __threefive.Stream__ has a new method __threefive.Stream.rt(func=show_cue)__  that parses SCTE-35 and proxies the stream to stdout at realtime speed.
* __threefive mcast__ now throttles Multicast output to realtime speed.
* __threefive packets__ and __threefive pts__ now works with __SRT__.

___

## [Fun Facts]
* threefive is single threaded.
* threefive has more left shifts than multiplication operations.
* threefive doesn't have a single lambda call.
___

##  [Examples]
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

####  [__More Examples__](https://github.com/superkabuki/threefive/tree/main/examples)


# [ Documentation ]

* __use threefive on the web__
	* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) hosted on my server_
	* [ SCTE-35 __Online Parser__ powered by threefive](http://www.domus1938.com/scte35parser) _another online parser powered by threefive_
	* [SCTE-35 __As a Service__](sassy.md) _if you can make an http request, you can parse SCTE-35, no install needed._

	
* [__install__](#install) 
	* [SCTE-35 Decoding __Quick Start__ ](#quick-start) _threefive makes decoding SCTE-35 fast and easy_
	* [SCTE-35 __Examples__](https://github.com/superkabuki/threefive/tree/main/examples) _examples of all kinds of SCTE-35 stuff_

* __Command line__
	* [SCTE-35 __Cli__](#-the-cli-tool-) _decode SCTE-35 on the command line_

* __Library__
 	* [__Using the threefive.Cue class__](https://github.com/superkabuki/threefive/blob/main/lib.md) 
	* [__Using the threefive library__](#using-the-library) _decode SCTE-35 with less than ten lines of code_
 	* * [threefive __Classes__](#classes) _threefive is OO, made to subclass_
		* [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) _this class you'll use often_ 
		* [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) _this is the class for parsing MPEGTS_

* [Use __threefive to stream Multicast__](#-threefive-streams-multicast-its-easy-) _threefive is a multicast client and server_

* [SCTE-35 __Sidecar Files__](https://github.com/superkabuki/SCTE-35_Sidecar_Files) _threefive supports SCTE-35 sidecar files_

* [__SuperKabuki__ SCTE-35 MPEGTS __Packet Injection__](inject.md) _inject SCTE-35 into MPEGTS streams_ 

* [SCTE-35 __HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) _parse SCTE-35 in HLS__
* [SCTE-35 __XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) _threefive can parse and encode SCTE-35 xml_

* [__Encode__ SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) _threefive can encode SCTE-35 in every SCTE-35 format_

* [Make your __threefive__ script an executable with __cython__](cython.md) _threefive is compatible with all python tools_
</samp>


##  [Install]
* python3 via pip
```rebol
python3 -mpip install threefive
```
* pypy3 
```rebol
pypy3 -mpip install threefive
```
* from the git repo
```rebol
git clone https://github.com/superkabuki/scte35.git
cd threefive
make install
```
___


## [Quick Start] 


* Most of the stuff in threefive all works the same way.

### [cli tool]

* The default action is to read a input and write a SCTE-35 output.

  *  __Inputs:__  mpegts, base64, hex, json,and xml, and xmlbin.

  *  __Outputs:__ base64, bytes, hex, int, json, xml, and xmlbin.

  *  __Sources:__ SCTE35 can read from  strings, files, stdin, http(s), multicast,srt and udp.

|Input     |Output     | How to use                                              |
|----------|-----------|---------------------------------------------------------|
|__mpegts__|__base64__ | threefive https://example.com/video.ts  __base64__      |
|          |           |                                                         |
|__base64__|__hex__    | threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' __hex__|
|          |           |                               |                     |
|__xmlbin__|__int__    | threefive   < xmlbin.xml __int__                        |
|          |           |                                                         |
|__xml__   |__json__   | threefive   < xml.xml                                   |
|          |           |                                                         |
|__mpegts__|__xml+bin__| threefive video.ts __xmlbin__                           |
|          |   |   |                                                     |
|__json__  |__xml__    | threefive  < json.json  __xml__                         |
|          |           |                                                         |


* __Additional functionality__ in the threefive cli tool.

| Description                              | How To Use                                       |
|------------------------------------------|---------------------------------------------------------|
| Adjust __SCTE-35__ PTS values by seconds  | threefive __bump__ -i input.ts -o output.ts -b -37.45   |
|											|														|
| Parse HLS for __SCTE35__                 |threefive __hls__ https://example.com/master.m3u8        |
|                                          |                                                         |
| Inject __SCTE35__ packets                |threefive __inject__ -i in.video -s sidecar.txt -o out.ts|
|                                          |                                                         |
| Show raw __SCTE35__ packets              |threefive __packets__ udp://@235.35.3.5:3535             |
|											|														| 
| Copy MPEGTS stream to stdout at realtime speed| threefive __rt__ input.ts | mplayer -				|
|                                          |                                                         |
| Create __SCTE35__ sidecar file           |threefive __sidecar__ video.ts                           |
|                                          |                                                         |
|Fix __SCTE-35__ data mangled by __ffmpeg__| threefive __sixfix__ video.ts                           |
|                                          |                                                         |
| Show streams in mpegts stream            | threefive __show__ https://example.com/video.ts         |
|                                          |                                                         |
| Show __iframes__ in mpegts stream        |threefive __iframes__ srt://10.10.1.3:9000               |
|                                          |                                                         |
| Show __PTS__ values from mpegts stream   | threefive __pts__ udp://192.168.1.10:9000               |
|                                          |                                                         |
|__Proxy__ the __mpegts__ stream to stdout |threefive __proxy__ https://wexample.com/video.ts        |
|                                          |                                                         |
| __Multicast__ anything                   |threefive __mcast__ some.file                            |
|                                          |                                                         |

___

## [XML]
* [XML](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) __New__! _updated 05/01/2025_
## [Cli]
* [SCTE-35 Cli Super Tool](#the-cli-tool) Encodes, Decodes, and Recodes. This is pretty cool, it does SCTE-35 seven different ways.
     * The cli tool comes with builtin documentation just type `threefive help`
## [HLS]
* [Advanced Parsing of SCTE-35 in HLS with threefive](https://github.com/superkabuki/threefive/blob/main/hls.md) All HLS SCTE-35 tags, Sidecar Files, AAC ID3 Header Timestamps, SCTE-35 filters... Who loves you baby?

##  [MPEGTS Packet Injection]
* [The SuperKabuki MPEGTS Packet Injection Engine in the Cli](inject.md)

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
* [Parse __SCTE-35__ in __hls__](#hls)
* [Display __MPEGTS__ __iframes__](#iframes)
* [Display raw __SCTE-35 packets__ from __video streams__](#packets)
* [__Repair SCTE-35 streams__ changed to __bin data__ by __ffmpeg__](#sixfix)

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
|  __HLS__          |                                                                                                    `threefive hls https://example.com/master.m3u8`|
|               |                                                                                                                                                    |


#### Outputs
* output type is determined by the key words __base64, bytes, hex, int, json, and xmlbin__.
* __json is the default__.
* __Any input (except HLS,) can be returned as any output__
  * examples __Base64 to Hex__ etc...) 


| Output Type | Cli Example         |
|-------------|----------------------------------------------------------|
|__Base 64__     |                                                                                                                                                                    `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  base64  `                                                                                                                                                                                                                                                                                                                                         |
| __Bytes__       |                                                                                 `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  bytes`                                                                                                                                                                                                                                                                                                                                                                                                                               |
| __Hex__         | `threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  hex`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| __Integer__     |                                                                                                                                                                                                                                                       `threefive '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  int`   |
| __JSON__        |                                                                                                                                                                                                                                                                                                              `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b json ` |
| __Xml+bin__     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `threefive 0xfc301600000000000000fff00506fed605225b0000b0b65f3b xmlbin   `      |`

#### `hls`
* parse hls manifests and segments for SCTE-35
```smalltalk
threefive hls https://example.com/master.m3u8
```
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
#### `sixfix`  
* Fix SCTE-35 data mangled by ffmpeg

```smalltalk
threefive sixfix video.ts
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


## [ threefive Streams Multicast, it's easy. ]
* The threefive cli has long been a Multicast Receiver( client )
* The cli now comes with a builtin Multicast Sender( server).
* It's optimized for MPEGTS (1316 byte Datagrams) but you can send any video or file.
* The defaults will work in most situations, you don't even have to set the address.
* threefive cli also supports UDP Unicast Streaming.

If you're tired of configuring strange kernel settings with sysctl trying to get multicast to work,<br> 
threefive multicast is written from scratch in raw sockets and autoconfigures most settings,<br> 
threefive adjusts the SO_RCVBUF, SO_SNDBUF, SO_REUSEADDR,SO_REUSEPORT,IP_MULTICAST_TTL and IP_MULTICAST_LOOP for you.<br>
all you really need to do is make sure multicast is enabled on the network device, threefive can handle the rest.<br>
```js
ip link set wlp2s0  multicast on

```

   
```js
a@fu:~$ threefive mcast help
usage: threefive mcast [-h] [-i INPUT] [-a ADDR] [-b BIND_ADDR] [-t TTL]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        like "/home/a/vid.ts" or "udp://@235.35.3.5:3535" or
                        "https://futzu.com/xaa.ts"
                        [default:sys.stdin.buffer]
  -a ADDR, --addr ADDR  Destination IP:Port [default:235.35.3.5:3535]
  -b BIND_ADDR, --bind_addr BIND_ADDR
                        Local IP to bind [default:0.0.0.0]
  -t TTL, --ttl TTL     Multicast TTL (1 - 255) [default:32]
a@fu:~$ 
```

* the video shows three streams being read and played from threefive's multicast, one stream is being converted to srt.
* the command
```sh
a@fu:~/scratch/threefive$ threefive mcast -i ~/mpegts/ms.ts 

```

https://github.com/user-attachments/assets/df95b8da-5ca6-4bf3-b029-c95204841e43

* __threefive mcast__ sends __1316 byte datagrams__. Here's `tcpdump multicast`output. 

<img width="1126" height="679" alt="image" src="https://github.com/user-attachments/assets/b29f33c7-d35c-42be-95fb-2c6e72d1ab9b" />

___


## [iodisco.com/scte35](https://iodisco.com/scte35)





 <svg width="100" height="100">
  <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
</svg> 

 <img width="258" height="256" alt="image" src="https://github.com/user-attachments/assets/642cb803-9465-408e-bb6e-03549eb22d78" />

___
 [__Install__](#install) |[__SCTE-35 Cli__](#the-cli-tool) | [__SCTE-35 HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) | [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) | [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) | [__Online SCTE-35 Parser__](https://iodisco.com/scte35) | [__Encode SCTE-35__](https://github.com/superkabuki/threefive/blob/main/encode.md) | [__SCTE-35 Examples__](https://github.com/superkabuki/threefive/tree/main/examples)
 | [__SCTE-35 XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) | [__threefive runs Four Times Faster on pypy3__](https://pypy.org/) | [__SuperKabuki SCTE-35 MPEGTS Packet Injection__](inject.md)



<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="./">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />

  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

<li><a class="reference internal" href="#module-threefive.base">threefive.base module</a><ul>

<li><a class="reference internal" href="#threefive.base.SCTE35Base"><code class="docutils literal notranslate"><span class="pre">SCTE35Base</span></code></a><ul>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.ROLLOVER"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.ROLLOVER</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.as_90k"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.as_90k()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.as_hms"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.as_hms()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.as_ticks"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.as_ticks()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.fix_hex"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.fix_hex()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.get"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.get()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.has"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.has()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.idxsplit"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.idxsplit()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.json"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.json()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.kv_clean"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.kv_clean()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.load"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.load()</span></code></a></li>
<li><a class="reference internal" href="#threefive.base.SCTE35Base.show"><code class="docutils literal notranslate"><span class="pre">SCTE35Base.show()</span></code></a></li>
</ul>
</li>
</ul>
</li>



<li><a class="reference internal" href="#module-threefive.cue">threefive.cue module</a><ul>
<li><a class="reference internal" href="#threefive.cue.Cue"><code class="docutils literal notranslate"><span class="pre">Cue</span></code></a><ul>
<li><a class="reference internal" href="#threefive.cue.Cue.base64"><code class="docutils literal notranslate"><span class="pre">Cue.base64()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.bytes"><code class="docutils literal notranslate"><span class="pre">Cue.bytes()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.decode"><code class="docutils literal notranslate"><span class="pre">Cue.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.decode_info_section"><code class="docutils literal notranslate"><span class="pre">Cue.decode_info_section()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.encode"><code class="docutils literal notranslate"><span class="pre">Cue.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.encode_as_hex"><code class="docutils literal notranslate"><span class="pre">Cue.encode_as_hex()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.encode_as_int"><code class="docutils literal notranslate"><span class="pre">Cue.encode_as_int()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.fix_bad_b64"><code class="docutils literal notranslate"><span class="pre">Cue.fix_bad_b64()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.get"><code class="docutils literal notranslate"><span class="pre">Cue.get()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.get_descriptors"><code class="docutils literal notranslate"><span class="pre">Cue.get_descriptors()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.hex"><code class="docutils literal notranslate"><span class="pre">Cue.hex()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.int"><code class="docutils literal notranslate"><span class="pre">Cue.int()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.load"><code class="docutils literal notranslate"><span class="pre">Cue.load()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.xml"><code class="docutils literal notranslate"><span class="pre">Cue.xml()</span></code></a></li>
<li><a class="reference internal" href="#threefive.cue.Cue.xmlbin"><code class="docutils literal notranslate"><span class="pre">Cue.xmlbin()</span></code></a></li>
</ul>
</li>
</ul>
</li>
<li><a class="reference internal" href="#module-threefive.section">threefive.section module</a><ul>
<li><a class="reference internal" href="#threefive.section.SpliceInfoSection"><code class="docutils literal notranslate"><span class="pre">SpliceInfoSection</span></code></a><ul>
<li><a class="reference internal" href="#threefive.section.SpliceInfoSection.decode"><code class="docutils literal notranslate"><span class="pre">SpliceInfoSection.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.section.SpliceInfoSection.encode"><code class="docutils literal notranslate"><span class="pre">SpliceInfoSection.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.section.SpliceInfoSection.xml"><code class="docutils literal notranslate"><span class="pre">SpliceInfoSection.xml()</span></code></a></li>
</ul>
</li>
</ul>
</li>

<li><a class="reference internal" href="#module-threefive.commands">threefive.commands module</a><ul>

<li><a class="reference internal" href="#threefive.commands.SpliceCommand"><code class="docutils literal notranslate"><span class="pre">SpliceCommand</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.SpliceCommand.decode"><code class="docutils literal notranslate"><span class="pre">SpliceCommand.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.SpliceCommand.encode"><code class="docutils literal notranslate"><span class="pre">SpliceCommand.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.commands.SpliceInsert"><code class="docutils literal notranslate"><span class="pre">SpliceInsert</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.SpliceInsert.decode"><code class="docutils literal notranslate"><span class="pre">SpliceInsert.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.SpliceInsert.encode"><code class="docutils literal notranslate"><span class="pre">SpliceInsert.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.SpliceInsert.xml"><code class="docutils literal notranslate"><span class="pre">SpliceInsert.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.commands.SpliceNull"><code class="docutils literal notranslate"><span class="pre">SpliceNull</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.SpliceNull.xml"><code class="docutils literal notranslate"><span class="pre">SpliceNull.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.commands.TimeSignal"><code class="docutils literal notranslate"><span class="pre">TimeSignal</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.TimeSignal.decode"><code class="docutils literal notranslate"><span class="pre">TimeSignal.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.TimeSignal.encode"><code class="docutils literal notranslate"><span class="pre">TimeSignal.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.TimeSignal.xml"><code class="docutils literal notranslate"><span class="pre">TimeSignal.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.commands.BandwidthReservation"><code class="docutils literal notranslate"><span class="pre">BandwidthReservation</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.BandwidthReservation.xml"><code class="docutils literal notranslate"><span class="pre">BandwidthReservation.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.commands.PrivateCommand"><code class="docutils literal notranslate"><span class="pre">PrivateCommand</span></code></a><ul>
<li><a class="reference internal" href="#threefive.commands.PrivateCommand.decode"><code class="docutils literal notranslate"><span class="pre">PrivateCommand.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.PrivateCommand.encode"><code class="docutils literal notranslate"><span class="pre">PrivateCommand.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.commands.PrivateCommand.xml"><code class="docutils literal notranslate"><span class="pre">PrivateCommand.xml()</span></code></a></li>
</ul>
</li>
</ul>
</li>
<li><a class="reference internal" href="#module-threefive.descriptors">threefive.descriptors module</a><ul>
<li><a class="reference internal" href="#threefive.descriptors.SpliceDescriptor"><code class="docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.SpliceDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">SpliceDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SpliceDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">SpliceDescriptor.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SpliceDescriptor.parse_id"><code class="docutils literal notranslate"><span class="pre">SpliceDescriptor.parse_id()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SpliceDescriptor.parse_tag_and_len"><code class="docutils literal notranslate"><span class="pre">SpliceDescriptor.parse_tag_and_len()</span></code></a></li>
</ul>
</li>

<li><a class="reference internal" href="#threefive.descriptors.AvailDescriptor"><code class="docutils literal notranslate"><span class="pre">AvailDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.AvailDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">AvailDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.AvailDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">AvailDescriptor.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.AvailDescriptor.xml"><code class="docutils literal notranslate"><span class="pre">AvailDescriptor.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.descriptors.DVBDASDescriptor"><code class="docutils literal notranslate"><span class="pre">DVBDASDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.DVBDASDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">DVBDASDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.DVBDASDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">DVBDASDescriptor.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.descriptors.DtmfDescriptor"><code class="docutils literal notranslate"><span class="pre">DtmfDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.DtmfDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">DtmfDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.DtmfDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">DtmfDescriptor.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.DtmfDescriptor.xml"><code class="docutils literal notranslate"><span class="pre">DtmfDescriptor.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.descriptors.SegmentationDescriptor"><code class="docutils literal notranslate"><span class="pre">SegmentationDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.SegmentationDescriptor.SUB_SEG_TYPES"><code class="docutils literal notranslate"><span class="pre">SegmentationDescriptor.SUB_SEG_TYPES</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SegmentationDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">SegmentationDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SegmentationDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">SegmentationDescriptor.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.SegmentationDescriptor.xml"><code class="docutils literal notranslate"><span class="pre">SegmentationDescriptor.xml()</span></code></a></li>
</ul>
</li>

<li><a class="reference internal" href="#threefive.descriptors.TimeDescriptor"><code class="docutils literal notranslate"><span class="pre">TimeDescriptor</span></code></a><ul>
<li><a class="reference internal" href="#threefive.descriptors.TimeDescriptor.decode"><code class="docutils literal notranslate"><span class="pre">TimeDescriptor.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.TimeDescriptor.encode"><code class="docutils literal notranslate"><span class="pre">TimeDescriptor.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.descriptors.TimeDescriptor.xml"><code class="docutils literal notranslate"><span class="pre">TimeDescriptor.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.descriptors.splice_descriptor"><code class="docutils literal notranslate"><span class="pre">splice_descriptor()</span></code></a></li>
</ul>
</li>


<li><a class="reference internal" href="#module-threefive.upids">threefive.upids module</a><ul>
<li><a class="reference internal" href="#threefive.upids.AirId"><code class="docutils literal notranslate"><span class="pre">AirId</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.AirId.decode"><code class="docutils literal notranslate"><span class="pre">AirId.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.AirId.encode"><code class="docutils literal notranslate"><span class="pre">AirId.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Atsc"><code class="docutils literal notranslate"><span class="pre">Atsc</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Atsc.decode"><code class="docutils literal notranslate"><span class="pre">Atsc.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Atsc.encode"><code class="docutils literal notranslate"><span class="pre">Atsc.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Eidr"><code class="docutils literal notranslate"><span class="pre">Eidr</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Eidr.decode"><code class="docutils literal notranslate"><span class="pre">Eidr.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Eidr.encode"><code class="docutils literal notranslate"><span class="pre">Eidr.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Isan"><code class="docutils literal notranslate"><span class="pre">Isan</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Isan.decode"><code class="docutils literal notranslate"><span class="pre">Isan.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Isan.encode"><code class="docutils literal notranslate"><span class="pre">Isan.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Mid"><code class="docutils literal notranslate"><span class="pre">Mid</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Mid.decode"><code class="docutils literal notranslate"><span class="pre">Mid.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Mid.encode"><code class="docutils literal notranslate"><span class="pre">Mid.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Mid.xml"><code class="docutils literal notranslate"><span class="pre">Mid.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Mpu"><code class="docutils literal notranslate"><span class="pre">Mpu</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Mpu.decode"><code class="docutils literal notranslate"><span class="pre">Mpu.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Mpu.encode"><code class="docutils literal notranslate"><span class="pre">Mpu.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.NoUpid"><code class="docutils literal notranslate"><span class="pre">NoUpid</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.NoUpid.decode"><code class="docutils literal notranslate"><span class="pre">NoUpid.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.NoUpid.encode"><code class="docutils literal notranslate"><span class="pre">NoUpid.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Umid"><code class="docutils literal notranslate"><span class="pre">Umid</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Umid.decode"><code class="docutils literal notranslate"><span class="pre">Umid.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Umid.encode"><code class="docutils literal notranslate"><span class="pre">Umid.encode()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.Upid"><code class="docutils literal notranslate"><span class="pre">Upid</span></code></a><ul>
<li><a class="reference internal" href="#threefive.upids.Upid.decode"><code class="docutils literal notranslate"><span class="pre">Upid.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Upid.encode"><code class="docutils literal notranslate"><span class="pre">Upid.encode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Upid.redecode"><code class="docutils literal notranslate"><span class="pre">Upid.redecode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.upids.Upid.xml"><code class="docutils literal notranslate"><span class="pre">Upid.xml()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.upids.charset"><code class="docutils literal notranslate"><span class="pre">charset</span></code></a></li>
</ul>

</ul>
</li>

<li><a class="reference internal" href="#module-threefive.stream">threefive.stream module</a><ul>
<li><a class="reference internal" href="#threefive.stream.Based"><code class="docutils literal notranslate"><span class="pre">Based</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Maps"><code class="docutils literal notranslate"><span class="pre">Maps</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Pids"><code class="docutils literal notranslate"><span class="pre">Pids</span></code></a><ul>
<li><a class="reference internal" href="#threefive.stream.Pids.PAT_PID"><code class="docutils literal notranslate"><span class="pre">Pids.PAT_PID</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Pids.SDT_PID"><code class="docutils literal notranslate"><span class="pre">Pids.SDT_PID</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.stream.ProgramInfo"><code class="docutils literal notranslate"><span class="pre">ProgramInfo</span></code></a><ul>
<li><a class="reference internal" href="#threefive.stream.ProgramInfo.show"><code class="docutils literal notranslate"><span class="pre">ProgramInfo.show()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.stream.Stream"><code class="docutils literal notranslate"><span class="pre">Stream</span></code></a><ul>
<li><a class="reference internal" href="#threefive.stream.Stream.PACKET_SIZE"><code class="docutils literal notranslate"><span class="pre">Stream.PACKET_SIZE</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.PMT_TID"><code class="docutils literal notranslate"><span class="pre">Stream.PMT_TID</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.ROLLOVER"><code class="docutils literal notranslate"><span class="pre">Stream.ROLLOVER</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.ROLLOVER9K"><code class="docutils literal notranslate"><span class="pre">Stream.ROLLOVER9K</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.SCTE35_PES_START"><code class="docutils literal notranslate"><span class="pre">Stream.SCTE35_PES_START</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.SCTE35_TID"><code class="docutils literal notranslate"><span class="pre">Stream.SCTE35_TID</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.SDT_TID"><code class="docutils literal notranslate"><span class="pre">Stream.SDT_TID</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.SYNC_BYTE"><code class="docutils literal notranslate"><span class="pre">Stream.SYNC_BYTE</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.as_90k"><code class="docutils literal notranslate"><span class="pre">Stream.as_90k()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.decode"><code class="docutils literal notranslate"><span class="pre">Stream.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.decode_next"><code class="docutils literal notranslate"><span class="pre">Stream.decode_next()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.decode_pids"><code class="docutils literal notranslate"><span class="pre">Stream.decode_pids()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.decode_start_time"><code class="docutils literal notranslate"><span class="pre">Stream.decode_start_time()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.iter_pkts"><code class="docutils literal notranslate"><span class="pre">Stream.iter_pkts()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.mk_pts"><code class="docutils literal notranslate"><span class="pre">Stream.mk_pts()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.pid2pcr"><code class="docutils literal notranslate"><span class="pre">Stream.pid2pcr()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.pid2prgm"><code class="docutils literal notranslate"><span class="pre">Stream.pid2prgm()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.pid2pts"><code class="docutils literal notranslate"><span class="pre">Stream.pid2pts()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.proxy"><code class="docutils literal notranslate"><span class="pre">Stream.proxy()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.pts"><code class="docutils literal notranslate"><span class="pre">Stream.pts()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.rt"><code class="docutils literal notranslate"><span class="pre">Stream.rt()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.show"><code class="docutils literal notranslate"><span class="pre">Stream.show()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.show_pts"><code class="docutils literal notranslate"><span class="pre">Stream.show_pts()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.Stream.speed"><code class="docutils literal notranslate"><span class="pre">Stream.speed()</span></code></a></li>
</ul>
</li>
<li><a class="reference internal" href="#threefive.stream.no_op"><code class="docutils literal notranslate"><span class="pre">no_op()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.show_cue"><code class="docutils literal notranslate"><span class="pre">show_cue()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stream.show_cue_stderr"><code class="docutils literal notranslate"><span class="pre">show_cue_stderr()</span></code></a></li>
</ul>
</li>


</li>



<li><a class="reference internal" href="#module-threefive.segment">threefive.segment module</a><ul>
<li><a class="reference internal" href="#threefive.segment.Segment"><code class="docutils literal notranslate"><span class="pre">Segment</span></code></a><ul>
<li><a class="reference internal" href="#threefive.segment.Segment.decode"><code class="docutils literal notranslate"><span class="pre">Segment.decode()</span></code></a></li>
<li><a class="reference internal" href="#threefive.segment.Segment.show_cue"><code class="docutils literal notranslate"><span class="pre">Segment.show_cue()</span></code></a></li>
<li><a class="reference internal" href="#threefive.segment.Segment.shushed"><code class="docutils literal notranslate"><span class="pre">Segment.shushed()</span></code></a></li>
</ul>
</li>
</ul>
</li>

<li><a class="reference internal" href="#module-threefive.stuff">threefive.stuff module</a><ul>
<li><a class="reference internal" href="#threefive.stuff.badtype"><code class="docutils literal notranslate"><span class="pre">badtype()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.blue"><code class="docutils literal notranslate"><span class="pre">blue()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.clean"><code class="docutils literal notranslate"><span class="pre">clean()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.codec_detect"><code class="docutils literal notranslate"><span class="pre">codec_detect()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.isfloat"><code class="docutils literal notranslate"><span class="pre">isfloat()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.ishex"><code class="docutils literal notranslate"><span class="pre">ishex()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.isjson"><code class="docutils literal notranslate"><span class="pre">isjson()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.iso8601"><code class="docutils literal notranslate"><span class="pre">iso8601()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.isxml"><code class="docutils literal notranslate"><span class="pre">isxml()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.k_by_v"><code class="docutils literal notranslate"><span class="pre">k_by_v()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.no_ESC"><code class="docutils literal notranslate"><span class="pre">no_ESC()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.pif"><code class="docutils literal notranslate"><span class="pre">pif()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.print2"><code class="docutils literal notranslate"><span class="pre">print2()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.reblue"><code class="docutils literal notranslate"><span class="pre">reblue()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.red"><code class="docutils literal notranslate"><span class="pre">red()</span></code></a></li>
<li><a class="reference internal" href="#threefive.stuff.rmap"><code class="docutils literal notranslate"><span class="pre">rmap()</span></code></a></li>
</ul>
</li>

<li><a class="reference internal" href="#module-threefive">Module contents</a></li>
</ul>
</li>
</ul>
</div>
        </div>
      </div>
    </nav>

    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap"><nav class="wy-nav-top" aria-label="Mobile navigation menu" >
          <i data-toggle="wy-nav-top" class="fa fa-bars"></i>
          <a href="index.html">threefive</a>
      </nav>

      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="navigation" aria-label="Page navigation">
  <ul class="wy-breadcrumbs">
      <li><a href="index.html" class="icon icon-home" aria-label="Home"></a></li>
      <li class="breadcrumb-item active">threefive package</li>
      <li class="wy-breadcrumbs-aside">
            <a href="_sources/threefive.rst.txt" rel="nofollow"> View page source</a>
      </li>
  </ul>
  <hr/>
</div>
          <div role="main" class="document" itemscope="itemscope" itemtype="http://schema.org/Article">
           <div itemprop="articleBody">
             
  <section id="threefive-package">
<h1>threefive package<a class="headerlink" href="#threefive-package" title="Link to this heading"></a></h1>
<section id="submodules">
<h2>Submodules<a class="headerlink" href="#submodules" title="Link to this heading"></a></h2>
</section>


</section>
<section id="module-threefive.base">
<span id="threefive-base-module"></span><h2>threefive.base module<a class="headerlink" href="#module-threefive.base" title="Link to this heading"></a></h2>
<p>threefive.base contains
the class SCTE35Base.</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.base.</span></span><span class="sig-name descname"><span class="pre">SCTE35Base</span></span><a class="headerlink" href="#threefive.base.SCTE35Base" title="Link to this definition"></a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>SCTE35Base is a base class for
SpliceCommand and SpliceDescriptor classes</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.ROLLOVER">
<span class="sig-name descname"><span class="pre">ROLLOVER</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">8589934591</span></span><a class="headerlink" href="#threefive.base.SCTE35Base.ROLLOVER" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.as_90k">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">as_90k</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">int_time</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.as_90k" title="Link to this definition"></a></dt>
<dd><p>ticks to 90k timestamps</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.as_hms">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">as_hms</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">secs_of_time</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.as_hms" title="Link to this definition"></a></dt>
<dd><p>as_hms converts timestamp to
00:00:00.000 format</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.as_ticks">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">as_ticks</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">float_time</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.as_ticks" title="Link to this definition"></a></dt>
<dd><p>90k timestamps to ticks</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.fix_hex">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">fix_hex</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">hexed</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.fix_hex" title="Link to this definition"></a></dt>
<dd><p>fix_hex adds padded zero if needed for byte conversion.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.get">
<span class="sig-name descname"><span class="pre">get</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.get" title="Link to this definition"></a></dt>
<dd><p>Returns instance as a kv_clean’ed dict</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.has">
<span class="sig-name descname"><span class="pre">has</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">what</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.has" title="Link to this definition"></a></dt>
<dd><p>has runs hasattr with self and what
returns value if set.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.idxsplit">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">idxsplit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">gonzo</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">sep</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.idxsplit" title="Link to this definition"></a></dt>
<dd><p>idxsplit is like split but you keep
the sep.</p>
<dl>
<dt>example:</dt><dd><div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">idxsplit</span><span class="p">(</span><span class="s1">&#39;123456789&#39;</span><span class="p">,</span><span class="mi">4</span><span class="p">)</span>
<span class="go">&gt;&gt;&gt;&#39;456789&#39;</span>
</pre></div>
</div>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.json">
<span class="sig-name descname"><span class="pre">json</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.json" title="Link to this definition"></a></dt>
<dd><p>json returns self as kv_clean’ed json</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.kv_clean">
<span class="sig-name descname"><span class="pre">kv_clean</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.kv_clean" title="Link to this definition"></a></dt>
<dd><p>kv_clean recursively removes items
from a dict if the value is None.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.load">
<span class="sig-name descname"><span class="pre">load</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">gonzo</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.load" title="Link to this definition"></a></dt>
<dd><p>load is used to load
data from a dict or json string.
only updates vars that exist in the obj.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.base.SCTE35Base.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.base.SCTE35Base.show" title="Link to this definition"></a></dt>
<dd><p>show prints self as json to stderr (2)</p>
</dd></dl>

</dd></dl>
</section>
<section id="module-threefive.commands">
<span id="threefive-commands-module"></span><h2>threefive.commands module<a class="headerlink" href="#module-threefive.commands" title="Link to this heading"></a></h2>
<p>SCTE35 Splice Commands</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.BandwidthReservation">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">BandwidthReservation</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.BandwidthReservation" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.commands.SpliceCommand" title="threefive.commands.SpliceCommand"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceCommand</span></code></a></p>
<p>Table 12 - bandwidth_reservation()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.BandwidthReservation.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.BandwidthReservation.xml" title="Link to this definition"></a></dt>
<dd><p>create XML Node of type BandwidthReservation</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.PrivateCommand">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">PrivateCommand</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.PrivateCommand" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.commands.SpliceCommand" title="threefive.commands.SpliceCommand"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceCommand</span></code></a></p>
<p>Table 13 - private_command</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.PrivateCommand.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.PrivateCommand.decode" title="Link to this definition"></a></dt>
<dd><p>PrivateCommand.decode method</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.PrivateCommand.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.PrivateCommand.encode" title="Link to this definition"></a></dt>
<dd><p>encode private command</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.PrivateCommand.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.PrivateCommand.xml" title="Link to this definition"></a></dt>
<dd><p>create XML Node of type PrivateCommand</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.SpliceCommand">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">SpliceCommand</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceCommand" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.base.SCTE35Base" title="threefive.base.SCTE35Base"><code class="xref py py-class docutils literal notranslate"><span class="pre">SCTE35Base</span></code></a></p>
<p>Base class, not used directly.</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceCommand.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceCommand.decode" title="Link to this definition"></a></dt>
<dd><p>default decode method</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceCommand.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceCommand.encode" title="Link to this definition"></a></dt>
<dd></dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.SpliceInsert">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">SpliceInsert</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceInsert" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.commands.TimeSignal" title="threefive.commands.TimeSignal"><code class="xref py py-class docutils literal notranslate"><span class="pre">TimeSignal</span></code></a></p>
<p>Table 10 - splice_insert()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceInsert.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceInsert.decode" title="Link to this definition"></a></dt>
<dd><p>decode SpliceInsert</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceInsert.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceInsert.encode" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceInsert.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceInsert.xml" title="Link to this definition"></a></dt>
<dd><p>xml return the SpliceInsert instance as an xml node.</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.SpliceNull">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">SpliceNull</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceNull" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.commands.SpliceCommand" title="threefive.commands.SpliceCommand"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceCommand</span></code></a></p>
<p>Table 8 - splice_null()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.SpliceNull.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.SpliceNull.xml" title="Link to this definition"></a></dt>
<dd><p>xml return a SplicNull xml Node instance.</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.commands.TimeSignal">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.commands.</span></span><span class="sig-name descname"><span class="pre">TimeSignal</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.TimeSignal" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.commands.SpliceCommand" title="threefive.commands.SpliceCommand"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceCommand</span></code></a></p>
<p>Table 11 - time_signal()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.TimeSignal.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.TimeSignal.decode" title="Link to this definition"></a></dt>
<dd><p>TimeSignal.decode method</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.TimeSignal.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.TimeSignal.encode" title="Link to this definition"></a></dt>
<dd><p>encode converts TimeSignal vars
to bytes</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.commands.TimeSignal.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.commands.TimeSignal.xml" title="Link to this definition"></a></dt>
<dd><p>xml return TimeSignal as an xml node</p>
</dd></dl>

</dd></dl>
</section>
<section id="module-threefive.cue">
<span id="threefive-cue-module"></span><h2>threefive.cue module<a class="headerlink" href="#module-threefive.cue" title="Link to this heading"></a></h2>
<p>threefive.Cue Class</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.cue.Cue">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.cue.</span></span><span class="sig-name descname"><span class="pre">Cue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">packet_data</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.base.SCTE35Base" title="threefive.base.SCTE35Base"><code class="xref py py-class docutils literal notranslate"><span class="pre">SCTE35Base</span></code></a></p>
<blockquote>
<div><p>The threefive.Cue class parses individual SCTE-35 Cues or messages.</p>
</div></blockquote>
<dl>
<dt>example:</dt><dd><div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span><span class="w"> </span><span class="nn">threefive</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">Base64</span> <span class="o">=</span> <span class="s2">&quot;/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=&quot;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span> <span class="o">=</span> <span class="n">threefive</span><span class="o">.</span><span class="n">Cue</span><span class="p">(</span><span class="n">Base64</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span><span class="o">.</span><span class="n">show</span><span class="p">()</span>
</pre></div>
</div>
<ul class="simple">
<li><p>Instance variables can be accessed via dot notation.</p></li>
</ul>
<p>&gt;&gt;&gt;&gt; cue.command
{‘command_length’: 5, ‘name’: ‘Time Signal’, ‘time_specified_flag’: True,
‘pts_time’: 21695.740089}</p>
<p>&gt;&gt;&gt;&gt; cue.command.pts_time=56.345</p>
</dd>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.base64">
<span class="sig-name descname"><span class="pre">base64</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.base64" title="Link to this definition"></a></dt>
<dd><p>base64 returns SCTE35
encoded as a base64 string.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.bytes">
<span class="sig-name descname"><span class="pre">bytes</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.bytes" title="Link to this definition"></a></dt>
<dd><p>bytes returns SCTE-35
as raw bytes</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.decode" title="Link to this definition"></a></dt>
<dd><p>Cue.decode() parses for SCTE35 data</p>
<ul class="simple">
<li><p>decode doesn’t need to be called directly</p></li>
</ul>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.decode_info_section">
<span class="sig-name descname"><span class="pre">decode_info_section</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.decode_info_section" title="Link to this definition"></a></dt>
<dd><p>Cue.decode_info_section parses the
Splice Info Section
of a SCTE35 cue.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.encode" title="Link to this definition"></a></dt>
<dd><p>encode is an alias for Cue.base64()</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.encode_as_hex">
<span class="sig-name descname"><span class="pre">encode_as_hex</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.encode_as_hex" title="Link to this definition"></a></dt>
<dd><p>encode_as_hex  alias for Cue.hex()</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.encode_as_int">
<span class="sig-name descname"><span class="pre">encode_as_int</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.encode_as_int" title="Link to this definition"></a></dt>
<dd><p>encode_as_int alias for Cue.int()</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.fix_bad_b64">
<span class="sig-name descname"><span class="pre">fix_bad_b64</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.fix_bad_b64" title="Link to this definition"></a></dt>
<dd><blockquote>
<div><p>fix_bad_b64 fixes bad padding on Base64</p>
</div></blockquote>
<dl>
<dt>example:</dt><dd><div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">from</span><span class="w"> </span><span class="nn">threefive.cue</span><span class="w"> </span><span class="kn">import</span> <span class="n">fix</span><span class="o">-</span><span class="n">bad_b64</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">fix</span><span class="o">-</span><span class="n">bad_b64</span><span class="p">(</span><span class="s2">&quot;/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g&quot;</span><span class="p">)</span>
</pre></div>
</div>
<p>/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.get">
<span class="sig-name descname"><span class="pre">get</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.get" title="Link to this definition"></a></dt>
<dd><blockquote>
<div><p>Cue.get returns the SCTE-35 Cue
data as a dict of dicts.</p>
</div></blockquote>
<dl>
<dt>example:</dt><dd><div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span><span class="w"> </span><span class="nn">threefive</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">Base64</span> <span class="o">=</span> <span class="s2">&quot;/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=&quot;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span> <span class="o">=</span> <span class="n">threefive</span><span class="o">.</span><span class="n">Cue</span><span class="p">(</span><span class="n">Base64</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span><span class="o">.</span><span class="n">get</span><span class="p">()</span>
</pre></div>
</div>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.get_descriptors">
<span class="sig-name descname"><span class="pre">get_descriptors</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.get_descriptors" title="Link to this definition"></a></dt>
<dd><p>Cue.get_descriptors returns a list of
SCTE 35 splice descriptors as dicts.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.hex">
<span class="sig-name descname"><span class="pre">hex</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.hex" title="Link to this definition"></a></dt>
<dd><p>hex returns SCTE-35
encoded as a hex string</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.int">
<span class="sig-name descname"><span class="pre">int</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.int" title="Link to this definition"></a></dt>
<dd><p>int returns SCTE-35
encoded as an Integer</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.load">
<span class="sig-name descname"><span class="pre">load</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.load" title="Link to this definition"></a></dt>
<dd><p>Cue.load loads SCTE35 data into the Cue instance.
data is a dict or json or xml
with any or all of these keys
data = {</p>
<blockquote>
<div><p>‘info_section’: {dict} ,
‘command’: {dict},
‘descriptors’: [list of {dicts}],
}</p>
</div></blockquote>
<ul class="simple">
<li><dl class="simple">
<dt>You can load partial data into a Cue instance.</dt><dd><p>for instance, you can load just the command if you want.</p>
</dd>
</dl>
</li>
<li><p>load doesn’t need to be called directly
unless you initialize a Cue without data.</p></li>
</ul>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.xml" title="Link to this definition"></a></dt>
<dd><blockquote>
<div><p>xml returns SCTE-35
as xml</p>
</div></blockquote>
<dl>
<dt>example:</dt><dd><div class="doctest highlight-default notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span><span class="w"> </span><span class="nn">threefive</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">Base64</span> <span class="o">=</span> <span class="s2">&quot;/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=&quot;</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span> <span class="o">=</span> <span class="n">threefive</span><span class="o">.</span><span class="n">Cue</span><span class="p">(</span><span class="n">Base64</span><span class="p">)</span>
<span class="gp">&gt;&gt;&gt; </span><span class="n">cue</span><span class="o">.</span><span class="n">xml</span><span class="p">()</span>
</pre></div>
</div>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.cue.Cue.xmlbin">
<span class="sig-name descname"><span class="pre">xmlbin</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.cue.Cue.xmlbin" title="Link to this definition"></a></dt>
<dd><p>xmlbin returns SCTE-35
as xmlbin</p>
</dd></dl>

</dd></dl>

</section>
<section id="module-threefive.descriptors">
<span id="threefive-descriptors-module"></span><h2>threefive.descriptors module<a class="headerlink" href="#module-threefive.descriptors" title="Link to this heading"></a></h2>
<p>SCTE35 Splice Descriptors</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.AvailDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">AvailDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.AvailDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.descriptors.SpliceDescriptor" title="threefive.descriptors.SpliceDescriptor"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a></p>
<p>Table 17 -  avail_descriptor()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.AvailDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.AvailDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>decode SCTE35 Avail Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.AvailDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.AvailDescriptor.encode" title="Link to this definition"></a></dt>
<dd><p>encode SCTE35 Avail Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.AvailDescriptor.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.AvailDescriptor.xml" title="Link to this definition"></a></dt>
<dd><p>Create a Node describing the AvailDescriptor</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.DVBDASDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">DVBDASDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DVBDASDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.descriptors.SpliceDescriptor" title="threefive.descriptors.SpliceDescriptor"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a></p>
<p>Experimental DVB Descriptor Support</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.DVBDASDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DVBDASDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>Decode DVB DAS Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.DVBDASDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DVBDASDescriptor.encode" title="Link to this definition"></a></dt>
<dd><p>encode DVB DAS Descriptor</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.DtmfDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">DtmfDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DtmfDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.descriptors.SpliceDescriptor" title="threefive.descriptors.SpliceDescriptor"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a></p>
<p>Table 18 -  DTMF_descriptor()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.DtmfDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DtmfDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>decode SCTE35 Dtmf Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.DtmfDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DtmfDescriptor.encode" title="Link to this definition"></a></dt>
<dd><p>encode SCTE35 Dtmf Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.DtmfDescriptor.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.DtmfDescriptor.xml" title="Link to this definition"></a></dt>
<dd><p>Create a Node describing a DTMFDescriptor</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.SegmentationDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">SegmentationDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SegmentationDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.descriptors.SpliceDescriptor" title="threefive.descriptors.SpliceDescriptor"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a></p>
<p>Table 19 - segmentation_descriptor()</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.descriptors.SegmentationDescriptor.SUB_SEG_TYPES">
<span class="sig-name descname"><span class="pre">SUB_SEG_TYPES</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">[48,</span> <span class="pre">50,</span> <span class="pre">52,</span> <span class="pre">54,</span> <span class="pre">56,</span> <span class="pre">58,</span> <span class="pre">68,</span> <span class="pre">70]</span></span><a class="headerlink" href="#threefive.descriptors.SegmentationDescriptor.SUB_SEG_TYPES" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SegmentationDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SegmentationDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>decode a segmentation descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SegmentationDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SegmentationDescriptor.encode" title="Link to this definition"></a></dt>
<dd><p>encode a segmentation descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SegmentationDescriptor.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SegmentationDescriptor.xml" title="Link to this definition"></a></dt>
<dd><p>Create a Node describing a SegmentationDescriptor</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.SpliceDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">SpliceDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SpliceDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.base.SCTE35Base" title="threefive.base.SCTE35Base"><code class="xref py py-class docutils literal notranslate"><span class="pre">SCTE35Base</span></code></a></p>
<p>SpliceDescriptor is the
base class for all splice descriptors.
It should not be used directly</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SpliceDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SpliceDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>decode handles Private Descriptors</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SpliceDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SpliceDescriptor.encode" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SpliceDescriptor.parse_id">
<span class="sig-name descname"><span class="pre">parse_id</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SpliceDescriptor.parse_id" title="Link to this definition"></a></dt>
<dd><p>parse splice descriptor identifier</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.SpliceDescriptor.parse_tag_and_len">
<span class="sig-name descname"><span class="pre">parse_tag_and_len</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.SpliceDescriptor.parse_tag_and_len" title="Link to this definition"></a></dt>
<dd><p>parses the descriptors tag and length
from self.bites</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.descriptors.TimeDescriptor">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">TimeDescriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.TimeDescriptor" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.descriptors.SpliceDescriptor" title="threefive.descriptors.SpliceDescriptor"><code class="xref py py-class docutils literal notranslate"><span class="pre">SpliceDescriptor</span></code></a></p>
<p>Table 25 - time_descriptor()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.TimeDescriptor.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.TimeDescriptor.decode" title="Link to this definition"></a></dt>
<dd><p>decode SCTE35 Time Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.TimeDescriptor.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.TimeDescriptor.encode" title="Link to this definition"></a></dt>
<dd><p>encode SCTE35 Time Descriptor</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.descriptors.TimeDescriptor.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.TimeDescriptor.xml" title="Link to this definition"></a></dt>
<dd><p>create a Node describing a TimeDescriptor</p>
</dd></dl>

</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.descriptors.splice_descriptor">
<span class="sig-prename descclassname"><span class="pre">threefive.descriptors.</span></span><span class="sig-name descname"><span class="pre">splice_descriptor</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bites</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.descriptors.splice_descriptor" title="Link to this definition"></a></dt>
<dd><p>replaced splice_descriptor</p>
</dd></dl>

</section>
<section id="module-threefive.segment">
<span id="threefive-segment-module"></span><h2>threefive.segment module<a class="headerlink" href="#module-threefive.segment" title="Link to this heading"></a></h2>
<p>The threefive.Segment class</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.segment.Segment">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.segment.</span></span><span class="sig-name descname"><span class="pre">Segment</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">seg_uri</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">key_uri</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">iv</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.segment.Segment" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.stream.Stream" title="threefive.stream.Stream"><code class="xref py py-class docutils literal notranslate"><span class="pre">Stream</span></code></a></p>
<p>The Segment class is a Sub Class of threefive.Stream
made for small, fixed size MPEGTS files,like HLS segments.</p>
<p>Segment Class Specific Features:</p>
<ul class="simple">
<li><p>Decryption of AES Encrypted MPEGTS.</p></li>
<li><p>Segment.cues  a list of SCTE35 cues found in the segment.</p></li>
</ul>
<p>Example:</p>
<blockquote>
<div><p>from threefive import Segment</p>
<p>&gt;&gt;&gt;&gt; uri = “<a class="reference external" href="https://example.com/1.ts">https://example.com/1.ts</a>”
&gt;&gt;&gt;&gt; seg = Segment(uri)
&gt;&gt;&gt;&gt; seg.decode()
&gt;&gt;&gt;&gt; [cue.encode() for cue in seg.cues]
[‘/DARAAAAAAAAAP/wAAAAAHpPv/8=’,
‘/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=’]</p>
</div></blockquote>
<p>AES Encryption Example:</p>
<blockquote>
<div><blockquote>
<div><p>from threefive import Segment</p>
<p>&gt;&gt;&gt;&gt; key = “<a class="reference external" href="https://example.com/aes.key">https://example.com/aes.key</a>”
&gt;&gt;&gt;&gt; IV=0x998C575D24F514AEC84EDC5CABCCDB81
&gt;&gt;&gt;&gt; uri = “<a class="reference external" href="https://example.com/aes-1.ts">https://example.com/aes-1.ts</a>”</p>
<p>&gt;&gt;&gt;&gt; seg = Segment(uri,key_uri=key, iv=IV)
&gt;&gt;&gt;&gt; seg.decode()
&gt;&gt;&gt;&gt; {cue.packet_data.pts:cue.encode() for cue in seg.cues}</p>
</div></blockquote>
<p>{ 89718.451333: ‘/DARAAAAAAAAAP/wAAAAAHpPv/8=’,
89730.281789: ‘/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=’}</p>
</div></blockquote>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.segment.Segment.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.segment.Segment.decode" title="Link to this definition"></a></dt>
<dd><p>decode a mpegts segment.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.segment.Segment.show_cue">
<span class="sig-name descname"><span class="pre">show_cue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">cue</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.segment.Segment.show_cue" title="Link to this definition"></a></dt>
<dd><p>show_cue prints SCTE35 Cue data
and calls add_cue to append the cue to
the Segment,cues list.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.segment.Segment.shushed">
<span class="sig-name descname"><span class="pre">shushed</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.segment.Segment.shushed" title="Link to this definition"></a></dt>
<dd><p>shushed sets self.shush to true to suppress
printing SCTE-35 Cue data.</p>
</dd></dl>

</dd></dl>

</section>

<section id="module-threefive.stream">
<span id="threefive-stream-module"></span><h2>threefive.stream module<a class="headerlink" href="#module-threefive.stream" title="Link to this heading"></a></h2>
<p>Mpeg-TS Stream parsing class Stream</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.stream.Based">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">Based</span></span><a class="headerlink" href="#threefive.stream.Based" title="Link to this definition"></a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Based is a base class</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.stream.Maps">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">Maps</span></span><a class="headerlink" href="#threefive.stream.Maps" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.stream.Based" title="threefive.stream.Based"><code class="xref py py-class docutils literal notranslate"><span class="pre">Based</span></code></a></p>
<p>Maps holds mappings
pids mapped to continuity_counters,
programs, partial tables and last payload.</p>
<p>programs mapped to pcr and pts</p>
</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.stream.Pids">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">Pids</span></span><a class="headerlink" href="#threefive.stream.Pids" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.stream.Based" title="threefive.stream.Based"><code class="xref py py-class docutils literal notranslate"><span class="pre">Based</span></code></a></p>
<p>Pids holds sets of pids for pat,pcr,pmt, and scte35</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Pids.PAT_PID">
<span class="sig-name descname"><span class="pre">PAT_PID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">0</span></span><a class="headerlink" href="#threefive.stream.Pids.PAT_PID" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Pids.SDT_PID">
<span class="sig-name descname"><span class="pre">SDT_PID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">17</span></span><a class="headerlink" href="#threefive.stream.Pids.SDT_PID" title="Link to this definition"></a></dt>
<dd></dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.stream.ProgramInfo">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">ProgramInfo</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pid</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">pcr_pid</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.ProgramInfo" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.stream.Based" title="threefive.stream.Based"><code class="xref py py-class docutils literal notranslate"><span class="pre">Based</span></code></a></p>
<p>ProgramInfo is a class to
hold Program information
for use with Stream.show()</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.ProgramInfo.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.ProgramInfo.show" title="Link to this definition"></a></dt>
<dd><p>show print2 the Program Infomation
in a familiar format.</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.stream.Stream">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">Stream</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">tsdata</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">show_null</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">headers</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">{}</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.stream.Based" title="threefive.stream.Based"><code class="xref py py-class docutils literal notranslate"><span class="pre">Based</span></code></a></p>
<p>Stream class for parsing MPEG-TS data.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.PACKET_SIZE">
<span class="sig-name descname"><span class="pre">PACKET_SIZE</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">188</span></span><a class="headerlink" href="#threefive.stream.Stream.PACKET_SIZE" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.PMT_TID">
<span class="sig-name descname"><span class="pre">PMT_TID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">b'\x02'</span></span><a class="headerlink" href="#threefive.stream.Stream.PMT_TID" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.ROLLOVER">
<span class="sig-name descname"><span class="pre">ROLLOVER</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">8589934591</span></span><a class="headerlink" href="#threefive.stream.Stream.ROLLOVER" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.ROLLOVER9K">
<span class="sig-name descname"><span class="pre">ROLLOVER9K</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">95443.717678</span></span><a class="headerlink" href="#threefive.stream.Stream.ROLLOVER9K" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.SCTE35_PES_START">
<span class="sig-name descname"><span class="pre">SCTE35_PES_START</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">b'\x00\x00\x01\xfc'</span></span><a class="headerlink" href="#threefive.stream.Stream.SCTE35_PES_START" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.SCTE35_TID">
<span class="sig-name descname"><span class="pre">SCTE35_TID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">b'\xfc'</span></span><a class="headerlink" href="#threefive.stream.Stream.SCTE35_TID" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.SDT_TID">
<span class="sig-name descname"><span class="pre">SDT_TID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">b'B'</span></span><a class="headerlink" href="#threefive.stream.Stream.SDT_TID" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py attribute">
<dt class="sig sig-object py" id="threefive.stream.Stream.SYNC_BYTE">
<span class="sig-name descname"><span class="pre">SYNC_BYTE</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">71</span></span><a class="headerlink" href="#threefive.stream.Stream.SYNC_BYTE" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.as_90k">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">as_90k</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ticks</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.as_90k" title="Link to this definition"></a></dt>
<dd><p>as_90k returns ticks as 90k clock time</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">&lt;function</span> <span class="pre">show_cue&gt;</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.decode" title="Link to this definition"></a></dt>
<dd><p>Stream.decode reads self.tsdata to find SCTE35 packets.
func can be set to a custom function that accepts
a threefive.Cue instance as it’s only argument.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.decode_next">
<span class="sig-name descname"><span class="pre">decode_next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.decode_next" title="Link to this definition"></a></dt>
<dd><p>Stream.decode_next returns the next
SCTE35 cue as a threefive.Cue instance.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.decode_pids">
<span class="sig-name descname"><span class="pre">decode_pids</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">scte35_pids</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">&lt;function</span> <span class="pre">show_cue&gt;</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.decode_pids" title="Link to this definition"></a></dt>
<dd><p>Stream.decode_pids takes a list of SCTE-35 Pids parse
and an optional call back function to run when a Cue is found.
if scte35_pids is not set, all threefive pids will be parsed.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.decode_start_time">
<span class="sig-name descname"><span class="pre">decode_start_time</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.decode_start_time" title="Link to this definition"></a></dt>
<dd></dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.iter_pkts">
<span class="sig-name descname"><span class="pre">iter_pkts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">num_pkts</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">1</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.iter_pkts" title="Link to this definition"></a></dt>
<dd><p>iter_pkts iterates a mpegts stream into packets</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.mk_pts">
<span class="property"><span class="k"><span class="pre">static</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">mk_pts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">payload</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.mk_pts" title="Link to this definition"></a></dt>
<dd><p>mk_pts calculate pts from payload</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.pid2pcr">
<span class="sig-name descname"><span class="pre">pid2pcr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.pid2pcr" title="Link to this definition"></a></dt>
<dd><p>pid2pcr takes a pid
returns the current pcr</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.pid2prgm">
<span class="sig-name descname"><span class="pre">pid2prgm</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.pid2prgm" title="Link to this definition"></a></dt>
<dd><p>pid2prgm takes a pid,
returns the program</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.pid2pts">
<span class="sig-name descname"><span class="pre">pid2pts</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.pid2pts" title="Link to this definition"></a></dt>
<dd><p>pid2pts takes a pid
returns the current pts</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.proxy">
<span class="sig-name descname"><span class="pre">proxy</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">&lt;function</span> <span class="pre">show_cue&gt;</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.proxy" title="Link to this definition"></a></dt>
<dd><p>Stream.decode_proxy writes all ts packets are written to stdout
for piping into another program like mplayer.
SCTE-35 cues are print2`ed to stderr.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.pts">
<span class="sig-name descname"><span class="pre">pts</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.pts" title="Link to this definition"></a></dt>
<dd><p>pts returns a dict of  program:pts</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.rt">
<span class="sig-name descname"><span class="pre">rt</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">&lt;function</span> <span class="pre">show_cue&gt;</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.rt" title="Link to this definition"></a></dt>
<dd><p>rt  all ts packets are written to stdout
for piping into another program in real time.
SCTE-35 cues are print2`ed to stderr.
decode SCTE-35.  the arg func can be set to
a function that accepts one arg, a Cue instance.
func is called everytime a Cue is found in the stream.
the default func, show_cue calls Cue.show().</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.show">
<span class="sig-name descname"><span class="pre">show</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.show" title="Link to this definition"></a></dt>
<dd><p>displays streams that will be
parsed for SCTE-35.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.show_pts">
<span class="sig-name descname"><span class="pre">show_pts</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.show_pts" title="Link to this definition"></a></dt>
<dd><p>show_pts displays current pts by pid.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.stream.Stream.speed">
<span class="sig-name descname"><span class="pre">speed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">func</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">&lt;function</span> <span class="pre">show_cue&gt;</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.Stream.speed" title="Link to this definition"></a></dt>
<dd><p>Stream.speed is identical to Stream.decode
but also shows parsing speed.</p>
</dd></dl>

</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stream.no_op">
<span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">no_op</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">cue</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.no_op" title="Link to this definition"></a></dt>
<dd><p>no_op is just a dummy func to pass to Stream.decode()
to suppress output.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stream.show_cue">
<span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">show_cue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">cue</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.show_cue" title="Link to this definition"></a></dt>
<dd><p>default function call for Stream.decode
when a SCTE-35 packet is found.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stream.show_cue_stderr">
<span class="sig-prename descclassname"><span class="pre">threefive.stream.</span></span><span class="sig-name descname"><span class="pre">show_cue_stderr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">cue</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stream.show_cue_stderr" title="Link to this definition"></a></dt>
<dd><p>print2 cue data to sys.stderr
for Stream.decode_proxy</p>
</dd></dl>

</section>
<section id="module-threefive.stuff">
<span id="threefive-stuff-module"></span><h2>threefive.stuff module<a class="headerlink" href="#module-threefive.stuff" title="Link to this heading"></a></h2>
<p>stuff.py functions and such common to threefive.</p>
<p>print2, pif, iso8601, red, blue</p>
<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.badtype">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">badtype</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">shouldbe</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.badtype" title="Link to this definition"></a></dt>
<dd><p>badtype shows a red message that we have a wrong type.
data can be anything.
shouldbe is a string like “int”, or “SpliceCommand”
data: anything
shouldbe: type</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.blue">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">blue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">message</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.blue" title="Link to this definition"></a></dt>
<dd><p>blue  print info messages in blue to stderr.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.clean">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">clean</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.clean" title="Link to this definition"></a></dt>
<dd><p>clean strip and if it’s a byte string
convert to a string</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.codec_detect">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">codec_detect</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.codec_detect" title="Link to this definition"></a></dt>
<dd><p>codec_detect decode bytes by trying multiple encodings
to find one that is compatible.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.isfloat">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">isfloat</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.isfloat" title="Link to this definition"></a></dt>
<dd><p>isfloat determine if a str or bytes is a float</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.ishex">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">ishex</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.ishex" title="Link to this definition"></a></dt>
<dd><p>ishex determine if a string is a hex value.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.isjson">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">isjson</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.isjson" title="Link to this definition"></a></dt>
<dd><p>isjson determine if a string or bytestring
is json.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.iso8601">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">iso8601</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.iso8601" title="Link to this definition"></a></dt>
<dd><p>return UTC time in iso8601 format.</p>
<p>‘2023-05-11T15:55:51.’</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.isxml">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">isxml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.isxml" title="Link to this definition"></a></dt>
<dd><p>isxml determine if a string or bytestring
is xml.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.k_by_v">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">k_by_v</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">adict</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">avalue</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.k_by_v" title="Link to this definition"></a></dt>
<dd><p>dict key lookup by value</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.no_ESC">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">no_ESC</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">a_string</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.no_ESC" title="Link to this definition"></a></dt>
<dd><p>no_ESC removes ansi colors
from astring</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.pif">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">pif</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.pif" title="Link to this definition"></a></dt>
<dd><p>pif  parses  an int or float from byte strings and strings and hex
if it’s not a string or byte string it  just returns the value.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.print2">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">print2</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">gonzo</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">b''</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.print2" title="Link to this definition"></a></dt>
<dd><p>print2 prints to 2 aka stderr.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.reblue">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">reblue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">message</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.reblue" title="Link to this definition"></a></dt>
<dd><p>reblue overwrites the last line in place</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.red">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">red</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">message</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.red" title="Link to this definition"></a></dt>
<dd><p>red  print error messages in red to stderr.</p>
</dd></dl>

<dl class="py function">
<dt class="sig sig-object py" id="threefive.stuff.rmap">
<span class="sig-prename descclassname"><span class="pre">threefive.stuff.</span></span><span class="sig-name descname"><span class="pre">rmap</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">data</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">amap</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.stuff.rmap" title="Link to this definition"></a></dt>
<dd><p>rmap multiple replaces applied to a string.
works like translate but smoother
data: string
amap: dict</p>
<p>returns string</p>
</dd></dl>

</section>
</section>
<section id="module-threefive.upids">
<span id="threefive-upids-module"></span><h2>threefive.upids module<a class="headerlink" href="#module-threefive.upids" title="Link to this heading"></a></h2>
<p>upids.py classy Upids</p>
<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.AirId">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">AirId</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.AirId" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Air Id Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.AirId.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.AirId.decode" title="Link to this definition"></a></dt>
<dd><p>decode AirId</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.AirId.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.AirId.encode" title="Link to this definition"></a></dt>
<dd><p>encode AirId</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Atsc">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Atsc</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Atsc" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>ATSC Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Atsc.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Atsc.decode" title="Link to this definition"></a></dt>
<dd><p>decode Atsc Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Atsc.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Atsc.encode" title="Link to this definition"></a></dt>
<dd><p>encode Atsc</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Eidr">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Eidr</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Eidr" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Eidr Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Eidr.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Eidr.decode" title="Link to this definition"></a></dt>
<dd><p>decode Eidr Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Eidr.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Eidr.encode" title="Link to this definition"></a></dt>
<dd><p>encode Eidr Upid</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Isan">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Isan</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Isan" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Isan Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Isan.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Isan.decode" title="Link to this definition"></a></dt>
<dd><p>decode Isan Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Isan.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Isan.encode" title="Link to this definition"></a></dt>
<dd><p>encode Isan Upid</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Mid">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Mid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mid" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Mid Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Mid.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mid.decode" title="Link to this definition"></a></dt>
<dd><p>decode Mid Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Mid.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mid.encode" title="Link to this definition"></a></dt>
<dd><p>encode Mid Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Mid.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mid.xml" title="Link to this definition"></a></dt>
<dd><p>xml return a upid xml node</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Mpu">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Mpu</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mpu" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Mpu Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Mpu.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mpu.decode" title="Link to this definition"></a></dt>
<dd><p>decode MPU Upids</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Mpu.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Mpu.encode" title="Link to this definition"></a></dt>
<dd><p>encode MPU Upids</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.NoUpid">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">NoUpid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.NoUpid" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>NoUpid class</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.NoUpid.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.NoUpid.decode" title="Link to this definition"></a></dt>
<dd><p>decode for no upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.NoUpid.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.NoUpid.encode" title="Link to this definition"></a></dt>
<dd><p>encode for no upid</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Umid">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Umid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Umid" title="Link to this definition"></a></dt>
<dd><p>Bases: <a class="reference internal" href="#threefive.upids.Upid" title="threefive.upids.Upid"><code class="xref py py-class docutils literal notranslate"><span class="pre">Upid</span></code></a></p>
<p>Umid Upid</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Umid.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Umid.decode" title="Link to this definition"></a></dt>
<dd><p>decode Umid Upids</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Umid.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Umid.encode" title="Link to this definition"></a></dt>
<dd><p>encode Umid Upid</p>
</dd></dl>

</dd></dl>

<dl class="py class">
<dt class="sig sig-object py" id="threefive.upids.Upid">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">Upid</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">bitbin</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_type</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">upid_length</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Upid" title="Link to this definition"></a></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Upid base class handles URI UPIDS</p>
<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Upid.decode">
<span class="sig-name descname"><span class="pre">decode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Upid.decode" title="Link to this definition"></a></dt>
<dd><p>decode Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Upid.encode">
<span class="sig-name descname"><span class="pre">encode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">nbin</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Upid.encode" title="Link to this definition"></a></dt>
<dd><p>encode Upid</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Upid.redecode">
<span class="sig-name descname"><span class="pre">redecode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">seg_upid</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Upid.redecode" title="Link to this definition"></a></dt>
<dd><p>redecode is for decoding complex xml upids
before encodingto another format.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="threefive.upids.Upid.xml">
<span class="sig-name descname"><span class="pre">xml</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">ns</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">'scte35'</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#threefive.upids.Upid.xml" title="Link to this definition"></a></dt>
<dd><p>xml return a upid xml node for simple and  complex upids</p>
</dd></dl>

</dd></dl>

<dl class="py data">
<dt class="sig sig-object py" id="threefive.upids.charset">
<span class="sig-prename descclassname"><span class="pre">threefive.upids.</span></span><span class="sig-name descname"><span class="pre">charset</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">'ascii'</span></span><a class="headerlink" href="#threefive.upids.charset" title="Link to this definition"></a></dt>
<dd><p>set charset to None to return raw bytes</p>
</dd></dl>

</section>

</html>
