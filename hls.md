# [ The problem with SCTE-35 and HLS ]
<pre> 
	The SCTE-35 spec uses the SCTE35 HLS tags. 
	
	The HLS spec uses the DateRange HLS tags for SCTE-35. 

	The mosty commonly used SCTE-35 HLS tags are actually from an old Adobe specification, 
and not officially acknowledged by the SCTE-35 or HLS spec. 
	
	To make it just a little bit more confusing, SCTE-35 can be also be embedded in the video segments, 
with or without any HLS tags.

</pre>
# Don't worry man, threefive supports HLS SCTE-35 in every way possible. 
<pre>
	Most of the options presented here are for filtering the SCTE-35 data to what you need,
	
	By default, threefive parses everything. 
	
</pre>

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
    *codecs:
      * video
         * mpeg2, h.264, h.265
        * audio
          * mpeg2, aac, ac3, mp3
* Protocols supported:
  * file
  * http(s)
  * UDP
  * Multicast

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
* Profile rules applied to the output:
* hls.m3u8  - live playable rewrite of the m3u8 with the profile SCTE-35 rules.
* hls.sidecar - list of ( pts, HLS SCTE-35 tag ) pairs

### Profile rules not applied to the output:

* hlsflat.m3u8  - hls live streams are flattened out into a vod playlist.
  When the live m3u8  first loads, every line is written to hlsflat.m3u8
  Wnen a live m3u8 is reloaded, everything except the headers
  is appended to hlsflat.m3u8. This give you a VOD style m3u8
  so you can fast forward or rewind while playing.
   GREAT for debugging SCTE-35 live hls.

# [ Cool Features ]

* threefive hls can resume when started in the middle of an ad break.
```rebol
            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067
```
* mpegts streams are listed on start ( like ffprobe )
```rebol
        Program: 1
            Service:
            Provider:
            Pid:	480
            Pcr Pid:	481
            Streams:
                Pid: 481[0x1e1]	Type: 0x1b AVC Video
                Pid: 482[0x1e2]	Type: 0xf AAC Audio
                Pid: 483[0x1e3]	Type: 0x86 SCTE35 Data
                Pid: 484[0x1e4]	Type: 252 Unknown
                Pid: 485[0x1e5]	Type: 0x15 ID3 Timed Meta Data
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
