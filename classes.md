# threefive commonly used classes. 
#### threefive is Object Oriented. Almost all of threefive is contained in classes. Inheritance is intentionally shallow.  
### The Cue class and the Stream class will be used most often.
<br>

# SCTE-35 Specific Stuff
### Most SCTE-35 objects are subclassed from SCTE35Base
* SCTE35Base
    * [__Cue__](threefive/cue.py)
    * [SpliceInfoSection](threefive/section.py) 
    * [SpliceCommand](threefive/commands.py)
        * BandwidthReservation
        * PrivateCommand
        * SpliceNull
        * TimeSignal
            * SpliceInsert
   * [SpliceDescriptor](threefive/descriptors.py)
        * AvailDescriptor
        * DtmfDescriptor
        * EventDescriptor
        * DVBDASDescriptor
        * Property
        * SegmentationDescriptor 
        * TimeDescriptor

## All upids are either Upid instances or a subclass of Upid.
* [Upid](threefive/upids.py)
    * AirId
    * Atsc
    * Mid
    * Mpu
    * Eidr
    * NoUpid
    * Isan
    * Umid

# SCTE-35 Related stuff
### Most MPEGTS parsers are either a Stream instance or subclass of Stream.
* [__Stream__](threefive/stream.py)
    * [Segment](threefive/segment.py)
    * [SixFix](threefive/sixfix.py)
       * [SuperKabuki](threefive/superkabuki.py)

### Other MPEGTS classes.
* [IFramer](threefive/iframes.py)
* Socked(socket.socket)
* PMT

### Multicast Sender/Server
* [GumS](threefive/gums.py)

### HLS related classes 
* [AacParser](threefive/aac.py)
* [HlsParser Pretty slick HLS with a strong SCTE-35 focus](threefive/hls.py)
* [TagParser parse all present and future HLS tags. (I read the whole spec)](threefive/hlstags.py)

### Bitwise decoder and encoder classes, we don't need no stinking byte alignment, we slice by the bit.
* [Bitn a better struct (bit slicing)](threefive/bitn.py)
* [NBin struct in reverse](threefive/bitn.py)

### Xml
* [XmlP All purpose xml parser](threefive/xml.py)
* [NameSpace](threefive/xml.py)
* [Node an xml node, very complete.](threefive/xml.py)
    * [Comment](threefive/xml.py)
* [NodeConverter scte-35 specific xml parsing](threefive/xml2scte35.py)
* [NodeList A list of Node instances](threefive/xml.py)
