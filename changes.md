
# [__Breaking News__]
* New stuff coming in threefive v3.1.7

* __threefive now parses ID3 streams for SCTE-35 in MPEGTS__. it's automatically detected, you don't need to do anything. SCTE-35 in a single ID3 packet and SCTE-35 spread over multiple ID3 packets are both supported. You can filter which pids are parsed for SCTE-35 with __Stream.decode_pids(list_of_pids)__

* __IFramer is being merged into the Stream class__.
* to get a list of iframes in a stream call __Stream.iframes()__
```py3
>>>> from threefive import Stream
>>>> strm = Stream('video.ts')
>>>> strm.iframes()
[69367.058844, 69368.978844, 69370.898844, 69372.818844, 69374.738844, 69376.658844, 69378.578844, 69380.498844, 69382.418844, 69384.338844, 69386.258844, 69388.178844, 69390.098844, 69392.018844, 69393.938844, 69395.858844, 69397.778844, 69399.698844, 69401.618844, 69403.538844, 69405.458844, 69407.378844, 69409.298844, 69411.218844,
... ]
```
* __Stream.next_iframe()__ gives you the next iframe, works for the first iframe as well.
```py3
>>>> from threefive import Stream
>>>> strm = Stream('video.ts')
>>>> strm.next_iframe()
69367.058844
>>>> strm.next_iframe()
69368.978844
```
* __To Not use a UPID__ in a __Segmentation Descriptor__, set __segmentation_upid_length__, OR  __segmentation_upid_type__  to __0__. 

* __On the Windows platform__, __piping__ data into the __threefive cli tool__ should now work. __The select call has been removed__. 
___




# [ version ]

### latest threefive version is _v3.1.5_
* There are no known issues with threefive v3.1.5
* Average cyclomatic complexity: __A (1.990)__
* Pylint: __9.69/10.0__
* __threefive is dumping mmap.__. The way threefive parses packets seems to make mmap use fifteen times as much memory as without mmap. 
* Here's a list of __what's been fixed.__
	* __AacParser__ The typo on the call to __AacParser.not_syncsafe()__ has been fixed.
	* __Property class__ for __SCTE-35-2 Event Descriptors__ now render __JSON__ correctly.  
	* __Segmentation Descriptors without UPIDS__
 		* threefive will no longer throw an exception on SegmentationDescriptors without a UPID if __segmentation_upid_type__ is not set to __0__. 
		* if __segmentation_upid_length is set to 0__, threefive will print a warning message and set __segmentation_upid_type__ to __0__ for you.
	* __threefive.xml.Node__
        * __Node.addchild(obj,slot=0)__ _(slots allow you to set the index of a child in Node.children when adding a child)._
        * New method __Node.a2c()__ converts attributes to children.
        * New method __Node.c2a()__ converts children to attributes.
   * __UltraXmlParser__ has been renamed __XmlP__ and moved from threefive/uxp.py to threefive.xml.py. 
___
