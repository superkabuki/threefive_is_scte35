# Examples

* `aac_id3header.py` - use the __threefive.aac.AacParser__ class to parse __HLS AAC__ segments for __PTS__ in __ID3 header tags__.
* `id3.aac` test file for __aac_id3header.py__
* `base64toxmlbin.py`- __convert__ __base64__ encoded __SCTE-35__ to __xml+binary__ encoded SCTE-35 and back.
  
* `cue2vtt.py` - display __SCTE-35__ data on video using __WebVTT__ subtitles to __verify__ __SCTE-35__ __splice points__.

* `decodenext.py` - parse __MPEGTS__ streams for __SCTE-35__ using __Stream.decode_next()__.

* `dtmf.py` - parse __base64__ __SCTE-35__ with a __DTMF__ descriptor and __re-encode__ to __SCTE-35__ in __Hex__ format.

* `edit_break_duration.py` - change the __SCTE-35__ __break duration__ and __re-encode__ __SCTE-35__.

* `encode_time_signal.py` - __encode__ a __SCTE-35__ __Cue__ with a __TimeSignal__ from scratch.

* `parsehlstags.py` - use the __TagParser__ class to parse __HLS tags__ from a __m3u8__ file and group the tags by segment.

* `proxy.py` - how to use the __Stream.proxy()__ method for parsing __SCTE-35__ and __piping__ video.

* `quickstream.py` - how to __add SCTE-35 parsing__ for __MPEGTS__ streams to __your application__.

* `spliceinsert.py` - a __SCTE-35__ __Splice Insert__ example.  
