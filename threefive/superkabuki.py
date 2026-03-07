"""
Super Kabuki - SCTE-35 Packet injection

"""

import argparse
import io
import sys
from collections import deque
from operator import itemgetter
from .new_reader import reader
from .iframes import IFramer
from .cue import Cue
from .stuff import print2, ERR, pif
from .bitn import NBin
from .commands import TimeSignal
from .sixfix import SixFix
from .pmt import PMT

REV = "\033[7m"
NORM = "\033[27m"


class SuperKabuki(SixFix):
    """
    Super Kabuki - SCTE-35 Packet injection

    """

    _PACKET_SIZE = 188
    _SYNC_BYTE = 0x47
    # tids
    PMT_TID = b"\x02"
    SCTE35_TID = b"\xFC"
    CUEI_DESCRIPTOR = b"\x05\x04CUEI"

    def __init__(self, tsdata=None):
        self.infile = None
        self.outfile = "superkabuki-out.ts"
        if isinstance(tsdata, str):
            self.outfile = f'superkabuki-{tsdata.rsplit("/",1)[1]}'
        super().__init__(tsdata)
        self.scte35_pid = None
        self.scte35_cc = 0
        self.iframer = IFramer(shush=True)
        self.sidecar = deque()
        self.sidecar_file = "sidecar.txt"
        self.time_signals = False
        self._parse_args()
        super().__init__(self.infile)

    def _parse_args(self):
        """
        _parse_args parse command line args
        """
        parser = argparse.ArgumentParser(epilog="superkabuki is part of threefive.\n\n")
        parser.add_argument(
            "-i",
            "--input",
            default=sys.stdin.buffer,
            help=""" Input source, like "/home/a/vid.ts"
                                    or "udp://@235.35.3.5:3535"
                                    [default: sys.stdin.buffer]
                                    """,
        )

        parser.add_argument(
            "-o",
            "--output",
            default=sys.stdout.buffer,
            help="Output file  [default: sys.stdout.buffer]",
        )

        parser.add_argument(
            "-s",
            "--sidecar",
            default="sidecar.txt",
            help="Sidecar file for SCTE35 [default: sidecar.txt]",
        )
        parser.add_argument(
            "-p",
            "--scte35_pid",
            default="0x86",
            # type=int,
            help="Pid for SCTE-35 packets [default: 0x86]",
        )
        parser.add_argument(
            "-t",
            "--time_signals",
            action="store_const",
            default=False,
            const=True,
            help="Flag to insert Time Signal cues at iframes.",
        )

        args = parser.parse_args()
        self._apply_args(args)

    def _apply_args(self, args):
        """
        _apply_args applies command line args
        """
        self.outfile = args.output
        self.infile = args.input
        self.sidecar_file = args.sidecar
        self._tsdata = reader(args.input)
        self.pid2int(args.scte35_pid)
        self.time_signals = args.time_signals

    def pid2int(self, pid):
        """
        pid2int converts a string pid
        like "0x86" or "1000" to an int.
        """
        try:
            self.scte35_pid = pif(pid)
        except ERR:
            try:
                self.scte35_pid = pif(pid)
            except ERR:
                self.scte35_pid = 0x86

    def _bump_cc(self):
        self.scte35_cc = (self.scte35_cc + 1) % 16

    def open_output(self):
        """
        open_output open output file
        """
        print2(f"\nOutput File:\t{self.outfile}")
        if isinstance(self.outfile, str):
            self.outfile = open(self.outfile, "wb")

    def auto_time_signals(self, pts, outfile):
        """
        auto_time_signals auto add
        timesignals for every iframe.
        """
        if self.time_signals:
            outfile.write(self._gen_time_signal(pts))

    def add_scte35_pkt(self, pts, active):
        """
        add_scte35_pkt
        """
        scte35_pkt = self.chk_sidecar_cues(pts)
        if scte35_pkt:
            active.write(scte35_pkt)

    def parse_pkt(self, pkt):
        """
        parse_pkt parse a packet
        """
        pid = self._parse_info(pkt)
        if self._pusi_flag(pkt):
            self._parse_pts(pkt, pid)
        return pkt

    def iframe_action(self, pkt, pid, active):
        """
        iframe_action this is what we do when we find an iframe.
        """
        pts = self.iframer.parse(pkt)  # insert on iframe
        if pts:
            prgm = self.pid2prgm(pid)
            self.maps.prgm_pts[prgm] = pts
            self.auto_time_signals(pts, active)
            self.load_sidecar(pts)
            self.add_scte35_pkt(pts, active)

    def mk_pmt(self, pay):
        """
        mk_pmt generate PMT with the new SCTE-35 stream.
        """
        pmt = PMT(pay)
        pmt.add_scte35stream(self.scte35_pid)
        return pmt

    def encode(self):
        """
        encode parses the video input,
        adds the SCTE-35 PID to the PMT,
        parses the sidecar file,
        and injects SCTE-35 Packets,

        """
        self.open_output()
        active = io.BytesIO()
        pkt_count = 0
        chunk_size = 530
        with self.outfile as outfile:
            for pkt in self.iter_pkts():
                pid = self._parse_pid(pkt[1], pkt[2])
                pkt = self._parse_by_pid(pkt, pid)
                if pkt:
                    self.iframe_action(pkt, pid, active)
                    active.write(pkt)
                    pkt_count = (pkt_count + 1) % chunk_size
                    if not pkt_count:
                        outfile.write(active.getbuffer())
                        active = io.BytesIO()

    def _gen_time_signal(self, pts):

        cue = Cue()
        cue.command = TimeSignal()
        cue.command.time_specified_flag = True
        cue.command.pts_time = pts
        cue.encode()
        print2(f"inserted @{pts} - {cue.encode()}")
        cue.decode()
        nbin = NBin()
        nbin.add_int(71, 8)  # sync byte
        nbin.add_flag(0)  # tei
        nbin.add_flag(1)  # pusi
        nbin.add_flag(0)  # tp
        nbin.add_int(self.scte35_pid, 13)
        nbin.add_int(0, 2)  # tsc
        nbin.add_int(1, 2)  # afc
        nbin.add_int(self.scte35_cc, 4)  # cont
        nbin.add_bites(b"\x00")
        nbin.add_bites(cue.bites)
        pad_size = 188 - len(nbin.bites)
        padding = b"\xff" * pad_size
        nbin.add_bites(padding)
        self._bump_cc()
        return nbin.bites

    def _chk_sidecar_pts(self, pts, line):
        insert_pts, cue = line.split(",", 1)
        insert_pts = float(insert_pts)
        if insert_pts == 0.0:
            insert_pts = pts
        if insert_pts >= pts:
            if [insert_pts, cue] not in self.sidecar:
                self.sidecar.append([insert_pts, cue])
        self.sidecar = deque(sorted(self.sidecar, key=itemgetter(0)))

    def _read_sidecar_file(self, pts):
        with reader(self.sidecar_file) as sidefile:
            for line in sidefile:
                line = line.decode().strip().split("#", 1)[0]
                if line:
                    self._chk_sidecar_pts(pts, line)

    @staticmethod
    def clobber_file(the_file):
        """
        clobber_file  blanks the_file
        """
        with open(the_file, "w", encoding="utf8") as clobbered:
            clobbered.close()

    def load_sidecar(self, pts):
        """
        _load_sidecar reads (pts, cue) pairs from
        the sidecar file and loads them into X9K3.sidecar
        if live, blank out the sidecar file after cues are loaded.
        """
        if self.sidecar_file:
            self._read_sidecar_file(pts)
            self.clobber_file(self.sidecar_file)

    def chk_sidecar_cues(self, pts):
        """
        _chk_sidecar_cues checks the insert pts time
        for the next sidecar cue and inserts the cue if needed.
        """
        if self.sidecar:
            if (pts - 10) <= float(self.sidecar[0][0]) <= pts:
                cue_mesg = self.sidecar.popleft()[1]
                print2(f"\nInserted Cue:\n\t@{pts}, {cue_mesg}")
                return self.mk_scte35_pkt(cue_mesg)
        return False

    def mk_scte35_pkt(self, cue_mesg):
        """
        Make a SCTE-35 packet,
        with cue_mesg as the payload.
        """
        cue = Cue(cue_mesg)
        cue.decode()
        nbin = NBin()
        nbin.add_int(71, 8)  # sync byte
        nbin.add_flag(0)  # tei
        nbin.add_flag(1)  # pusi
        nbin.add_flag(0)  # tp
        nbin.add_int(self.scte35_pid, 13)
        nbin.add_int(0, 2)  # tsc
        nbin.add_int(1, 2)  # afc
        nbin.add_int(self.scte35_cc, 4)  # cont
        nbin.add_bites(b"\x00")
        nbin.add_bites(cue.bites)
        pad_size = 188 - len(nbin.bites)
        padding = b"\xff" * pad_size
        nbin.add_bites(padding)
        self._bump_cc()
        return nbin.bites


def cli():
    """
    cli handles all the command line args
    and such.

    """
    sk = SuperKabuki()
    sk.encode()
