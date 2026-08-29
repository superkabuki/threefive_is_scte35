# [ The problem with SCTE-35 and HLS ]
 
*	The SCTE-35 specification specifies SCTE35 HLS tags for SCTE-35 in HLS. 
*	The HLS specification specifies DateRange HLS tags for SCTE-35 in HLS. 
*	The most commonly used HLS tags for SCTE-35 in HLS are from an old Adobe specification, and completely ignored in both the SCTE-35 and HLS specifications.
* SCTE-35 can be also be embedded in the video segments, with or without any HLS tags.


## threefive supports HLS SCTE-35 in every way possible. 
	Most of the options presented here are for filtering the SCTE-35 data to what you need,	
	By default, threefive parses everything. 


# [ threefive hls ]

* threefive hls is a HLS SCTE-35 parser. It takes a rendition or master m3u8 as input. 
* Automatic AES decryption for segments.
* Automatic AAC and AC3 ID3 Tag sync safe timestamp header parsing for audio only renditions.
* SCTE-35 Can be parsed from MPEGTS segments and from m3u8 files. 
* All HLS SCTE-35 tags are supported. 
* threefive hls also allows you to filter SCTE-35 Messages.

# [ Help ]

  To display this help:
  
```rebol
	threefive hls help
```

# [ Input ]

* threefive hls takes an m3u8 URI as input.
* M3U8 formats supported:
  * master  ( When a master.m3u8 used, threefive hls parses the first rendition it finds )
  * rendition
  
* Segment types supported:
    * AAC
    * AC3
    * MPEGTS
    * MP4
    * fMP4
    
* Protocols supported:
  * stdin
  * file
  * HTTP(S)
  * Multicast
  * Secure Reliable Transport
  * UDP Unicast

* Encryption supported:
    * AES-128 (segments are automatically decrypted)

# [ SCTE-35 ]

  threefive hls displays SCTE-35 Embedded Cues as well as SCTE-35 HLS Tags.

* Supported HLS Tags
  * #EXT-OATCLS-SCTE35
   * #EXT-X-CUE-OUT-CONT
  * #EXT-X-DATERANGE
  * #EXT-X-SCTE35
  * #EXT-X-CUE-IN
  * #EXT-X-CUE-OUT

# [ SCTE-35 Parsing Profiles ]

  SCTE-35 parsing can be fine tuned by setting a parsing profile.

  running the command:

            threefive hls profile

  will generate a default profile and write a file named hls.profile
  in the current working directory.
```rebol
    a@fu:~$ cat hls.profile

    expand_cues = False
    parse_segments = False
    parse_manifests = True
    hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,
    #EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
    command_types = 0x6,0x5
    descriptor_tags = 0x2
    starts = 0x22,0x30,0x32,0x34,0x36,0x44,0x46
```
*  Integers are show in hex (base 16), base 10 unsigned integers can also be used.

* `expand_cues`:       set to True to show cues fully expanded as JSON
  
* `parse_segments`:    set to true to enable parsing SCTE-35 from MPEGTS.
  
* `parse_manifests`:   set to true to parse the m3u8 file for SCTE-35 HLS Tags.

* `hls_tags`:          set which SCTE-35 HLS Tags to parse.
   
* `command_types`:     set which Splice Commands to parse.
    
* `descriptor_tags`:   set which Splice Descriptor Tags to parse.
  
* `starts`:            set which Segmentation Type IDs to use to start breaks.

  Edit the file as needed and then run threefive hls.

# [ Profile Formatting Rules ]

* Values do not need to be quoted.
* Multiple values are separated by a commas.
 * No partial line comments. Comments must be on a separate lines.
 * Comments can be started with a # or //
* Integers can be base 10 or base 16

# [ Output Files ]

* Created in the current working directory
* Clobbered on start of showcues
* __hls.m3u8__  - live playable rewrite of the m3u8 with the profile SCTE-35 rules.
* __hls.sidecar__ - list of ( pts, HLS SCTE-35 tag ) pair
* __hlsflat.m3u8__  - hls live streams are flattened out into a vod playlist.
  * When the live m3u8  first loads, every line is written to __hlsflat.m3u8__
  * Wnen a live m3u8 is reloaded, everything except the headers is appended to __hlsflat.m3u8__.
  	* __This give you a local playable VOD style m3u8, even from live sources__. 

# [ Cool Features ]

* threefive hls can resume when started in the middle of an ad break.
```rebol
            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067
```

# [ Example Usage ]

* Show this help:
```rebol
         threefive hls help
```
* Generate a new hls.profile:
```rebol
        threefive hls profile
```
* parse an m3u8:
```rebol
        threefive  https://example.com/out/master.m3u8
```
