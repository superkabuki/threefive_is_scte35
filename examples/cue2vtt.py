"""
cue2vtt.py

uses webvtt subtitles to display SCTE-35

Usage:

pypy3 cue2vtt.py thevideo.ts | mplayer thevideo.ts -sub -

"""

import sys
import time
from threefive import Stream


def first():
    global start_pts
    st = Stream(sys.argv[1])
    start_pts = st.next_iframe()


def ts_to_vtt(timestamp):
    """
    ts_to_vtt converts timestamp into webvtt times
    """
    timestamp -= start_pts
    hours, seconds = divmod(timestamp, 3600)
    mins, seconds = divmod(seconds, 60)
    seconds = round(seconds, 3)
    return f"{int(hours):02}:{int(mins):02}:{seconds:02}"


def scte35_to_vtt(cue):
    """
    scte35_to_vtt prints SCTE-35 via webvtt
    """
    cue_start = 0
    cue_end = 0
    du
    pts_time = None
    upid = None
    seg_mesg = None
    now = cue.packet_data.pts
    if cue.command.has("pts_time"):
        cue_start = cue.command.pts_time + cue.info_section.pts_adjustment
    else:
        cue_start = now
    #    if cue_start > now:
    #       time.sleep(cue_start - now)
    if cue.command.has("break_duration"):
        duration = cue.command.break_duration
    for d in cue.descriptors:
        if d.has("segmentation_duration"):
            duration = d.segmentation_duration
            if d.has("segmentation_upid"):
                upid = d.segmentation_upid
            if d.has("segmentation_message"):
                seg_mesg = d.segmentation_message
    if cue_start:
        cue_end = cue_start + 2
    ##    if cue_end == 0:
    ##        end = start + 4

    print(f"{ts_to_vtt(cue_start)} --> {ts_to_vtt(cue_end)} ")

    print(f"Cmd: {cue.command.name}    ")
    pts_time = None
    if cue.command.pts_time:
        pts_time = cue.command.pts_time + cue.info_section.pts_adjustment
    else:
        pts_time = now
    print(f"PTS:  {pts_time}  ")
    if duration:
        print(f"Duration:  {round(duration,3)} ")
    if seg_mesg:
        print(seg_mesg)
    if upid:
        print(f"Upid: {upid}")
    print()


if __name__ == "__main__":
    arg = sys.argv[1]
    first()
    print("WEBVTT\n\n\n")
    strm = Stream(arg)
    strm.decode(func=scte35_to_vtt)
