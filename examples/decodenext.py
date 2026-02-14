"""
next.py demonstrates how to use Stream.decode_next() to grab and process
the next SCTE-35 Cue in an MPEGTS stream.

threefive.Stream.decode_next() is a python generator that yields a cue
when it finds one

once you have a cue, you can show it, or pass it to another function or method

Below,
    when a cue is found,
    if the splice command has the pts_time,
    print the splice command name and pts_time
   else print just the splice command name

"""

import sys
from threefive import Stream


def do():
    arg = sys.argv[1]
    strm = Stream(sys.argv[1])
    for cue in strm.decode_next():
        cmd = f"Command: {cue.command.name}"
        if cue.command.has("pts_time"):
            cmd += f"\t pts: {cue.command.pts_time}"
        print(cmd)


if __name__ == "__main__":
    do()
