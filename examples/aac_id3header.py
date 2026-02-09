#!/usr/bin/env python3
"""
aac_id3header.py

Use threefive.aac.AacParser class to 
parse HLS aac segments for PTS in ID3 header tags. 
try it with id3.aac in this same directory
like:

  python3 aac_id3header.py id3.aac

PTS : 82276.680533



"""
import sys
from threefive.aac import AacParser

ap = AacParser()
#  this is an HLS audio only segment with PTS in an ID3 header tag.
url = sys.argv[1]
pts = ap.parse(url)
print(f"PTS : {pts}")
