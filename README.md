# [ threefive ]
## https://github.com/superkabuki/threefive

### __threefive__ is the industry leading SCTE-35 tool. 

___

### [ Terms and Conditions ]
*    __You be cool, and I'll be cool.__
*    __Questions?__ Ask them. 
*    __Features?__ Speak up. I'm open to new ideas..
*    __Comments?__ Make them. 
*    __Got Code?__ Do a pull request.
___
### [ News ]
* __Python3 vs. Pypy3__ [__parsing SCTE35 with threefive__](https://github.com/superkabuki/threefive_is_scte35#python3-vs-pypy3-running-threefive) (watch the cool video)
 
* __threefive now supports__ [__Secure Reliable Transport__](https://github.com/superkabuki/threefive_is_scte35/blob/main/README.md#threefive-now-supports-srt)

___

### [ Latest version is  v3.0.71 ]
* [why can`t you be more cyclomatic like your brother?](cyclomatic.md)
* All ansi color codes striped when output is not a tty.
*  __threefive.Cue.xmlbin()__ now returns a __threefive.xml.Node instance like__ __threefive.Cue.xml()__. 
* __threefive.Stream__ has a new method __threefive.Stream.rt(func=show_cue)__  that parses SCTE-35 and proxies the stream to stdout at realtime speed.
* <s>__threefive.Stream.decode()__ now shows parse speed.</s>
* __Cli tool__ new features
	* __New  __bump__ keyword to adjust SCTE-35 PTS. Supports positive and negative adjustments.
    * New __rt__  keyword parses SCTE-35, writes a SCTE-35 sidecar file, and outputs the MPEGTS stream to stdout at realtime speed.   
	*  <s>All __MPEGTS__ related tasks show parsing speed.</s>
	* __threefive mcast__ now throttles Multicast output to realtime speed.
    * __threefive packets__ and __threefive pts__ now works with __SRT__.

___

### [ Features ]

<samp>

* __Decode SCTE-35__ from MPEGTS ✔ Base64 ✔ Bytes ✔ DASH ✔ Hex ✔ HLS ✔ Integers ✔ JSON ✔ XML  ✔ XML+Binary ✔ DASH ✔ Dicts ✔  

* __Encodes SCTE-35__ to MPEGTS ✔ Base64 ✔ Bytes ✔ Hex ✔ Integers ✔ JSON ✔ XML ✔ XML+Binary ✔

* __threefive file protocols__ Pipes(stdin, stdout) ✔ Files ✔

* __threefive network protocols__ HTTP(s) ✔ Multicast ✔ UDP ✔ SRT ✔ 

* __Automatic AES decryption__ for __MPEGTS__ and __HLS__. ✔

* __Built-in Multicast Sender__ and __Receiver__. ✔

* __Injects SCTE-35 Packets__ into __MPEGTS__ video ✔.

___

###  [ Tip Of The Week ]

*  __Stream.decode_next()__ is now a generator

```py3
	from threefive import Stream

    strm =Stream(some_url)
    for cue in strm.decode_next():
		your_complicated_function(cue, one_arg , two_arg, 13,)
```        

___

# [ Documentation ]
	
* [__Install__](#install) 
* [SCTE-35 Decoding __Quick Start__ ](#quick-start) _threefive makes decoding SCTE-35 fast and easy_
* [SCTE-35 __Examples__](https://github.com/superkabuki/threefive/tree/main/examples) _examples of all kinds of SCTE-35 stuff_
* [SCTE-35 __Cli__](#-the-cli-tool-) _decode SCTE-35 on the command line_
* [__Using the threefive library__](#using-the-library) _decode SCTE-35 with less than ten lines of code_
	* [__Using the threefive.Cue class__](https://github.com/superkabuki/threefive/blob/main/lib.md) 
* [SCTE-35 __HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) _parse SCTE-35 in HLS__
* [SCTE-35 __XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) _threefive can parse and encode SCTE-35 xml_
* [__Encode__ SCTE-35](https://github.com/superkabuki/threefive/blob/main/encode.md) _threefive can encode SCTE-35 in every SCTE-35 format_
* [SCTE-35 __Sidecar Files__](https://github.com/superkabuki/SCTE-35_Sidecar_Files) _threefive supports SCTE-35 sidecar files_
* [__SuperKabuki__ SCTE-35 MPEGTS __Packet Injection__](inject.md) _inject SCTE-35 into MPEGTS streams_ 
* [threefive __Classes__](#classes) _threefive is OO, made to subclass_
	* [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) _this class you'll use often_ 
	* [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) _this is the class for parsing MPEGTS_
* [Use threefive to stream __Multicast__](#-threefive-streams-multicast-its-easy-) _threefive is a multicast client and server_
* [threefive SCTE-35 __Online Parser__](https://iodisco.com/scte35) hosted on my server_
* [ SCTE-35 __Online Parser__ powered by threefive](http://www.domus1938.com/scte35parser) _another online parser powered by threefive_
* [SCTE-35 __As a Service__](sassy.md) _if you can make an http request, you can parse SCTE-35, no install needed._
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

##  [Examples]

 <details><summary>

### mpegts 

 </summary>
 
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



<details><summary>

### Base64

</summary>

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


<details><summary>

### Bytes

</summary>

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


<details><summary>
	
### Hex

</summary>

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


<details><summary>
	
### Int

</summary>

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


<details><summary>
	
### JSON

</summary>

* __cli__
	* 	put JSON SCTE-35 in a file and redirect it into threefive 
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


<details><summary><u>

### Xml

</u>
</summary>

* __cli__
	* put xml SCTE-35 in a [file](xml.xml) and redirect it into threefive 
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



<details><summary>
	
### Xml+binary

</summary>

* __cli__
	* write xml+binary to a [file](xmlbin.xml) and redirect it to threefive
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

##  [__More Examples__](https://github.com/superkabuki/threefive/tree/main/examples)

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
 * __Start the Receiver first__
* It's optimized for MPEGTS (1316 byte Datagrams) but you can send any video or file.
* The defaults will work in most situations, you don't even have to set the address.
* threefive cli also supports UDP Unicast Streaming.
   
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


___


## [iodisco.com/scte35](https://iodisco.com/scte35)





 <svg width="100" height="100">
  <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
</svg> 

 <img width="258" height="256" alt="image" src="https://github.com/user-attachments/assets/642cb803-9465-408e-bb6e-03549eb22d78" />

___
 [__Install__](#install) |[__SCTE-35 Cli__](#the-cli-tool) | [__SCTE-35 HLS__](https://github.com/superkabuki/threefive/blob/main/hls.md) | [__Cue__ Class](https://github.com/superkabuki/threefive/blob/main/cue.md) | [__Stream__ Class](https://github.com/superkabuki/threefive/blob/main/stream.md) | [__Online SCTE-35 Parser__](https://iodisco.com/scte35) | [__Encode SCTE-35__](https://github.com/superkabuki/threefive/blob/main/encode.md) | [__SCTE-35 Examples__](https://github.com/superkabuki/threefive/tree/main/examples)
 | [__SCTE-35 XML__ ](https://github.com/superkabuki/SCTE-35/blob/main/xml.md) and [More __XML__](node.md) | [__threefive runs Four Times Faster on pypy3__](https://pypy.org/) | [__SuperKabuki SCTE-35 MPEGTS Packet Injection__](inject.md)

