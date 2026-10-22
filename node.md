### If you just want to parse SCTE-35 from Xml, you can just pass Xml directly to a Cue instance
```py3
from threefive import Cue
event=""" <Event presentationTime="1725946427520" duration="38400" id="14268737">
....          <Signal>
....             <Binary>/DAgAAAAAAAAAP/wDwUA2blBf//+ADS8AMAAAAAAAORhJCQ=</Binary>
....          </Signal>
....       </Event>
.... """
>>>> cue=Cue(event)
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
        "crc": "0xe4612424"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 38.4,
        "splice_event_id": 14268737,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": []
}
```



# The Node Class 
#### _requires threefive v3.0.45_
The Node class for creating and modifying xml Nodes, it is not SCTE-35 specific so it can be used for anything.

### make a Node instance
```py3
>>>> from threefive.xml import Node
>>>> mynode=Node("MyNode")
>>>> mynode
<MyNode  />
```
### add a comment
```py3
>>>> mynode.addcomment("Hi Mom")
>>>> mynode
<MyNode >
   <!-- Hi Mom -->
</MyNode>
```
### make a Node instance with attributes
```py3
>>>> achild=Node("Child", attrs={"favColor":"green", "favNumber":13})
>>>> achild
   <Child favcolor="green" favnumber="13"/>
```

### add a child Node 
```py3
>>>> mynode.addchild(achild)
>>>> mynode
<MyNode >
   <!-- Hi Mom -->
   <Child favcolor="green" favnumber="13"/>
</MyNode>

```
### get a list of child nodes
```py3
>>>> mynode.children
[   <!-- Hi Mom -->
,    <Child favcolor="green" favnumber="13"/>
]
>>>> 
```

#### __Parse a DASH mpd__
* use __Ultra Xml Parser__ (_Supreme_)
    * Ultra Xml Parser parses SCTE-35
```py3

a@fu:~/threefive$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u3, Dec 30 2024, 22:36:23)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>>> from threefive import reader
>>>> from threefive.uxp import UltraXmlParser

>>>> data = reader('/home/a/fu.mpd').read()

>>>> u = UltraXmlParser()  # <---   use Ultra Xml Parser 
>>>> n =u.parse(data)     # <--- UltraXmlParser.parse(data) returns a Node instance
```
### Parse SCTE-35 from Xml and convert to JSON


#### __search recursively for Event tags in the MPD xml__
* __Node.findtag(tag)__ returns a NodeList instance, so you can modify the Xml if needed.

 ```py3

>>>> events = n.findtag("Event")

>>>> events
[         <Event presentationTime="1725946427520" duration="0.426667" id="14268737">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blBf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946548480" duration="0.426667" id="14268738">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blCf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946669440" duration="0.426667" id="14268739">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blDf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946790400" duration="0.426667" id="14268740">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blEf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725946911360" duration="0.426667" id="14268741">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blFf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
,          <Event presentationTime="1725947032320" duration="0.426667" id="14268742">
            <Signal>
               <Binary>/DAgAAAAAAAAAP/wDwUA2blGf//+ADS8AMAAAAAAAORhJCQ=</Binary>
            </Signal>
         </Event>
]
```
#### Get the attributes and the value of the Binary node for each event.
```py3
>>> for e in events: print(e.attrs, e.children[0].children[0].value)
... 
{'presentation_time': 1725946427520, 'duration': 38400, 'id': 14268737} /DAgAAAAAAAAAP/wDwUA2blBf//+ADS8AMAAAAAAAORhJCQ=
{'presentation_time': 1725946548480, 'duration': 38400, 'id': 14268738} /DAgAAAAAAAAAP/wDwUA2blCf//+ADS8AMAAAAAAAORhJCQ=
{'presentation_time': 1725946669440, 'duration': 38400, 'id': 14268739} /DAgAAAAAAAAAP/wDwUA2blDf//+ADS8AMAAAAAAAORhJCQ=
{'presentation_time': 1725946790400, 'duration': 38400, 'id': 14268740} /DAgAAAAAAAAAP/wDwUA2blEf//+ADS8AMAAAAAAAORhJCQ=
{'presentation_time': 1725946911360, 'duration': 38400, 'id': 14268741} /DAgAAAAAAAAAP/wDwUA2blFf//+ADS8AMAAAAAAAORhJCQ=
{'presentation_time': 1725947032320, 'duration': 38400, 'id': 14268742} /DAgAAAAAAAAAP/wDwUA2blGf//+ADS8AMAAAAAAAORhJCQ=


```

#### __These events can be modified or deleted and the changes applied in real time.__

```py3

>>>> events  = n.findtag("Event")

>>>> len(events)
6

>>>> events.pop()
>>>> len(events)
5

>>>> events.pop(0)
>>>> len(events)
4
```

#### you can also search with _Node.findattr(attr)_ for xml nodes that have an attribute

```py3
>>>> bwidth_nodes=n.findattr("bandwidth")
>>>> bwidth_nodes
[<Representation   id="audio_eng" bandwidth="128000"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```

#### __you can modify those nodes too.__
* Here I add an attribute to the first bwidth_node

```py3
>>>> bwidth_nodes[0].addattr("fu","2you")
>>>> bwidth_nodes
[<Representation   id="audio_eng" bandwidth="128000" fu="2you"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```
* __access the parent__
* _You can also chain parents like bwidth_nodes[0].parent.parent_

```py3
>>>> bwidth_nodes[0].parent    

<AdaptationSet   id="1" group="1" contentType="audio" lang="en" segmentAlignment="true" audioSamplingRate="48000" mimeType="audio/mp4" codecs="mp4a.40.2" startWithSAP="1">
   <AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="1"/>
   <Role schemeIdUri="urn:mpeg:dash:role:2011" value="main"/>
   <SegmentTemplate timescale="48000" startNumber="898930439" initialization="scte35-$RepresentationID$.dash" media="scte35-$RepresentationID$-$Time$.dash">
      <SegmentTimeline>
         <S t="82845429166080" d="92160" r="311"/>
      </SegmentTimeline>
   </SegmentTemplate>
   <Representation id="audio_eng" bandwidth="128000" fu="2you"/>
</AdaptationSet>
````

#### __go crazy with namespaces__
    * namespaces can be set from the top, or by node.
    *  namespaces can set on tags and/or attributes.
<br><br>

* set the namespace on the first node

```py3
>>>> bwidth_nodes[0].namespace.ns="supercool"
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```

* set the second node to a different namespace

```py3
>>>> bwidth_nodes[1].namespace.ns="hottamale"
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <hottamale:Representation   id="video" bandwidth="1000000" scanType="progressive"/>
]
```

* apply the namespace to the attributes the second node

```py3
>>>> bwidth_nodes[1].namespace.all = True
>>>> bwidth_nodes
[   <supercool:Representation id="audio_eng" bandwidth="128000" fu="2you"/>
, <hottamale:Representation   hottamale:id="video" hottamale:bandwidth="1000000" hottamale:ScanType="progressive"/>
]
```
### Turn attributes into child nodes, recursively.
```py3
>>>> from threefive.xml import Node
>>>> n=Node("root", attrs={"one":1,"two":2,"three":3,})
>>>> n
<root one="1" two="2" three="3"/>

>>>> n2=Node("next",attrs={"four":4,"five":5,})
>>>> n.addchild(n2)
>>>> n
<root one="1" two="2" three="3">
    <next four="4" five="5"/>
</root>

>>>> n.a2c()
>>>> n
<root>
    <next>
        <four>4</four>
        <five>5</five>
    </next>
    <one>1</one>
    <two>2</two>
    <three>3</three>
</root>


```

*  __threefive v3.1.5__ can make children into attributes with __Node.c2a()__
```py3
>>>> n.c2a()
>>>> n
<root one="1" two="2" three="3">
    <next four="4" five="5"/>
</root>

```
### Help is built-in

```py3
Help on class Node in module threefive.xml:

class Node(builtins.object)
 |  Node(tag, value='', attrs=None, ns=None)
 |  
 |  The Node class is to create an xml node.
 |  
 |  An instance of Node has:
 |  
 |      tag :      <tag> </tag>
 |      value  :    <tag>value</tag>
 |      attrs :     <tag attrs[k]="attrs[v]">
 |      children :  <tag><children[0]></children[0]</tag>
 |      depth:      tab depth for printing (automatically set)
 |      namespace:    a NameSpace instance for the Node
 |  
 |  Use like this:
 |  
 |      from threefive.xml import Node
 |  
 |      ts = Node('TimeSignal')
 |      st = Node('SpliceTime',attrs={'pts_time':3442857000})
 |      ts.addchild(st)
 |      print(ts)
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tag, value='', attrs=None, ns=None)
 |  
 |  __repr__(self)
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

#### Namespaces
threefive.xml.Node __implements namespaces via the embedded NameSpace class__
<br> Namespaces can be set,changed or disabled for the entire Xml, or by individual Nodes. <br>
The namespace Uri can be set, changed, or disabled. <br>
A namespace can also be set, changed, or disabled on Node attributes.

#### Entity Expansion.
I am considering how to do entity expansion safely, <br>
__I'm going to limit size and not allow repeating entities for the same value.__ <br>
Not allowing repeated entities will stop most entity expansion hacks. 
<br>
__If you have a better idea, speak up.__

#### DTD Validation. 
Currently, __I have no plans to implement DTD validation.__  <br>
The SCTE-35 data is validated by threefive already, <br>
and I don't see the benefit of validating other DTDs, <br>
there are plenty of other tools for that sort of thing.


