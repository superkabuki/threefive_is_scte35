"""
threefive/bump.py

provides the function bumped to adjust pts in a SCTE-35 MPEGTS packet
bumped takes a packet and a float that is the amount to adjust  the SCTE-35 pts,

if the Cue in the packet has cue.command.pts_time:

    cue.command.pts_time is adjusted directly  like this:

   1)   cue.command.pts_time = bump + cue.info_section.pts_adjustment+ cue.command.pts_time

  2)  cue.info_section.pts_adjustment = 0.0

  3) if  a negative adjustement is used and cue.command.pts_time reults in a negative pts,
   then pts_time = ROLLOVER + negative_pts.

    For example if cue.command.pts_time =5000.0 and the adjustment is -8000.0
     5000.0 + (-8000.0)= -3000.0
     ROLLOVER +( -3000.0) = 92443.717678
     cue.command.pts_time would be set to 92443.717678


if the Cue in the packet doesn't have cue.command.pts_time:

   1)     cue.info_section.pts_adjustment=bump + cue.info_section.pts_adjustment



final values are modolo`ed to the ROLLOVER.

"""

import argparse
import sys

from .cue import Cue
from .stuff import blue
from .stream import Stream


ROLLOVER = 95443.717678
REV = "\033[7m"
NORM = "\033[27m"


def bump_pts_time(cue, bump):
    """
    bump_pts_time add bump directly to cue.command.pts_time
    """
    bumpme = cue.command.pts_time + cue.info_section.pts_adjustment + bump
    cue.info_section.pts_adjustment = 0.0
    if bumpme < 0.0:
        bumpme = ROLLOVER + bumpme
    cue.command.pts_time = bumpme % ROLLOVER


def bump_pts_adjust(cue, bump):
    """
    bump_pts_adjust add bump to cue.command.pts_adjustment
    """
    bumpme = cue.info_section.pts_adjustment + bump
    cue.info_section.pts_adjustment = bumpme % ROLLOVER


def show_bump():
    """
    show_bump show the Cue with adjusted pts.
    """
    blue("Cue adjusted")


def bump_pts(pay, bump):
    """
    bump_pts adjust SCTE-35 pts by bump
    """
    cue = Cue(pay)
    if cue.command.pts_time:
        bump_pts_time(cue, bump)
    else:
        bump_pts_adjust(cue, bump)
    cue.encode()
    show_bump()
    return cue.bytes()


def repad(pkt):
    """
    repad add padding to packet as needed.
    """
    pad = b"\xff"
    padsize = 188 - len(pkt)
    pkt = pkt + (pad * padsize)
    return pkt


def bumped(pkt, bump):
    """
    bumped adjust the pts_time in the Cue in the pkt by bump,
    bump is a float in seconds.
    """
    if b"\xfc" in pkt:
        pre = pkt.split(b"\x00\x00\x01\xfc")[-1]
        tail = pre[pre.index(b"\xfc") :]
        head = pkt.replace(tail, b"")
        tail = bump_pts(tail, bump)
        pkt = repad(head + tail)
    return pkt


class StreamBumper(Stream):
    """
    StreamBumper class

        Adjust SCTE-35 PTS times  in MPEGTS
    """

    def __init__(self, tsdata=None, show_null=True):
        super().__init__(tsdata)
        self.outfile = sys.stdout.buffer
        self.infile = None
        self.bump = 0.0
        self._parse_args()

    def _scte35(self, pkt, pid):
        if self._pid_has_scte35(pid):
            pkt = bumped(pkt, self.bump)
        return pkt

    def _parse2(self, pkt):
        """
        parse packets for tables and SCTE-35,
        adjust SCTE-35 PTS by bump.
        return modified pkt.
        """
        pid = self._parse_info(pkt)
        pkt = self._scte35(pkt, pid)
        return pkt

    def bump_scte35(self):
        """
        bump_scte_35 adjust pts of the SCTE-35 by bump
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

    def _apply_args(self, args):
        """
        _apply_args applies command line args
        """
        self.outfile = args.output
        self.infile = args.input
        self.bump = float(args.bump)
        super().__init__(self.infile)

    def _parse_args(self):
        """
        _parse_args parse command line args
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i",
            "--input",
            default=sys.stdin.buffer,
            help=f""" Input source, stdin, file, http(s), udp, or multicast mpegts
                                    [ default:{REV}sys.stdin.buffer{NORM} ]
                                    """,
        )
        parser.add_argument(
            "-o",
            "--output",
            default=sys.stdout.buffer,
            help=f"Output file  [ default:{REV}sys.stdout.buffer{NORM} ]",
        )
        parser.add_argument(
            "-b",
            "--bump",
            default=0.0,
            help=f"Adjustment to apply to SCTE-35 Cues. [default: {REV}0.0{NORM}]",
        )
        args = parser.parse_args()
        self._apply_args(args)


def cli():
    """
    function to make a cli tool
    """
    bumper = StreamBumper()
    bumper.bump_scte35()
