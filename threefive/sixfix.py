"""
sixfix.py
"""

import io
import sys
from collections import deque
from functools import partial
from .stuff import print2, ERR
from .stream import Stream, ProgramInfo
from .pmt import PMT

fixme = []

HELPME="""
  scte35fix checks MPEGTS for SCTE-35 Streams
  that have been change to bin data (type 0x06)
  and changes them back to SCTE-35 (type 0x86) streams.

  Output files are created in the current directory
  and prefixed with 'sixfix-'.

  Only bin data streams containing SCTE-35 will be converted.

  Multiple files can be specified on the command line.
  Wild cards work too.

  Example Usage:

        scte35fix video.ts

        scte35fix video1.ts video2.ts

        scte35fix video*.ts

        scte35fix https://example.com/video.ts

        scte35fix srt://10.10.10.13:4201


scte35fix is part of threefive.
"""

def passed(cue):
    """
    passed  is a function passed to decode
    used to pull pids from streams containing SCTE-35
    so that we don't convert non-SCTE-35 0x06 streams.
    """
    globals()['fixme'].append(cue.packet_data.pid)
    return cue


class PreFix(Stream):
    """
    PreFix is used to gather 06 Bin data pids with SCTE-35.
    """

    def decode(self, func=passed):
        super().decode(func=passed)
        tofix = list(set(globals()['fixme']))
        if tofix:
            print("fixing these pids", tofix)
        return tofix


class SixFix(Stream):
    """
    SixFix class
    fixes bin data streams with SCTE-35 to 0x86 SCTE-35 streams
    """

    CUEI_DESCRIPTOR = b"\x05\x04CUEI"

    def __init__(self, tsdata=None):
        super().__init__(tsdata)
        self.pmt_payloads = {}
        self.pmt_headers = deque()  # popleft()
        self.pmt_inputs = []
        self.pid_prog = {}
        self.con_pids = set()
        try:
            self.out_file = "sixfixed-" + tsdata.rsplit("/")[-1]
        except ERR:
            pass
        self.in_file = sys.stdin.buffer

    def iter_pkts(self, num_pkts=1):
        """
        iter_pkts iterates a mpegts stream into packets
        """
        # Skip find_start to catch first PAT/PMT
        return iter(partial(self._tsdata.read, self.PACKET_SIZE * num_pkts), b"")

    def _parse_by_pid(self, pkt, pid):
        if pid in self.pids.pmt:
            self.pmt_headers.append(pkt[:4])
            self._parse_pmt(pkt[4:], pid)
            prgm = self.pid2prgm(pid)
            if prgm in self.pmt_payloads:
                return self.pmt_payloads[prgm]
        else:
            if pid in self.pids.tables:
                self._parse_tables(pkt, pid)
            return pkt

    def _parse_pkts(self, out_file):
        active = io.BytesIO()
        # active hold
        pkt_count = 0
        activepkts = 2632
        for pkt in self.iter_pkts():
            pid = self._parse_pid(pkt[1], pkt[2])
            pkt = self._parse_by_pid(pkt, pid)
            if pkt:
                active.write(pkt)
                # dump active buff  to out_file every activepkts
                pkt_count = (pkt_count + 1) % activepkts
                if not pkt_count:
                    out_file.write(active.getbuffer())
                    active = io.BytesIO()

    def convert_pids(self):
        """
        convert_pids
        changes the stream type to 0x86 and replaces
        the existing PMT as it writes packets to the outfile
        """
        with open(self.out_file, "wb") as out_file:
            self._parse_pkts(out_file)

    def _chk_payload(self, pay, pid):
        pay = self._chk_partial(pay, pid, self.PMT_TID)
        return pay

    def pmt2packets(self, pmt, program_number):
        """
        pmt2packets split the new pmt table into 188 byte packets
        if you have a PMT spread over multiple packets,
        the packets will show up in order, and back to back,
        even if they were not that way in the original stream.
        """
        pmt_parts = []
        if not self.pmt_headers:
            return False
        pmt = self.pmt_headers.popleft() + pmt.mk()
        if len(pmt) < 188:
            pad = (188 - len(pmt)) * b"\xff"
            pmt_parts.append(pmt + pad)
        else:
            pmt_parts.append(pmt[:188])
            pmt = pmt[188:]
            while pmt and self.pmt_headers:
                pmtpkt = self.pmt_headers.popleft() + pmt
                if len(pmtpkt) < 188:
                    padding = 188 - len(pmtpkt)
                    pad = padding * b"\xff"
                    pmtpkt = pmtpkt + pad
                else:
                    pmt = pmtpkt[188:]
                    pmtpkt = pmtpkt[:188]
                pmt_parts.append(pmtpkt)
        self.pmt_payloads[program_number] = b"".join(pmt_parts)
        return True

    def _pmt_precheck(self, pay, pid):
        pay = self._unpad(pay)
        pay = self._chk_payload(pay, pid)
        if not pay:
            return False
        ##        if pay in self.pmt_inputs:   <<----  this is how I break continuity counters.
        ##            return False
        self.pmt_inputs.append(pay)
        return pay

    def mk_pmt(self, pay):
        pmt = PMT(pay, self.con_pids)
        return pmt

    def _parse_pmt(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._pmt_precheck(pay, pid)
        if not pay:
            return False
        pmt = self.mk_pmt(pay)
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, pid, seclen):
            return False
        program_number = self._parse_program(pay[3], pay[4])
        if not program_number:
            return False
        pcr_pid = self._parse_pid(pay[8], pay[9])
        if program_number not in self.maps.prgm:
            self.maps.prgm[program_number] = ProgramInfo()
        pinfo = self.maps.prgm[program_number]
        pinfo.pid = pid
        pinfo.pcr_pid = pcr_pid
        self.pids.pcr.add(pcr_pid)
        self.maps.pid_prgm[pcr_pid] = program_number
        self.maps.pid_prgm[pid] = program_number
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12
        end = idx + proginfolen
       # info_bites = pay[idx:end]
        idx = 12 + proginfolen
    #    si_len = seclen - (9 + proginfolen)  #  ???
        return self.pmt2packets(pmt, program_number)


def sixfix(arg):
    """
    sixfix converts 0x6 bin data mpegts streams
    that contain SCTE-35 data to stream type 0x86
    """
    globals()['fixme'] = []
    s1 = PreFix(arg)
    print2(f"reading {arg}")
    sixed = s1.decode(func=passed)

    if not sixed:
        print2("no bin data streams containing SCTE-35 data were found.")
        return
    s2 = SixFix(arg)
    s2.con_pids = sixed
    s2.convert_pids()
    print2(f'wrote: sixfixed-{arg.rsplit("/")[-1]}\n')
    return


def _chk_help():
    for h in ['help','-h', '--help']:
        if h in sys.argv:
            print(HELPME)
            sys.exit()


def cli():
    _chk_help()
    args = sys.argv[1:]
    _ = [sixfix(arg) for arg in args]


if __name__ == "__main__":
    cli()
