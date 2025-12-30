"""
next.py demonstrates how to use Stream.decode_next() to grab and process
the next SCTE-35 Cue in an MPEGTS stream.

Here, if the Cue Splice Command is a Splice Insert, we print the Splice Command vars,
but you trigger any action you like, this is just an example. 

"""

import sys
from threefive import Stream


def do():
    arg = sys.argv[1]
    strm =Stream(sys.argv[1])
    for cue in strm.decode_next():
        cue.show()


if __name__ == "__main__":
    do()
