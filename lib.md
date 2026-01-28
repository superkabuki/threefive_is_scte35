# Using threefive as a library.

#### threefive is made almost entirely of classes.

#### The class used most often is the Cue class. 
* [Decoding](#decoding)
* [Output methods](#output-methods)
* [Components](#components)
* [Inherited SCTE35Base methods](#threefivescte35base)
  
# Decoding 

#### A Cue instance can decode SCTE-35 from Base64, Bytes, Hex, Integer, JSON, Xml, Xml+bin, or a raw MPEGTS packet.

* Some Examples

```py3
>>>> from threefive import Cue
```

* __Base64__

```py3
>>>> cue=Cue('/DAgAAAAAAAAAP/wDwUAAAABf//+AFJlwAABAAAAAMOOklg=')
```
* __Bytes__

```py3
>>>> cue =Cue(b'\xfc0 \x00\x00\x00\x00\x00\x00\x00\xff\xf0\x0f\x05\x00\x00\x00\x01\x7f\xff\xfe\x00Re\xc0\x00\x01\x00\x00\x00\x00\xc3\x8e\x92X')
```
* __Int__

```py3
>>>> cue=Cue(1913741249324105789713965315611872444571137197654250805822733947388252170837252018776)
```
* __Xml__

```py3
>>>> exemel='''<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="1">
      <scte35:BreakDuration autoReturn="true" duration="5400000"/>
   </scte35:SpliceInsert>
</scte35:SpliceInfoSection>'''

>>>> cue =Cue(exemel)
```

#### Once you have a Cue instance you can print the data in JSON with the show() method.

```py3
>>>> from threefive import Cue

>>>> cue=Cue('/DAgAAAAAAAAAP/wDwUAAAABf//+AFJlwAABAAAAAMOOklg=')

>>>> cue.show()

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 32,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xc38e9258"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 60.0,
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": []
}
```
___

#### Cue variables or attributes can be accessed via dot notation.
```py3
>>>> from threefive import Cue
>>>> cue=Cue('/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==')
>>>> cue.info_section.table_id
'0xfc'
>>>> cue.command.pts_time
123.456789

```
___

# Output methods

#### The data can be returned in a variety of formats.

* __Cue.base64()__ _returns SCTE-35 as bytes_
 
* __Cue.bytes()__  _returns SCTE-35 darta as bytes_

* __Cue.hex()__ _returns SCTE-35 data as a hex string_

* __Cue.int()__ _returns SCTE-35 data as a big integer_

* __Cue.json()__ _returns SCTE-35 data as a json string_

* __Cue.xml()__ _returns SCTE-35 data as Xml_
`
* __Cue.xmlbin()__ _returns SCTE-35 as Xml+binary_

___

# Components

#### A Cue can also be initialized without data.

```
>>>> from threefive import Cue 

>>>> cue=Cue()
```

* __A Cue instance contains__

    * 1 Splice InfoSection as __Cue.InfoSection__ 
    * 1 Splice Command as __Cue.command__
    * 0 or more Splice Descriptors as a list __Cue.descriptors__
      * A Splice Descriptor contains 0 or more __Upids__ 

___

* __Splice Commands__ 
  * BandwidthReservation
  * PrivateCommand
  * SpliceNull
  * TimeSignal
  * SpliceInsert

___

* __Splice Descriptors__
    * AvailDescriptor
    * DtmfDescriptor
    * DVBDASDescriptor
    * SegmentationDescriptor
    * TimeDescriptor

___

* __Upids__

    * Upid
    * AirId
    * Atsc
    * Mid
    * Mpu
    * Eidr
    * NoUpid
    * Isan
    * Umid

___

#### The individual components of a Cue can be initialized and added to the Cue, the Splice Info Section is automatically added for you.

```py3
>>>> from threefive import Cue, TimeSignal

>>>> cue=Cue()

>>>> ts=TimeSignal()

>>>> cue.command=ts


>>>> cue

{'command': {'command_length': 0, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': None, 'pts_time': None},
 'descriptors': [],
 'info_section': {'table_id': None, 'section_syntax_indicator': None, 'private': None, 'sap_type': None,
 'sap_details': None, 'section_length': None, 'protocol_version': None, 'encrypted_packet': None, 'encryption_algorithm': None,
 'pts_adjustment': 0, 'cw_index': None, 'tier': None, 'splice_command_length': None, 'splice_command_type': None,
 'descriptor_loop_length': 0, 'crc': None},
 'bites': None, 'packet_data': None, 'dash_data': None}

```
___

#### Cue vars can be edited via dot notation

```py3
>>>> cue.command.time_specified_flag
False

>>>> cue.command.time_specified_flag=True

>>>> cue.command.time_specified_flag
True

>>>> cue.command.pts_time=123.456789

>>>> cue

{'command': {'command_length': 0, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': True, 'pts_time': 123.456789}, 'descriptors': [], 'info_section': {'table_id': None, 'section_syntax_indicator': None, 'private': None, 'sap_type': None, 'sap_details': None, 'section_length': None, 'protocol_version': None, 'encrypted_packet': None, 'encryption_algorithm': None, 'pts_adjustment': 0, 'cw_index': None, 'tier': None, 'splice_command_length': None, 'splice_command_type': None, 'descriptor_loop_length': 0, 'crc': None}, 'bites': None, 'packet_data': None, 'dash_data': None}
```
___

#### Running Cue.encode() will fill in the Splice Info Section.
```py3

>>>> cue.encode()
'/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q=='

>>>> cue

{'command': {'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 123.456789},
 'descriptors': [],
'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x03',
 'sap_details': 'No Sap Type', 'section_length': 22, 'protocol_version': 0, 'encrypted_packet': False,
 'encryption_algorithm': 0, 'pts_adjustment': 0.0, 'cw_index': '0x00', 'tier': '0x0fff', 'splice_command_length': 5,
 'splice_command_type': 6, 'descriptor_loop_length': 0, 'crc': '0xb3baed9'},
'bites': b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\xa9\x8a\xc7\x00\x00\x0b;\xae\xd9',
 'packet_data': None, 'dash_data': None}

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
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xb3baed9"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 123.456789
    },
    "descriptors": []
}
```

___


## Cue, Splice Info Section, Splice Commands, Splice Descriptors, and Upids all have these methods.

* __decode()__ decode the SCTE-35 component
* __encode()__ encode the SCTE-35 component and return the byte string
* __xml()__    return a threefive.Node xml instance

___

## Splice Info Section, Splice Commands, Splice Descriptors, and Upids can be manipulated with or without a Cue.
```py3
>>>> from threefive import TimeSignal

>>>> ts = TimeSignal()
>>>> cue.command.time_specified_flag=True
>>>> cue.command.pts_time=123.456789

>>>>ts.encode()
b'\xfe\x00\xa9\x8a\xc7'

>>>> ts.xml()

<scte35:TimeSignal >
   <scte35:SpliceTime ptsTime="11111111"/>
</scte35:TimeSignal>

```
___

# threefive.SCTE35Base

## Cue, Splice Info Section, Splice Commands, and Splice Descriptors all inherit from threefive.SCTE35Base 

####  Methods inherited from threefive.base.SCTE35Base:
  
 * __has(self, what)__ has runs hasattr with self and what as the attribute. Returns value of what if set or False if not set. 
 * __json(self)__  returns self as kv_clean'ed json
 * __kv_clean(self)__ recursively removes attributes from the instance if the value is None.
 * __show(self)__ prints __kv_clean__'ed self as json to stderr
 
#### Static methods inherited from threefive.base.SCTE35Base:

 * __as_90k(int_time)__ ticks to 90k timestamps
 * __as_hms(secs_of_time)__ converts timestamp to 00:00:00.000 format
 * __as_ticks(float_time)__ 90k timestamps to ticks
 * __fix_hex(hexed)__ adds padded zero if needed for byte conversion.
```py3
>>> from threefive import Cue
>>>> cue=Cue()
>>>> cue.fix_hex('0xDBEE3')
'0x0DBEE3'
```
 * __idxsplit(gonzo, sep)__  split gonzo at sep and return sep + everything after.
```py3
>>> from threefive import Cue
>>>> cue=Cue()
>>>> cue.idxsplit("Hello","e")
'ello'
>>>> cue.idxsplit("Hello","l")
'llo'
>>>> cue.idxsplit("Hello","w")
'Hello'
```
___
