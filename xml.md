# Xml

### [decoding](#decoding)

### [encoding](#encoding)

### [namespaces](namespaces)

### [threefive.xml.Node class](node.md)

# How does SCTE-35 Xml work with threefive?

# Decoding 
### Cli
```js
a@fu:~/threefive$ cat ~/xml3.xml

<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="false" eventIdComplianceFlag="true" availNum="1" availsExpected="1" outOfNetworkIndicator="true" uniqueProgramId="39321">
      <scte35:Program>
         <scte35:SpliceTime ptsTime="6554297154"/>
      </scte35:Program>
      <scte35:BreakDuration autoReturn="true" duration="10798788"/>
   </scte35:SpliceInsert>
   <!-- Provider Placement Opportunity Start -->
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="93" segmentNum="0" segmentsExpected="0" subSegmentNum="0 subSegmentsExpected="0" segmentationDuration="10800000">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- Type 0x01 is deprecated, use MPU type 0x0C -->
      <scte35:SegmentationUpid segmentationUpidType="1" segmentationUpidFormat="hexbinary">futronica</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
* decode the xml into json and write to a file
* threefive outputs SCTE-35 data to stderr aka 2 , stdout is used for piping video and such.
  ```js
  threefive < ~/xml3.xml 2> json.json
  ```
* decode the xml into hex
  ```js
  threefive < ~/xml3.xml hex
  0xfc303a00000003289800fff00f05000000017faffe00a4c6c499990101001a021843554549000000007f800109667574726f6e6963615d0000a6ac3c8d

  ```
### lib
* read the xml data in from a file
```py3
>>>> from threefive import reader
>>>> data = reader('/home/a/xml5.xml').read()
```
* load the data into a Cue instance
```py3
>>>> from threefive import Cue
>>>> cue=Cue(data)
```
* to see the data, call cue.show()
```py3
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 42,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x98767c66"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": false,
        "break_duration": 75.0,
        "splice_event_id": 18,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": false,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "event_id_compliance_flag": true,
        "unique_program_id": 1,
        "avail_num": 18,
        "avails_expected": 255
    },
    "descriptors": [
        {
            "tag": 0,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 18,
            "descriptor_length": 8
        }
    ]
}
```


# Encoding 
### Cli
* Encoding with the cli is easy, pass your SCTE-35 data to threefive and just add the xml keyword
* if you had SCTE-35 in JSON format in a file like this
```js
a@fu:~/threefive$ cat ~/json2.json
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 52,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 2.3,
        "cw_index": "0x0",
        "tier": 4095,
        "splice_command_length": 10,
        "splice_command_type": 5,
        "descriptor_loop_length": 25,
        "crc": "0xe2f9395d"
    },
    "command": {
        "command_length": 10,
        "command_type": 5,
        "name": "SpliceInsert",
        "splice_event_id": 1,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": false,
        "program_splice_flag": false,
        "duration_flag": false,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 39321,
        "avail_num": 1,
        "avails_expected": 255
    },
    "descriptors": [
        {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id": "0x0",
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": false,
            "archive_allowed_flag": false,
            "device_restrictions": "Restrict Group 0",
            "segmentation_message": "Provider Placement Opportunity End",
            "segmentation_type_id": 53,
            "segmentation_upid_length": 13,
            "segmentation_upid_type": 12,
            "segmentation_upid_type_name": "MPU",
            "segmentation_upid": {
                "format_identifier": "DOOM",
                "private_data": "5375706572446f6f6d"
            },
            "segment_num": 0,
            "segments_expected": 0,
            "descriptor_length": 23
        }
    ]
}
```
* to generate xml output
```js
a@fu:~/threefive$ threefive < ~/json2.json xml
```
```xml
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="1" availsExpected="255" outOfNetworkIndicator="false" uniqueProgramId="39321"/>
   <!-- Provider Placement Opportunity End -->    #<----- I add the segmentationType as a comment, because I'm old and lazy .
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="53" segmentNum="0" segmentsExpected="0">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- MPU -->   # <--------I add the Upid type as a comment, because I'm old and lazy.
      <scte35:SegmentationUpid segmentationUpidType="12" segmentationUpidFormat="hexbinary" formatIdentifier="1146048333" privateData="1539542133359170776941">444f4f4d5375706572446f6f6d</scte35:SegmentationUpid>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
* you can parse MPEGTS and output SCTE-35 as xml
```js
threefive video.ts xml
``` 
### lib
* If you want to make a TimeSignal
```py3
>>>> from threefive import TimeSignal, Cue
>>>> t =TimeSignal()
>>>> t
{'command_length': 0, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': None, 'pts_time': None}
```
* set the vars for the TimeSignal
```py3
>>>> t.time_specified_flag=True

>>>> t.pts_time=15345.123903
```
* render the TimeSignal as xml
```xml
>>>> t.xml()
<scte35:TimeSignal >
   <scte35:SpliceTime ptsTime="1381061151"/>
</scte35:TimeSignal>
```
* add the TimeSignal to a Cue and render as xml
*  (threefive automatically generates the Splice Info Section if needed)
*  __Notes__:
        *  __When you call Cue.xml() it returns a Node instance__
        *  __if you print Cue.xml() or a Node instance, you get the Xml string.__
  
```py3
>>>> cue=Cue()
>>>> cue.command =t
>>>> cue.encode()
>>>> print(cue.xml()) 
```
```xml
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="1381061151"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```
* make an Avail Splice Descriptor and add it to the Cue
```py3
>>>> from threefive import AvailDescriptor
>>>> avd =AvailDescriptor()
>>>> avd
{'tag': 0, 'identifier': 'CUEI', 'name': 'Avail Descriptor', 'bites': None, 'private_data': None, 'provider_avail_id': None}
>>>> avd.provider_avail_id="fumatica"
```
* __When you call encode() on a threefive object, it tells you if you've got something wrong__

```py3
>>>> avd.encode()
  provider_avail_id is fumatica, it should be type int, 32 bit(s) long.  # <--- threefive points out your mistakes
```
* __use dot notation to access the vars and make the changes__
```
>>>> avd.provider_avail_id=1234
>>>> avd.encode()
```
* append the Avail Splice Descriptor to cue.descriptors
* cue.descriptors is a list
```py3
>>>> cue.descriptors.append(avd)
```
* __When ever you make a change to cue, call cue.encode() and it recalculates the length vars and the CRC32.
```
>>>> cue.encode()
```
* print cue.xml() to see the new xml
```xml
>>>> print(cue.xml())
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="1381061151"/>
   </scte35:TimeSignal>
   <scte35:AvailDescriptor providerAvailId="1234"/>
</scte35:SpliceInfoSection>
```
# Namespaces
* The SCTE-35 spec is very non-commital on namespaces. You can use the SCTE35 namespace or not use it and you can use it on attributes or not.
* the SCTE35 schema uri is scte35="https://scte.org/schemas/35".
* When threefive outputs xml it includes the namespace and uri because it applies.
---
#### By default the namespace is set to scte35
```py3
>>>> from threefive import Cue
>>>> cue=Cue('/DAWAAAAAAAAAP/wBQb+ALKOoAAAJte19A==')
>>>> cue.xml()
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11701920"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```
#### The Cue.xml method accepts an optional ns arg
```py3
>>>> cue.xml(ns="supercool")
<supercool:SpliceInfoSection xmlns:supercool="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <supercool:TimeSignal>
      <supercool:SpliceTime ptsTime="11701920"/>
   </supercool:TimeSignal>
</supercool:SpliceInfoSection>
```
#### set ns to an empty string for no namespace
```py3
>>>> cue.xml(ns="")
<SpliceInfoSection xmlns="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="11701920"/>
   </TimeSignal>
</SpliceInfoSection>

```


  
### Q. What if I'm special and need to change the namespace uri?

### A.Then you can change it. I'll explain.

```py3
>>>> x = cue.xml()

>>>> x.namespace.uri
'https://scte.org/schemas/35'
>>>> x.namespace.uri="https://iodisco.com/boom"
>>>> x
<scte35:SpliceInfoSection xmlns:scte35="https://iodisco.com/boom"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11701920"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```

### if you pass in the above xml to a Cue instance, threefive will accept it, 
### but will change it to the schema used by threefive in xml output, as it's should.
```py3
>>>> cue2=Cue(x.mk())
>>>> cue2
>>>> cue2.xml()
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <scte35:TimeSignal>
      <scte35:SpliceTime ptsTime="11701920"/>
   </scte35:TimeSignal>
</scte35:SpliceInfoSection>
```
### Since Cue.xml returns a threefive.Node instance, you can easily change the uri, namespace or anything else
```py3
>>>> x2 = cue2.xml()
>>>> x2.namespace.uri="https://slo.me/adrianiscool"
>>>> x2.namespace.ns="fu"
>>>> x2
<fu:SpliceInfoSection xmlns:fu="https://slo.me/adrianiscool"  ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <fu:TimeSignal>
      <fu:SpliceTime ptsTime="11701920"/>
   </fu:TimeSignal>
</fu:SpliceInfoSection>
```
### set namespace on everything including attributes
```py3
>>>> x2.namespace.all=True
>>>> x2
<fu:SpliceInfoSection xmlns:fu="https://slo.me/adrianiscool"  fu:PtsAdjustment="0" fu:ProtocolVersion="0" fu:SapType="3" fu:tier="4095">
   <fu:TimeSignal>
      <fu:SpliceTime fu:PtsTime="11701920"/>
   </fu:TimeSignal>
</fu:SpliceInfoSection>
```
# RTFM
### help(threefive.xml.Node)
```py3
class Node(builtins.object)
 |  Node(tag, value='', attrs=None, ns=None)
 |  
 |      The Node class is to create an xml node.
 |  
 |      An instance of Node has:
 |  
 |          tag :      <tag> </tag>
 |  
 |          value  :    <tag>value</tag>
 |  
 |          attrs :     <tag attrs[k]="attrs[v]">
 |  
 |          children :  <tag><children[0]></children[0]</tag>
 |  
 |          depth:      tab depth for printing (automatically set)
 |  
 |          namespace:    a NameSpace instance for the Node
 |  
 |  example:
 |  
 |          >>> from threefive.xml import Node
 |          >>> ts = Node('TimeSignal')
 |          >>> st = Node('SpliceTime',attrs={'pts_time':3442857000})
 |          >>> ts.addchild(st)
 |          >>> print(ts)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tag, value='', attrs=None, ns=None)
 |  
  __repr__(self)
 |  
 |  a2c(self)
 |      a2c convert attrs to child nodes
 |  
 |  addattr(self, attr, value)
 |      addattr add an attribute
 |  
 |  addchild(self, child, slot=None)
 |      addchild adds a child node
 |      set slot to insert at index slot.
 |  
 |  addcomment(self, comment, slot=None)
 |      addcomment add a Comment node
 |  
 |  c2a(self)
 |      c2a convert children to attributes
 |      if the child has no attributes or children
 |  
 |  children_namespaces(self)
 |      children_namespaces give children your namespace
 |  
 |  drop(self, obj=None)
 |      drop delete self
 |  
 |  dropattr(self, attr)
 |      dropattr remove an attribute
 |  
 |  dropchild(self, child)
 |      dropchild remove a child
 |      
 |      example:
 |      a_node.dropchild(a_node.children[3])
 |  
 |  findattr(self, attr, obj=None)
 |      findattr  recursively searches children for all nodes that
 |      have an attribute that matches attr. findattr returns a NodeList.
 |  
 |  findtag(self, tag, obj=None)
 |      findtag  recursively searches children for
 |      all nodes with a tag that matches tag.
 |      findtag returns a NodeList.
 |  
 |  mk(self, obj=None)
 |      mk make the Node as xml.
 |  
 |  set_ns(self, ns=None)
 |      set_ns set namespace on the Node
 |  

```
### help(threefive.xml.Namespace)
```py3

Help on class NameSpace in module threefive.xml:

class NameSpace(builtins.object)
 |  NameSpace(ns=None, uri=None)
 |  
 |  Each Node instance has a NameSpace instance
 |  to track namespace settings.
 |  @ns is the name of the namespace
 |  @uri is the xmlns uri
 |  @all is a flag to signal that all elements and
 |  attributes will have the namespace prefixed.
 |  By default only  the elements are prefixed with the namespace.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, ns=None, uri=None)
 |  
 |  clear(self)
 |      clear clear namespace info
 |  
 |  prefix_all(self, abool=True)
 |      prefix_all takes a boolean
 |      True turns it on, False turns it off.
 |  
 |  xmlns(self)
 |      xmlns return xmlns attribute
 |  
 |  ----------------------------------------------------------------------
```



## threefive vs. Quadradic Blowup

* threefive detects the hack and stops it from being parsed. 
 
* [Code stolen from here](https://gist.github.com/jordanpotti/04c54f7de46f2f0f0b4e6b8e5f5b01b0)
 
<img width="1015" height="651" alt="image" src="https://github.com/user-attachments/assets/cbac313f-bf93-431d-9244-22bf9cff3d97" />

