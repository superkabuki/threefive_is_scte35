
# threefive.Cue Class

## class threefive.Cue(data=None, packet_data=None)

    The threefive.Cue class handles parsing individual SCTE 35 Cues
```rebol
        import threefive
        Base64 = “/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=”
        cue = threefive.Cue(Base64)
        cue.show()
```

*        A cue instance can be initialized with Base64, Bytes, Hex, Int, Json, or Xml+binary data.

*        Instance variables can be accessed via dot notation.
```rebol
>>>> cue.command

    {‘command_length’: 5, ‘name’: ‘Time Signal’, ‘time_specified_flag’: True, ‘pts_time’: 21695.740089}

>>>> cue.command.pts_time

    21695.740089
```


| Cue methods       | details                                                 |
|-------------------|---------------------------------------------------------|
| base64()          | converts SCTE35 data to a base64 encoded string.        |
| bytes()           | return SCTE35 data as bytes                             |
| decode()          |  parses for SCTE35 data *decode doesn’t need to be called directly unless you initialize a Cue without data.                   |
| encode()          |   alias for base64()                                    |
|encode_as_hex()    |   alias for hex()                                       |
| encode_as_int()   |   alias for int()                                       |
| fix_bad_b64(data) |  fixes bad padding on Base64 string data.               |
|  get()            |  returns the SCTE-35 Cue data as a dict of dicts.       |
| get_descriptors() |  returns a list of SCTE 35 splice descriptors           |
| hex()             | returns SCTE35 data as hex                              |
| int()             | returns SCTE35 data as Int                              |
| load()            | loads SCTE35 data as dict,json, or xml into Cue instance|
| xml()             | return SCTE35 data as Xml                               |
| xmlbin()          |  return SCTE35 as Xml+binary                            |

    
