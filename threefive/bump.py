#!/usr/bin/env python3

"""
threefive/bump.py

provides the function bumped to adjust pts in a SCTE-35 MPEGTS packet
bumped takes a packet and a float that is the amount to adjust  the SCTE-35 pts,

if the Cue in the packet has cue.command.pts_time:

    cue.command.pts_time is adjusted directly  like this:

   1)   cue.command.pts_time = secs + cue.info_section.pts_adjustment+ cue.command.pts_time

  2)  cue.info_section.pts_adjustment = 0.0

  3) if  a negative adjustement is used and cue.command.pts_time reults in a negative pts,
   then pts_time = ROLLOVER + negative_pts.

    For example if cue.command.pts_time =5000.0 and the adjustment is -8000.0
     5000.0 + (-8000.0)= -3000.0
     ROLLOVER +( -3000.0) = 92443.717678
     cue.command.pts_time would be set to 92443.717678


if the Cue in the packet doesn't have cue.command.pts_time:

   1)     cue.info_section.pts_adjustment=secs + cue.info_section.pts_adjustment



final values are modolo`ed to the ROLLOVER.

you just need one function call ,bump.

example:
                >>> from threefive import bump
                >>> bump(infile,outfile,secs)

"""

import argparse
import sys

from .cue import Cue
from .stuff import blue, pif
from .stream import Stream


ROLLOVER = 95443.717678
REV = "\033[7m"
NORM = "\033[27m"


class StreamBumper(Stream):
    """
        StreamBumper class

            Adjust SCTE-35 PTS times  in MPEGTS

    example:
                    >>> from threefive.bump import StreamBumper
                    >>> sb=StreamBumper()
                    >>> sb.infile = "input.ts"
                    >>> sb.outfile = "output.ts"
                    >>> sb.secs = 100.123
                    >>> sb.bump()

    """

    def __init__(self, tsdata=None, show_null=True):
        super().__init__(tsdata)
        self.outfile = sys.stdout.buffer
        self.infile = None
        self.secs = 0.0
        self._parse_args()

    @staticmethod
    def _show_bump():
        """
        _show_bump show the Cue with adjusted pts.
        """
        blue("Cue adjusted")

    @staticmethod
    def _repad(pkt):
        """
        _repad add padding to packet as needed.
        """
        pad = b"\xff"
        padsize = 188 - len(pkt)
        pkt = pkt + (pad * padsize)
        return pkt

    def bump(self):
        """
        bump adjust pts of the SCTE-35 by secs
        """
        num_pkts = 2420
        with open(self.outfile, "wb") as outfile:
            for chunk in self.iter_pkts(num_pkts):
                pkts = [
                    self._parse2(chunk[i : i + self.PACKET_SIZE])
                    for i in range(0, len(chunk), self.PACKET_SIZE)
                ]
                outfile.write(b"".join(pkts))
                outfile.flush()
        return False

    def _scte35(self, pkt, pid):
        if pid in (self.pids.scte35 or self.pids.maybe_scte35):
            pkt = self._bumped(pkt)
        return pkt

    def _parse2(self, pkt):
        """
        parse packets for tables and SCTE-35,
        adjust SCTE-35 PTS by secs.
        return modified pkt.
        """
        pid = self._parse_info(pkt)
        pkt = self._scte35(pkt, pid)
        return pkt

    def _bump_pts_time(self, cue):
        """
        _bump_pts_time add secs directly to cue.command.pts_time
        """
        bumpme = cue.command.pts_time + cue.info_section.pts_adjustment + self.secs
        cue.info_section.pts_adjustment = 0.0
        if bumpme < 0.0:
            bumpme = ROLLOVER + bumpme
        cue.command.pts_time = bumpme % ROLLOVER

    def _bump_pts_adjust(self, cue):
        """
        _bump_pts_adjust add secs to cue.command.pts_adjustment
        """
        bumpme = cue.info_section.pts_adjustment + self.secs
        cue.info_section.pts_adjustment = bumpme % ROLLOVER

    def _bump_pts(self, pay):
        """
        _bump_pts adjust SCTE-35 pts by secs
        """
        cue = Cue(pay)
        if cue.command.pts_time:
            self._bump_pts_time(cue)
        else:
            self._bump_pts_adjust(cue)
        cue.encode()
        self._show_bump()
        return cue.bytes()

    def _bumped(self, pkt):
        """
        _bumped adjust the pts_time in the Cue in the pkt by secs,
        secs is a float in seconds.
        """
        if b"\xfc" in pkt:
            pre = pkt.split(b"\x00\x00\x01\xfc")[-1]
            tail = pre[pre.index(b"\xfc") :]
            head = pkt.replace(tail, b"")
            tail = self._bump_pts(tail)
            pkt = self._repad(head + tail)
        return pkt

    def apply_args(self, args):
        """
        apply_args applies command line args
        """
        self.outfile = args.outfile
        self.infile = args.infile
        self.secs = pif(args.secs)
        super().__init__(self.infile)

    def _parse_args(self):
        """
        _parse_args parse command line args
        """
        parser = argparse.ArgumentParser(epilog="scte35bump is part of threefive.\n\n")
        parser.add_argument(
            "-i",
            "--infile",
            default=sys.stdin.buffer,
            help=""" Input source, stdin, file, http(s), udp, or multicast mpegts
                                    [default: sys.stdin.buffer]
                                    """,
        )
        parser.add_argument(
            "-o",
            "--outfile",
            default=sys.stdout.buffer,
            help="Output file  [default: sys.stdout.buffer]",
        )
        parser.add_argument(
            "-s",
            "--secs",
            default=0.0,
            help="Adjustment to apply to SCTE-35 Cues. [default: 0.0]",
        )
        args = parser.parse_args()
        self.apply_args(args)


def bump(infile=sys.stdin.buffer, outfile=sys.stdout.buffer, secs=0.0):
    """
        bump  is a function to adjust PTS with defaults.

            infile = sys.stdin.buffer

            outfile = sys.stdout.buffer

            secs= 0.0

    example:
                    >>> from threefive import bump
                    >>> bump(infile,outfile,secs)

    """
    args = {
        "infile": infile,
        "outfile": outfile,
        "secs": secs,
    }
    bumper = StreamBumper()
    bumper.apply_args(args)
    bumper.bump()


def cli():
    """
    function to make a cli tool
    """
    bumper = StreamBumper()
    bumper.bump()
