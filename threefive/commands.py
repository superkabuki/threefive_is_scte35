"""
SCTE35 Splice Commands
"""

from .bitn import Bitn
from .base import SCTE35Base
from .stuff import blue, red
from .xml import Node


class SpliceCommand(SCTE35Base):
    """
    Base class, not used directly.
    """

    def __init__(self, bites=None):
        self.command_length = 0
        self.command_type = None
        self.name = None
        self.bites = bites

    def decode(self):
        """
        default decode method
        """

    def _set_len(self, start, end):
        """
        _set_len sets
        self.command_length
        """
        self.command_length = (start - end) >> 3

    def encode(self, nbin=None):
        """
        encode
        """
        nbin = self._chk_nbin(nbin)
        self.command_length = len(nbin.bites)
        return nbin.bites


class BandwidthReservation(SpliceCommand):
    """
    Table 12 - bandwidth_reservation()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 7
        self.name = "Bandwidth Reservation"

    def xml(self, ns="scte35"):
        """
        create XML Node of type BandwidthReservation
        """
        return Node("BandwidthReservation", ns=ns)


class PrivateCommand(SpliceCommand):
    """
    Table 13 - private_command
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 255
        self.name = "Private Command"
        self.identifier = None
        self.private_bytes = None

    def decode(self):
        """
        PrivateCommand.decode method
        """
        self.identifier = int.from_bytes(
            self.bites[:4], byteorder="big"
        )  # 4 bytes = 32 bits
        self.private_bytes = self.bites[4:]

    def encode(self, nbin=None):
        """
        encode private command
        """
        nbin = self._chk_nbin(nbin)
        self._chk_var(int, nbin.add_int, "identifier", 32)  # 4 bytes = 32 bits
        nbin.add_bites(self.private_bytes)
        self.command_length = len(nbin.bites)
        return nbin.bites

    def xml(self, ns="scte35"):
        """
        create XML Node of type PrivateCommand
        """
        attrs = {"identifier": self.identifier}
        pc = Node("PrivateCommand", attrs=attrs)
        pc.addchild(Node("PrivateBytes", value=self.private_bytes.hex(), ns=ns))
        return pc


class SpliceNull(SpliceCommand):
    """
    Table 8 - splice_null()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 0
        self.name = "Splice Null"

    def xml(self, ns="scte35"):
        """
        xml return a SplicNull xml Node instance.
        """
        return Node("SpliceNull", ns=ns)


class TimeSignal(SpliceCommand):
    """
    Table 11 - time_signal()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 6
        self.name = "Time Signal"
        self.time_specified_flag = None
        self.pts_time = None

    #  self.pts_ticks = None

    def decode(self):
        """
        TimeSignal.decode method
        """
        bitbin = Bitn(self.bites)
        start = bitbin.idx
        self._splice_time(bitbin)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        encode converts TimeSignal vars
        to bytes
        """
        nbin = self._chk_nbin(nbin)
        self._encode_splice_time(nbin)
        self.command_length = len(nbin.bites)
        return nbin.bites

    def _splice_time(self, bitbin):
        """
        _splice_time Table 14 - splice_time()
        """
        self.time_specified_flag = bitbin.as_flag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            pts_ticks = bitbin.as_int(33)
            self.pts_time = self.as_90k(pts_ticks)
        else:
            bitbin.forward(7)

    def _encode_splice_time(self, nbin):
        """
        _encode_splice_time Table 14 - splice_time()
        """
        self._chk_var(bool, nbin.add_flag, "time_specified_flag", 1)
        if self.time_specified_flag:
            nbin.reserve(6)
            if not self.pts_time:
                return red("pts_time is not set")
            nbin.add_int(self.as_ticks(self.pts_time), 33)
        else:
            self.pts_time = None
            nbin.reserve(7)

    def xml(self, ns="scte35"):
        """
        xml return TimeSignal as an xml node
        """
        ts = Node("TimeSignal", ns=ns)
        if self.has("pts_time"):
            if self.pts_time:
                self.pts_time = round(self.pts_time, 6)
                st = Node(
                    "SpliceTime",
                    attrs={"pts_time": self.as_ticks(self.pts_time)},
                    ns=ns,
                )
                ts.addchild(st)
        return ts


class SpliceInsert(TimeSignal):
    """
    Table 10 - splice_insert()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 5
        self.name = "Splice Insert"
        self.break_auto_return = None
        self.break_duration = None
        self.break_duration_ticks = None
        self.splice_event_id = None
        self.splice_event_cancel_indicator = None
        self.out_of_network_indicator = None
        self.program_splice_flag = None
        self.duration_flag = None
        self.splice_immediate_flag = None
        self.event_id_compliance_flag = None
        self.unique_program_id = None
        self.avail_num = None
        self.avails_expected = None

    def _decode_break_duration(self, bitbin):
        """
        _decode_break_duration Table 15 - break_duration()
        """
        self.break_auto_return = bitbin.as_flag(1)
        bitbin.forward(6)
        break_duration_ticks = bitbin.as_int(33)
        self.break_duration = self.as_90k(break_duration_ticks)

    def decode(self):
        """
        decode SpliceInsert
        """
        bitbin = Bitn(self.bites)
        start = bitbin.idx
        self.splice_event_id = bitbin.as_int(32)
        self.splice_event_cancel_indicator = bitbin.as_flag(1)
        bitbin.forward(7)
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitbin.as_flag(1)
            self.program_splice_flag = bitbin.as_flag(1)
            self.duration_flag = bitbin.as_flag(1)
            self.splice_immediate_flag = bitbin.as_flag(1)
            self.event_id_compliance_flag = bitbin.as_flag(1)
            bitbin.forward(3)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._splice_time(bitbin)
            if self.duration_flag:
                self._decode_break_duration(bitbin)
            self.unique_program_id = bitbin.as_int(16)
            self.avail_num = bitbin.as_int(8)
            self.avails_expected = bitbin.as_int(8)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        SpliceInsert.encode
        """
        nbin = self._chk_nbin(nbin)
        self._chk_var(int, nbin.add_int, "splice_event_id", 32)
        self._chk_var(bool, nbin.add_flag, "splice_event_cancel_indicator", 1)
        nbin.forward(7)
        if not self.splice_event_cancel_indicator:
            self._chk_var(bool, nbin.add_flag, "out_of_network_indicator", 1)
            self._chk_var(bool, nbin.add_flag, "program_splice_flag", 1)
            self._chk_var(bool, nbin.add_flag, "duration_flag", 1)
            self._chk_var(bool, nbin.add_flag, "splice_immediate_flag", 1)
            self._chk_var(bool, nbin.add_flag, "event_id_compliance_flag", 1)
            nbin.forward(3)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._encode_splice_time(nbin)
            if self.duration_flag:
                self._encode_break_duration(nbin)
            self._chk_var(int, nbin.add_int, "unique_program_id", 16)
            self._chk_var(int, nbin.add_int, "avail_num", 8)
            self._chk_var(int, nbin.add_int, "avails_expected", 8)
        self.command_length = len(nbin.bites)
        return nbin.bites

    def _encode_break_duration(self, nbin):
        """
        SpliceInsert._encode_break(nbin) is called
        if SpliceInsert.duration_flag is set
        """
        self._chk_var(bool, nbin.add_flag, "break_auto_return", 1)
        nbin.forward(6)
        if not self.break_duration:
            red("break_duration is not set")
        else:
            ##            self.break_duration = self.as_90k(self.break_duration_ticks)
            nbin.add_int(self.as_ticks(self.break_duration), 33)

    def xml(self, ns="scte35"):
        """
        xml return the SpliceInsert instance as an xml node.
        """
        si_attrs = {
            "splice_event_id": self.splice_event_id,
            "splice_event_cancel_Indicator": self.splice_event_cancel_indicator,
            "splice_immediate_flag": self.splice_immediate_flag,
            "event_id_compliance_flag": self.event_id_compliance_flag,
            "avail_num": self.avail_num,
            "avails_expected": self.avails_expected,
            "out_of_network_indicator": self.out_of_network_indicator,
            "unique_program_id": self.unique_program_id,
        }
        for k, v in si_attrs.items():
            if v is None:
                blue(f"SpliceInsert.{k} needs to be set")
        si = Node("SpliceInsert", attrs=si_attrs, ns=ns)
        if self.pts_time:
            prgm = Node("Program", ns=ns)
            st = Node(
                "SpliceTime", attrs={"ptsTime": self.as_ticks(self.pts_time)}, ns=ns
            )
            prgm.addchild(st)
            si.addchild(prgm)
        if self.break_duration:
            bd_attrs = {
                "auto_return": self.break_auto_return,
                "duration": self.as_ticks(self.break_duration),
            }
            bd = Node("BreakDuration", attrs=bd_attrs, ns=ns)
            si.addchild(bd)
        return si


# table 7
command_map = {
    0: SpliceNull,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}
