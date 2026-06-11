"""
stream.py
Mpeg-TS Stream parsing class
"""

import io
import os
import sys
from collections import deque
from functools import partial
from .cue import Cue
from .new_reader import reader
from .packetdata import PacketData
from .streamtypes import streamtype_map
from .stuff import blue, ERR, print2
from .speedo import Speedo
from .throttle import Throttle


def show_cue(cue):
    """
    default function call for Stream.decode
    when a SCTE-35 packet is found.
    """
    cue.show()


def no_op():
    pass


class Based:
    """
    Based is a base class
    """

    def __repr__(self):
        stuff = []
        for k, v in self.__dict__.items():
            stuff.append(f"\n{k}:\t{v}")
        return "\n".join(stuff)

    @staticmethod
    def as_hms(secs_of_time):
        """
        as_hms converts timestamp to
        00:00:00.000 format
        """
        hours, seconds = divmod(secs_of_time, 3600)
        mins, seconds = divmod(seconds, 60)
        seconds = round(seconds)
        output = f"{int(hours):02}:{int(mins):02}:{seconds}"
        return output


class ProgramInfo(Based):
    """
    ProgramInfo is a class to
    hold Program information
    for use with Stream.show()
    """

    def __init__(self, pid=None, pcr_pid=None):
        self.streams = {}  # pid to stream_type mapping
        self.pid = pid
        self.pcr_pid = pcr_pid

    def _mk_vee(self, k):
        vee = int(self.streams[k], base=16)
        if vee in streamtype_map:
            vee = f"{hex(vee)}\t{streamtype_map[vee]}"
        else:
            vee = f"{vee} Unknown"
        print2(f"#\t  {k} [{hex(k)}]\t{vee}")

    def show(self):
        """
        show print2 the Program Infomation
        in a familiar format.
        """
        print2("")
        print2(f"#   Program Pid: {self.pid}")
        print2(f"#   Pcr Pid:     {self.pcr_pid}")
        print2("#   Streams:")
        # sorted_dict = {k:my_dict[k] for k in sorted(my_dict)})
        keys = sorted(self.streams)
        print2("#\t  Pid\t\tType")
        for k in keys:
            self._mk_vee(k)


class Pids(Based):
    """
    Pids holds sets of pids for pat,pcr,pmt, and scte35
    """

    SDT_PID = 0x11
    PAT_PID = 0x00

    def __init__(self):
        self.pcr = set()
        self.pmt = set()
        self.scte35 = set()
        self.maybe_scte35 = set()
        self.not_scte35 = set()
        self.tables = set([self.PAT_PID, self.SDT_PID])


class Maps(Based):
    """
    Maps holds mappings
    pids mapped to continuity_counters,
    programs, partial tables and last payload.

    programs mapped to pcr and pts

    """

    def __init__(self):
        self.pid_cc = {}
        self.pid_prgm = {}
        self.prgm_pcr = {}
        self.prgm_pts = {}
        self.prgm = {}
        self.partial = {}
        self.last = {}


class Stream(Based):
    """
    Stream class for parsing MPEG-TS data.
    """

    # the _CONST are deprecated
    # please switch to CONST

    PACKET_SIZE = 188
    SYNC_BYTE = 0x47
    MIN_PMT_COUNT = 16
    # tids
    PMT_TID = b"\x02"
    SCTE35_TID = b"\xfc"
    SDT_TID = b"\x42"
    ROLLOVER = 8589934591  # 95443.717678
    ROLLOVER9K = 95443.717678
    SCTE35_PES_START = b"\x00\x00\x01\xfc"

    def __init__(self, tsdata, show_null=True, headers={}):
        """
        tsdata is an file or http/https url
        set show_null=False to exclude Splice Nulls

        Use like...

        from threefive import Stream
        strm = Stream("vid.ts",show_null=False)
        strm.decode()

        """
        self.tsfile = tsdata
        if not isinstance(tsdata, str):
            self._tsdata = tsdata
        else:
            self._tsdata = reader(tsdata, headers=headers)
        self.show_null = show_null
        self.start = {}
        self.info = False
        self.the_scte35_pids = None
        self.pids = Pids()
        self.maps = Maps()
        self.pmt_payloads = {}
        self.pmt_count = 0
        self.pmt_pkt = None
        self.pat_pkt = None

    @staticmethod
    def as_90k(ticks):
        """
        as_90k returns ticks as 90k clock time
        """
        return round((ticks / 90000.0), 6)

    @staticmethod
    def _pusi_flag(pkt):
        return pkt[1] & 0x40

    @staticmethod
    def _afc_flag(pkt):
        return pkt[3] & 0x20

    @staticmethod
    def _pcr_flag(pkt):
        return pkt[5] & 0x10

    @staticmethod
    def _spi_flag(pkt):
        return pkt[5] & 0x20

    @staticmethod
    def _pts_flag(pay):
        # uses pay not pkt
        return pay[7] & 0x80

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return (byte1 & 0xF) << 8 | byte2

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        pid = (byte1 & 0x1F) << 8 | byte2
        return pid

    @staticmethod
    def _parse_program(byte1, byte2):
        """
        parse a 16 bit program number value
        """
        return (byte1 << 8) | byte2

    @staticmethod
    def _split_by_idx(pay, marker):
        try:
            return pay[pay.index(marker) :]
        except ERR:
            return False

    def rai(pkt):
        """
        rai random access indicator
        (keyframes)
        """
        if pkt[3] & 0x20: 
            return pkt[5] & 0x40
        return False

    def _find_start(self):
        while self._tsdata:
            one = self._tsdata.read(1)
            if one:
                if one[0] == self.SYNC_BYTE:
                    tail = self._tsdata.read(self.PACKET_SIZE - 1)
                    self._parse(one + tail)
                    return True
        print2("No Stream Found\n")
        return False

    def rt(self, func=show_cue):
        """
        rt  all ts packets are written to stdout
        for piping into another program in real time.
        SCTE-35 cues are print2`ed to stderr.
        decode SCTE-35.  the arg func can be set to
        a function that accepts one arg, a Cue instance.
        func is called everytime a Cue is found in the stream.
        the default func, show_cue calls Cue.show().
        """
        throttler = Throttle()
        for pkt in self.iter_pkts():
            self.pkt2cue(pkt, func)
            throttler.throttle(pkt)
            sys.stdout.buffer.write(pkt)
            sys.stdout.buffer.flush()
        return False

    def packetize(self, chunk):
        """
        packetize - turn chunk into 188 byte packets
        """
        for i in range(0, len(chunk), self.PACKET_SIZE):
            yield chunk[i : i + self.PACKET_SIZE]

    def iter_pkts(self, num_pkts=3300):
        """
        iter_pkts - iterate packets from stream
        """
        if self._find_start():
            for chunk in iter(
                partial(self._tsdata.read, num_pkts * self.PACKET_SIZE), b""
            ):
                yield from self.packetize(chunk)

    def speed(self):
        """
        Stream.speed is identical to Stream.decode
        but also shows parsing speed.
        """
        speedo = Speedo()
        num_pkts = 700
        for chunk in self.chunked(num_pkts=num_pkts):
            speedo.plus(len(chunk))
        speedo.end()
        return False

    def pkt2cue(self, pkt, func):
        """
        pkt2cue parse a packet,
        if Cue : func(Cue)
        return a Cue instance or None
        """
        cue = self._parse(pkt)
        if cue:
            func(cue)
            return cue
        return None

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        for pkt in self.iter_pkts():
            self.pkt2cue(pkt, func)
        return False

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        for pkt in self.iter_pkts():
            cue = self.parse(pkt)
            if cue:
                yield cue
        return False

    def decode_pcr(self, func=show_cue):
        """
        decode_pcr same as decode() but also includes pcr values
        """
        for pkt in self.iter_pkts():
            cue = self._parse_with_pcr(pkt)
            if cue:
                func(cue)
        return False

    def decode_pids(self, scte35_pids=None, func=show_cue):
        """
        Stream.decode_pids takes a list of SCTE-35 Pids parse
        and an optional call back function to run when a Cue is found.
        if scte35_pids is not set, all threefive pids will be parsed.
        """
        if scte35_pids:
            self.the_scte35_pids = scte35_pids
        return self.decode(func)

    def decode_start_time(self):
        """
        decode_start_time
        """
        for pkt in self.iter_pkts():
            self.parse(pkt)
            if len(self.start.values()) > 0:
                return self.start.popitem()[1]
        return False

    def proxy(self, func=show_cue):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        SCTE-35 cues are print2`ed to stderr.
        """
        for pkt in self.iter_pkts():
            self.pkt2cue(pkt, func)
            sys.stdout.buffer.write(pkt)
        return False

    def show(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        print2(f"\n# {self.tsfile}\n")
        self.info = True
        for pkt in self.iter_pkts():
            self._parse(pkt)
            if self.pmt_count > self.MIN_PMT_COUNT:
                blue(f"PMT Count: {self.pmt_count}")
                break
        if self.maps.prgm.keys():
            sopro = sorted(self.maps.prgm.items())
            for k, vee in sopro:
                print2(f"\n# Program: {k}")
                vee.show()

    def show_pts(self):
        """
        show_pts displays current pts by pid.
        """

        def short_bus(short_list, limit=None):
            short_list = deque(sorted(short_list))
            if not limit:
                limit = len(short_list)
            for i in range(limit):
                pts = short_list.popleft()
                print(f"\t{self.pid2prgm(pid)}\t{pts}")

        print("\tPrgm\tPTS")
        short_list = deque()
        for pkt in self.iter_pkts():
            pid = self._parse_info(pkt)
            if self._pusi_flag(pkt):
                if pid in self.pids.pcr:
                    self._parse_pts(pkt, pid)
                    pts = self.pid2pts(pid)
                    if pts:
                        short_list.append(pts)
                        if len(short_list) == 20:
                            short_bus(short_list, 10)
        short_bus(short_list)

    def pts(self):
        """
        pts returns a dict of  program:pts
        """
        return self.maps.prgm_pts

    def pid2prgm(self, pid):
        """
        pid2prgm takes a pid,
        returns the program
        """
        prgm = 1
        if pid in self.maps.pid_prgm:
            prgm = self.maps.pid_prgm[pid]
        return prgm

    def pid2pts(self, pid):
        """
        pid2pts takes a pid
        returns the current pts
        """
        prgm = self.pid2prgm(pid)
        if prgm in self.maps.prgm_pts:
            return self.as_90k(self.maps.prgm_pts[prgm])
        return False

    def pid2pcr(self, pid):
        """
        pid2pcr takes a pid
        returns the current pcr
        """
        prgm = self.pid2prgm(pid)
        if prgm in self.maps.prgm_pcr:
            return self.as_90k(self.maps.prgm_pcr[prgm])
        return False

    def _unpad_afc(self, pkt):
        return pkt[:4] + self._unpad(pkt[4:])

    def _unpad(self, bites=b""):
        return bites.strip(b"\xff")

    def _mk_packet_data(self, pid):
        prgm = self.maps.pid_prgm[pid]
        pdata = PacketData(pid, prgm)
        pdata.mk_pcr(self.maps.prgm_pcr)
        pdata.mk_pts(self.maps.prgm_pts)
        return pdata

    @staticmethod
    def mk_pts(payload):
        """
        mk_pts calculate pts from payload
        """
        pts = (payload[9] & 14) << 29
        pts |= payload[10] << 22
        pts |= (payload[11] >> 1) << 15
        pts |= payload[12] << 7
        pts |= payload[13] >> 1
        return pts

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        payload = self._parse_payload(pkt)
        if len(payload) > 13:
            if self._pts_flag(payload):
                pts = self.mk_pts(payload)
                prgm = self.pid2prgm(pid)
                self.maps.prgm_pts[prgm] = pts
                if prgm not in self.start:
                    self.start[prgm] = pts
        return False

    def _mk_pcr(self, pkt, pid):

        if self._afc_flag(pkt):
            pcr = pkt[6] << 25
            pcr |= pkt[7] << 17
            pcr |= pkt[8] << 9
            pcr |= pkt[9] << 1
            pcr |= pkt[10] >> 7
            prgm = self.pid2prgm(pid)
            self.maps.prgm_pcr[prgm] = pcr

    def _parse_payload(self, pkt):
        """
        _parse_payload returns the packet payload
        """
        head_size = 4
        if self._afc_flag(pkt):
            pkt = pkt[:4] + self._unpad(pkt[4:])
            afl = pkt[4]
            head_size += afl + 1  # +one for afl byte
        return pkt[head_size:]

    def _pmt_pid(self, pay, pid):
        self.pmt_count += 1
        prgm = self.pid2prgm(pid)
        if pay not in self.pmt_payloads.values():
            prgm = self.pid2prgm(pid)
            self.pmt_payloads[prgm] = pay
            self._parse_pmt(pay, pid)

    def _parse_tables(self, pkt, pid):
        pay = self._parse_payload(pkt)
        if pid == self.pids.PAT_PID:
            if not self._same_as_last(pay, self.pids.PAT_PID):
                self._parse_pat(pay)
        if pid in self.pids.pmt:
            self._pmt_pid(pay, pid)
        return False

    def _parse_info(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self.pids.tables:
            self._parse_tables(pkt, pid)
        return pid

    def _parse(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self.pids.tables:
            return self._parse_tables(pkt, pid)
        if pid in (self.pids.scte35 or self.pids.maybe_scte35):
            return self._parse_scte35(pkt, pid)
        if self._pusi_flag(pkt):
            if pid in self.pids.pcr:
                self._parse_pts(pkt, pid)
        return False

    def parse(self, pkt):
        """
        parse  parse pkt for tables and SCTE-35
        """
        return self._parse(pkt)

    def _parse_with_pcr(self, pkt):
        """
        same as _parse but includes pcr values
        """
        cue = self._parse(pkt)
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self.pids.pcr:
            if self._pcr_flag(pkt):
                self._mk_pcr(pkt, pid)
        return cue

    def _chk_partial(self, pay, pid, sep):
        if pid in self.maps.partial:
            pay = self.maps.partial.pop(pid) + pay
        return self._split_by_idx(pay, sep)

    def _same_as_last(self, pay, pid):
        last = False
        if pid in self.maps.last:
            last = self.maps.last[pid]
        self.maps.last[pid] = pay
        return last == pay

    def _section_incomplete(self, pay, pid, seclen):
        # + 3 for the bytes before section starts
        if len(pay) > (seclen + 3):
            return False
        if (seclen + 3) > len(pay):
            self.maps.partial[pid] = pay
            return True
        return False

    def _parse_cue(self, pay, pid):
        packet_data = None
        packet_data = self._mk_packet_data(pid)
        cue = Cue(pay, packet_data)
        if cue:
            return cue
        return False

    def _strip_scte35_pes(self, pkt):
        pay = self._parse_payload(pkt)
        if self.SCTE35_PES_START in pay:
            # blue(f"# Stripping PES Header from SCTE35")
            pay = pay.split(self.SCTE35_PES_START, 1)[-1]
            peslen = pay[4] + 5  # PES header length
            pay = pay[peslen:]
        return pay

    def _pop_maybe_pid(self, pid):
        if pid in self.pids.maybe_scte35:
            self.pids.maybe_scte35.remove(pid)
            self.pids.not_scte35.add(pid)

    def _chk_maybe_pid(self, pay, pid):
        pay = self._chk_partial(pay, pid, self.SCTE35_TID)
        if not pay:
            self._pop_maybe_pid(pid)
            return False
        if pay[13] == self.show_null:
            return False
        return pay

    def _mk_scte35_payload(self, pkt, pid):
        pay = self._strip_scte35_pes(pkt)
        if not pay:
            return False
        return self._chk_maybe_pid(pay, pid)

    def _parse_scte35(self, pkt, pid):
        """
        parse a threefive cue from one or more packets
        """
        if self.the_scte35_pids:  # for parse by pid
            if pid not in self.the_scte35_pids:
                return False
        pay = self._mk_scte35_payload(pkt, pid)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, pid, seclen):
            return False
        pay = pay[: seclen + 3]
        cue = self._parse_cue(pay, pid)
        return cue

    def _mk_pinfo(self, service_id, pn, sn):
        if service_id not in self.maps.prgm:
            self.maps.prgm[service_id] = ProgramInfo()
        pinfo = self.maps.prgm[service_id]
        pinfo.provider = pn
        pinfo.service = sn

    def _parse_pat(self, pay):
        """
        parse program association table
        for program to pmt_pid mappings.
        """
        pay = self._chk_partial(pay, self.pids.PAT_PID, b"")
        seclen = self._parse_length(pay[2], pay[3])
        if self._section_incomplete(pay, self.pids.PAT_PID, seclen):
            return False

        seclen -= 5  # pay bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while seclen > 4:  #  4 bytes for crc
            program_number = self._parse_program(pay[idx], pay[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(pay[idx + 2], pay[idx + 3])
                self.pids.pmt.add(pmt_pid)
                self.pids.tables.add(pmt_pid)
            seclen -= chunk_size
            idx += chunk_size
        return True

    def _parse_pmt(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._chk_partial(pay, pid, self.PMT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, pid, seclen):
            return False
        if self._same_as_last(pay, pid):
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
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12 + proginfolen
        si_len = seclen - (9 + proginfolen)
        self._parse_program_streams(si_len, pay, idx, program_number)
        return True

    def _parse_program_streams(self, si_len, pay, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        # 5 bytes for stream_type info
        chunk_size = 5
        end_idx = (idx + si_len) - 4
        while end_idx - chunk_size >= idx:
            stream_type, pid, ei_len = self._parse_stream_type(pay, idx)
            pinfo = self.maps.prgm[program_number]
            pinfo.streams[pid] = stream_type
            idx += chunk_size + ei_len
            self.maps.pid_prgm[pid] = program_number

    def _parse_stream_type(self, pay, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(pay[idx])
        el_pid = self._parse_pid(pay[idx + 1], pay[idx + 2])
        ei_len = self._parse_length(pay[idx + 3], pay[idx + 4])
        self._set_scte35_pids(el_pid, stream_type)
        return stream_type, el_pid, ei_len

    def _set_scte35_pids(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x86"]:
            self.pids.scte35.add(pid)
        if stream_type in ["0x06", "0x6", "0x05", "0x5"]:
            if pid not in self.pids.not_scte35:
                self.pids.maybe_scte35.add(pid)
