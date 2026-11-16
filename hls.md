# [threefive and HLS SCTE-35]
* parsing SCTE-35 in HLS with threefive is easy.
* threefive supports single rendition and multi-rendition(maaster.m3u8)
* Just pass the uri to threefive
```py3
 threefive https://demo.unified-streaming.com/k8s/live/scte35.isml/.m3u8
```
___

### [ hls profile ]
* these are the settings for parsing SCTE-35 in HLS. this is optional.
*  __the default profile will work for most people__

<img width="799" height="177" alt="image" src="https://github.com/user-attachments/assets/4fd04331-83d8-47b9-8b82-2b965dda5845" />

* to edit the profile settings, generate a hls.profile file and edit the file.
 
```py3
threefive hls profile

 vi hls.profile 
```

* hls.profile
```cobol
expand_cues = False
parse_segments = True
parse_manifests = True
hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,#EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
command_types = 0x6,0x5
descriptor_tags = 0x2

```
* __expand_cues__ - When True SCTE-35 Cue data will be displayed in JSON when found. Default False.
* __parse_segments__ - When True MPEGTS segments will be parsed for SCTE-35. __Default True__.
* __parse_manifests__ - When True HLS tags are parsed from the HLS Manifest. __Default True__.
* __hls_tags__ - A list of hls_tags to be used for splice points. __Default is all of the tags__.
* __command_types__ - A list of Splice Commands Types to be parsed. __Default is 0x06, 0x05__ ( Splice Insert, TimeSignal)
* __descriptor_tags__ - A list of Splice Descriptors to be parsed. __Default is 0x02__ ( Segmentation Descriptor)
