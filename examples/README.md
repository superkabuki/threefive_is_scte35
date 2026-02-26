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

## [More Examples]

* [aac_id3header.py](aac_id3header.py) - use the __threefive.aac.AacParser__ class to parse __HLS AAC__ segments for __PTS__ in __ID3 header tags__. _(__Updated__ 01/07/2026)_
* [id3.aac](id3.aac) test file for __aac_id3header.py__   _(__New!__ 01/12/2026)_
* [base64toxmlbin.py](base64toxmlbin.py) - __convert__ __base64__ encoded __SCTE-35__ to __xml+binary__ encoded SCTE-35 and back.
* [cue2vtt.py](cue2vtt.py) - display __SCTE-35__ data on video using __WebVTT__ subtitles to __verify__ __SCTE-35__ __splice points__.
* [decodenext.py](decodenext.py) - parse __MPEGTS__ streams for __SCTE-35__ using __Stream.decode_next()__.  _(__Updated__ 01/12/2026)_
* [dtmf.py](dtmf.py) - parse __base64__ __SCTE-35__ with a __DTMF__ descriptor and __re-encode__ to __SCTE-35__ in __Hex__ format.
* [edit_break_duration.py](edit_break_duration.py) - change the __SCTE-35__ __break duration__ and __re-encode__ __SCTE-35__.
* [encode_time_signal.py](encode_time_signal.py) - __encode__ a __SCTE-35__ __Cue__ with a __TimeSignal__ from scratch.
* [parsehlstags.py](parsehlstags.py) - use the __TagParser__ class to parse __HLS tags__ from a __m3u8__ file and group the tags by segment.
* [proxy.py](proxy.py) - how to use the __Stream.proxy()__ method for parsing __SCTE-35__ and __piping__ video.
* [quickstream.py](quickstream.py) - how to __add SCTE-35 parsing__ for __MPEGTS__ streams to __your application__.
* [spliceinsert.py](spliceinsert.py) - a __SCTE-35__ __Splice Insert__ example.  
* [upid_custom_output.py](upid_custom_output.py) - __customizing Upid data output__ for a variety of __Upids__. _(__New!__ 01/11/2026)_
* [custom_upid_handling.py](custom_upid_handling.py) -  Custom __user defined UPID__ handling example. _(__New!__ 01/11/2026)_
