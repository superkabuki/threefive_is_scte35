"""
parsehlstags.py
Use the TagParser class to parse hls tags from a m3u8 file
and group the tags into a dict by segment.

Example:
these are the tags for the segment index_2_8875296.ts

          "index_2_8875296.ts": {

               "#EXT-X-PROGRAM-DATE-TIME": "2024-11-24T15:24:42.700Z",

                "#EXT-X-CUE-OUT-CONT": {
                      "SCTE35":     "/DBAAAAAAyiYAAAABQb/FOWM0AAqAihDVUVJ/////3//AAFJi8ABFG1zbmJjX0VQMDM0NDY3MTkxMDY5IgIEbMGIMA=",
                      "Duration":     239.967,
                      "ElapsedTime":    238.867,
                      "CAID":  624854195548842227305490153684004159669692020281
                },

            "#EXTINF":  1.133
          },
"""

import json
import sys
from threefive.hlstags import TagParser,HEADER_TAGS
from threefive.new_reader import reader

headers=[]
data = {}
for arg in sys.argv[1:]:
    with reader(arg) as mu:
        results = []
        lines = mu.readlines()
        for line in lines:
                line=line.decode()
                if line.startswith("#"):
                    for tag in HEADER_TAGS:
                        if tag in line:
                            headers.append(line)
                    if line not in headers:
                        # hold tags until we find a segment
                        results.append(line)         
                else:
                    if line:
                        if headers:
                            data['HEADER TAGS']=TagParser(headers).tags
                            headers=[]          
                        tp = TagParser(results)
                        # when we find a segment, make it a key in data
                        # and a dict of the tags as the value
                        # trim down to just the file name.
                        line = line.rsplit("/", 1)[-1].split("?", 1)[0].strip()
                        if line:
                             # segment name is the key and the tags are the value.
                            data[line] = tp.tags
                            # clear results for next segment
                            results = []
    if data:
        print(json.dumps(data, indent=4))
