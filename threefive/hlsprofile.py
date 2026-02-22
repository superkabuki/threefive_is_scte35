"""
hlsprofile.py contains Scte35Profile for the HLSParser class.

"""

import os

from .stuff import pif


ROLLOVER = 95443.717678
REV = "\033[7m"
NORM = "\033[0m"


class Scte35Profile:
    """
    Scte35Profile Manages the Scte35 Parsing Profile
    """

    def __init__(self):
        """
        A Scte35Profile
        """
        self.expand_cues = False  # Show SCTE-35 Cues fully expanded.
        self.parse_segments = True  # Parse Segments for SCTE-35.
        self.parse_manifests = True  # Parse m3u8 files for SCTE-35 HLS tags.
        #  Parse these types of HLS SCTE-35 tags.
        self.hls_tags = [
            "#EXT-OATCLS-SCTE35",
            "#EXT-X-CUE-OUT-CONT",
            "#EXT-X-DATERANGE",
            "#EXT-X-SCTE35",
            "#EXT-X-CUE-IN",
            "#EXT-X-CUE-OUT",
        ]
        # Which Splice Commands types to parse.
        self.command_types = [6, 5]
        # Which  Splice Descriptors tags to parse.
        self.descriptor_tags = [
            2,
        ]
        # Which Descriptor Segmentation Types IDs should be parsed
        self.starts = [0x22, 0x30, 0x32, 0x34, 0x36, 0x44, 0x46]
        self.seg_type = 0x23

    # self.stops = [0x23, 0x31, 0x33, 0x35, 0x37, 0x45, 0x47]

    def __repr__(self):
        return "\n\n  ".join(
            [f"\n{REV} Profile {NORM}"]
            + [f"{REV} {k} {NORM} = {v}" for k, v in vars(self).items()]
        )

    def _is_int(self, vee, line):
        for item in vee:
            if isinstance(item, int):
                line = f"{line}{hex(item)},"
            else:
                line = f"{line}{item},"
        return line

    def _list_in_profile(self, vee, line):
        if isinstance(vee, list):
            line = self._is_int(vee, line)
        return line

    def _bool_in_profile(self, vee, line):
        if isinstance(vee, bool):
            line = f"{line}{vee}"
        return line

    def _mk_profile_line(self, que, vee):
        line = f"{que} = "
        line = self._list_in_profile(vee, line)
        line = self._bool_in_profile(vee, line)
        line = line.strip(",")
        return line

    def _write_profile_lines(self, pro_f):
        for quay, vee in vars(self).items():
            line = self._mk_profile_line(quay, vee)
            pro_f.write(line + "\n")

    def write_profile(self, pro_file):
        """
        write_profile writes hls.profile for editing.
        """
        with open(pro_file, "w", encoding="utf-8") as pro_f:
            self._write_profile_lines(pro_f)

    def _vee_to_hex(self, vee):
        return [hex(eye) for eye in vee]

    def _vee_is_ints(self, vee):
        if isinstance(vee[0], int):
            vee = self._vee_to_hex(vee)
        return vee

    def _vee_is_list(self, vee):
        if isinstance(vee, list):
            vee = self._vee_is_ints(vee)
        return vee

    def _is_comment(self, line, this):
        if line[0] == "#" or line[:2] == "//":
            this = None
        return this

    def _split_this_that(self, line):
        this, that = None, None
        if line:
            this, that = line.split("=", 1)
            that = list(that.split(","))
        this = self._is_comment(line, this)
        return this, that

    @staticmethod
    def _clean(line):
        """
        remove whitespace and quotes
        """
        translate_map = {34: 94, 10: 94, 9: 94, 32: 94, 39: 94}
        return line.translate(translate_map).replace("^", "")

    def _clean_n_split(self, line):
        """
        _clean_n_split a line.
        """
        line = self._clean(line)
        return self._split_this_that(line)

    def _string2bool(self, this, that):
        if this.startswith("parse") or this.startswith("expand"):
            return [False, True][that[0] == "True"]
        return that

    @staticmethod
    def _hex_or_int(s):
        return pif(s)

    def _new_that(self, that):
        new_that = []
        for s in that:
            new_s = self._hex_or_int(s)
            new_that.append(new_s)
        return new_that

    def _hexed(self, this, that):
        if this in ["command_types", "descriptor_tags", "starts"]:
            return self._new_that(that)
        return that

    @staticmethod
    def _this_that_none(this, that):
        if this is None or that is None:
            return True
        return False

    def format4profile(self, this, that):
        """
        format4profile formats data read from hls.profile for internal use.
        """
        if not self._this_that_none(this, that):
            this = this.lower()
            that = self._string2bool(this, that)
            that = self._hexed(this, that)
            self.__dict__.update({this: that})

    def _parse_profile(self, pro_handle):
        for line in pro_handle:
            this, that = self._clean_n_split(line)
            self.format4profile(this, that)

    def read_profile(self, pro_file):
        """
        read_profile reads hls.profile
        """
        if os.path.isfile(pro_file):
            with open(pro_file, "r", encoding="utf-8") as pro_handle:
                self._parse_profile(pro_handle)

    #####

    def set_pts(self, cue):
        """
        set_pts cue.command.pts_time +
        cue.info_section.pts_adjustment
        % ROLLOVER
        """
        pts = cue.command.pts_time + cue.info_section.pts_adjustment
        return pts % ROLLOVER

    def _chk_pts(self, cue):
        pts = None
        if cue.command.has("pts_time"):
            pts = self.set_pts(cue)
        return pts

    def _chk_expand(self, cue):
        if self.expand_cues:
            cue.show()

    def _chk_time_signal(self, cue, line):
        if cue.command.command_type == 6:
            line = self._validate_time_signal(cue)
        return line

    def _chk_splice_insert(self, cue, line):
        if cue.command.command_type == 5:
            line = self._validate_splice_insert(cue)
        return line

    def validate_cue(self, cue):
        """
        validate_cue use the parsing profile to validate a SCTE-35 Cue.
        """
        pts = None
        line = None
        cue.decode()
        if cue.command.command_type in self.command_types:
            self._chk_expand(cue)
            pts = self._chk_pts(cue)
            line = self._chk_splice_insert(cue, line)
            line = self._chk_time_signal(cue, line)
        return pts, line

    def _mk_cueout_line(self, duration):
        return f"#EXT-X-CUE-OUT:{duration}\n"

    def _is_splice_insert_cueout(self, cue):
        line = None
        if cue.command.has("break_duration"):
            line = self._mk_cueout_line(cue.command.break_duration)
        return line

    def _validate_splice_insert(self, cue):
        """
        _validate_splice_insert is named appropriately.
        """
        line = self._is_splice_insert_cueout(cue)
        if not line:
            line = "#EXT-X-CUE-IN\n"
        return line

    def _incr_seg_type(self, line, dscptr):
        self.seg_type = dscptr.segmentation_type_id + 1
        if dscptr.has("segmentation_duration"):
            line = self._mk_cueout_line(dscptr.segmentation_duration)
        return line

    def _is_dscptr_cueout(self, dscptr, line):
        if dscptr.segmentation_type_id in self.starts:
            line = self._incr_seg_type(line, dscptr)
        return line

    def _is_dscptr_cuein(self, dscptr, line):
        if dscptr.segmentation_type_id == self.seg_type:
            line = "#EXT-X-CUE-IN\n"
            self.seg_type = None
        return line

    def _validate_dscptr(self, dscptr, line):
        if dscptr.tag in self.descriptor_tags:
            line = self._is_dscptr_cueout(dscptr, line)
            line = self._is_dscptr_cuein(dscptr, line)
        return line

    def _validate_time_signal(self, cue):
        """
        _validate_time_signal is named appropriately.
        """
        line = None
        for dscptr in cue.descriptors:
            line = self._validate_dscptr(dscptr, line)
        return line
