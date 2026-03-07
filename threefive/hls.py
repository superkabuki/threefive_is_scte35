#!/usr/bin/env python3
"""
threefive.hls  hls.py
(replaces showcues)

"""

import sys
import time
from collections import deque
from .aac import AacParser
from .hlstags import TagParser, HEADER_TAGS
from .segment import Segment
from .cue import Cue
from .new_reader import reader
from .stuff import iso8601, red, blue, ERR, reblue, pif
from .hlsprofile import Scte35Profile

REV = "\033[7m"
NORM = "\033[0m"
SUB = "\t"
NSUB = f"\n{SUB}"
ROLLOVER = 95443.717678
HEADER_TAGS = list(HEADER_TAGS)
HEADER_TAGS.append("#EXTM3U")


class Pane:
    """
    Pane class. Sliding_Window slides Panes
    """

    def __init__(self, media, lines):
        self.media = media
        self.lines = lines

    def get(self):
        """
        get merges self.lines and self.media for
        writing m3u8 files.
        """
        all_lines = self.lines + [self.media]
        return "".join(all_lines)

    def __repr__(self):
        return str(self.__dict__)


class SlidingWindow:
    """
    The Sliding Window class
    """

    def __init__(self, size=101):
        self.size = size
        self.panes = deque()
        self.delete = False

    def pop_pane(self):
        """
        pop_pane removes the first item in self.panes
        """
        if len(self.panes) > self.size:
            self.panes.popleft()

    def all_panes(self):
        """
        all_panes returns the current window panes joined.
        """
        return "\n".join({a_pane.get() for a_pane in self.panes})

    def slide_panes(self, a_pane):
        """
        slide calls self.push_pane with a_pane
        and then calls self.pop_pane to trim self.panes
        as needed.
        """
        self.panes.append(a_pane)
        self.pop_pane()


class HlsParser:
    """
    HlsParser is the Hls Parser
    """

    def __init__(self, pro_file="hls.profile", headers={}):
        self.media = deque()
        self.sidecar = "hls.sidecar"
        self.dumpfile = "hls.dump"
        self.flat = "hlsflat.m3u8"
        self.pro_file = pro_file
        self.m3u8 = "hls.m3u8"
        self.last_dump_line = None
        self.base_uri = None
        self.iv = None
        self.key_uri = None
        self.last_iv = None
        self.last_key_uri = None
        self.break_timer = None
        self.break_duration = None
        self.reload = True
        self.sleep_duration = 0
        self.window_size = None
        self.sliding_window = SlidingWindow()
        self.cue_state = None
        self.last_cue = None
        self.headers = headers
        self.hls_headers = []
        self.pts = 0
        self.cont_resume = True
        self.first_segment = True
        self.hls_pts = "HLS"
        self.prof = Scte35Profile()
        self.prof.read_profile(self.pro_file)
        self.rendition = None
        self._clear_files()

    @staticmethod
    def _clear():
        """
        _clear previous line.
        """
        print(" " * 80, end="\r")
        print(" " * 80, file=sys.stderr, end="\r", flush=True)

    def _clear_files(self):
        """
        _clear_files clobbers the appended files
        self.sidecar, self.dumpfile, self.flat, self.m3u8
        when showcues is started.
        """
        for sidef in [self.sidecar, self.dumpfile, self.flat, self.m3u8]:
            with open(sidef, "w+", encoding="utf-8") as side_file:  # touch
                side_file.close()
            # pass

    def _chk_aes(self, line):
        """
        _chk_aes checks for AES encryption
        """
        if "#EXT-X-KEY" in line:
            tags = TagParser([line]).tags
            if "URI" in tags["#EXT-X-KEY"]:
                self.key_uri = tags["#EXT-X-KEY"]["URI"]
                if not self.key_uri.startswith("http"):
                    re_uri = self.base_uri + self.key_uri
                    self.key_uri = re_uri
                if "IV" in tags["#EXT-X-KEY"]:
                    self.iv = tags["#EXT-X-KEY"]["IV"]

    def _to_sidecar(self, pts, line):
        """
        _to_sidecar writes (pts,hls tag) pairs to the sidecar file.
        """
        with open(self.sidecar, "a", encoding="utf-8") as sidecar:
            sidecar.write(f"{round(pts,6)},{line}\n")

    def _to_dump(self, pts, line):
        """
        _to_dump copies all SCTE-35 lines to self.dumpfile.
        """
        with open(self.dumpfile, "a", encoding="utf-8") as dump:
            dump_line = f"{pts},{line}\n"
            if dump_line != self.last_dump_line:
                dump.write(dump_line)
                self.last_dump_line = dump_line

    def _media_stuff(self):
        """
        _media_stuff trims segment URI to just the file name.
        """
        media = self.media[-1]
        short_media = media.rsplit("/", 1)[1].split("?", 1)[0]
        return f"Media: {short_media.strip()}"

    ##    def _cue_stuff(self):
    ##        """
    ##        _cue_stuff returns self.cue_state formated.
    ##        """
    ##        return f"Cue {REV}{self.cue_state} {NORM}"

    def _diff_stuff(self):
        """
        diff gonzo returns formated self.break_timer
        and if possible the difference between the actual break duration
        and the specified SCTE-35 break duration.
        """
        if self.break_timer is not None:
            if not self.break_duration:
                return f"{NSUB}Break Timer: {round(self.break_timer,6)}"
            return (NSUB).join(
                [
                    f"{NSUB}Timer: { round(self.break_timer,6)}",
                    f"Duration: {self.break_duration}",
                    f"Diff: {round(self.break_timer - self.break_duration,6)}",
                ]
            )
        return ""

    def _dur_stuff(self):
        """
        _dur_stuff returns self.break_duration formated.
        """
        return f"{NSUB}Duration: {self.break_duration}"

    def _pts_stuff(self):
        """
        _pts_stuff returns  PTS formated.
        """
        return f"{NSUB}{self.hls_pts}: {self.pts}"

    def _chk_cue_in(self, line, head):
        # print("\n",line,"\n")
        if line.startswith("#EXT-X-CUE-IN"):  # and self.cue_state == "CONT":
            self.cue_state = "IN"
            self._to_sidecar(self.pts, line)
            self._clear()
            print(f"{head}{self._diff_stuff()}{NSUB}{self._media_stuff()}\n")
            self._reset_break()
        return line

    def _chk_cue_out(self, line, head):
        if line.startswith("#EXT-X-CUE-OUT") and self.cue_state in [None, "IN"]:
            self._reset_break()
            self.cue_state = "OUT"
            self.break_timer = 0.0
            if ":" in line:
                self.break_duration = pif(line.split(":")[1])
            self._to_sidecar(self.pts, line)
            self._clear()
            print(f"{head}{self._dur_stuff()}{NSUB}{self._media_stuff()}\n")
        return line

    def _set_cue_state(self, cue, line):
        """
        _set_cue_state determines cue_state

        """
        #  line= self._auto_cuein(line)
        if isinstance(cue, int):
            cue = f"{cue}"
        if cue.encode() == self.last_cue:
            return ""
        self.last_cue = cue.encode()
        if line and "CONT" not in line:
            head = f"\n{iso8601()}{REV}{line}{NORM}\n{REV} Splice Point {NORM}{self._pts_stuff()} "
            line = self._chk_cue_in(line, head)
            line = self._chk_cue_out(line, head)

        elif self.cue_state in ["OUT", "CONT"]:
            self._to_sidecar(self.pts, line)
            self.cue_state = "CONT"
        return line

    def _invalid(self, line):
        """
        _invalid print invalid SCTE-35 HLS tags
        """
        self._clear()
        blue(f"{iso8601()}{REV}  Skipped  {NORM} {line}  ")
        print(f"{self._pts_stuff()}{NSUB}{self._media_stuff()}\n")
        return "## " + line

    def _show_tags(self, tags):
        """
        _show_tags print tags
        """
        for que, vee in tags.items():
            print(f"{SUB}{que}: {vee}")

    def _set_break_timer(self, line, cont_tags):
        """
        _set_break_timer sets self.break_timer to ElaspsedTime
        read from a CUE-OUT-CONT tag or to 0.0.
        """
        if self.break_timer:
            return
        if "ElapsedTime" in cont_tags:
            self.break_timer = cont_tags["ElapsedTime"]
        else:
            try:
                self.break_timer = round(float(line.split(":", 1)[1].split("/")[0]), 3)
            except ERR:
                self.break_timer = 0.0
        print(f"{iso8601()}{REV} Break Timer {NORM} {self.break_timer}\n")
        time.sleep(0.1)

    def _set_break_duration(self, line, cont_tags):
        """
        __set_break_duration sets self.break_duration from
        a CUE-OUT-CONT tag or from a CUE-OUT tag.
        """
        if self.break_duration:
            return
        if "Duration" in cont_tags:
            self.break_duration = cont_tags["Duration"]
        else:
            try:
                self.break_duration = round(
                    float(line.split(":", 1)[1].split("/")[1]), 3
                )
            except ERR:
                self.break_duration = None
        if self.break_duration:
            print(f"{iso8601()}{REV} Break Duration {NORM} {self.break_duration}\n")
            time.sleep(0.1)

    def _chk_x_cue_out_cont(self, tags, line):
        """
        _chk_x_cue_out_const processes
        #EXT-X-CUE-OUT-CONT tags
        """
        ##        if "#EXT-X-CUE-OUT-CONT" not in self.prof.hls_tags:
        ##            return ""
        cont_tags = tags["#EXT-X-CUE-OUT-CONT"]

        if self.cue_state not in ["OUT", "CONT"] and not self.first_segment:
            return None
        if self.first_segment:
            blue(f"{NORM}{iso8601()}{REV} Resuming Ad Break")
            self.cue_state = "CONT"
            self._set_break_timer(line, cont_tags)
            self._set_break_duration(line, cont_tags)
            line = self._auto_cuein(line)
        return self._auto_cont()

    def _chk_x_cue_in(self, tags, line):
        """
        _chk_x_cue_in processes
        #EXT-X-CUE-IN tags.
        """
        ##        if "#EXT-X-CUE-IN" not in self.prof.hls_tags:
        ##            return self._invalid(line)
        self._reset_break()
        self.cue_state = "IN"
        return self._set_cue_state(line, line)

    def _chk_x_cue_out(self, tags, line):
        """
        _chk_x_cue_out processes
        #EXT-X-CUE-OUT tags
        """
        ##        if "#EXT-X-CUE-OUT" not in self.prof.hls_tags:
        ##            return self._invalid(line)
        return self._set_cue_state(line, line)

    def _chk_x_scte35(self, tags, line):
        """
        _chk_x_scte35 handles #EXT-X-SCTE35 tags.
        """
        ##        if "#EXT-X-SCTE35" not in self.prof.hls_tags:
        ##            return self._invalid(line)
        if "CUE" in tags["#EXT-X-SCTE35"]:
            cue = Cue(tags["#EXT-X-SCTE35"]["CUE"])
            pts, new_line = self.prof.validate_cue(cue)
            if pts and new_line:
                return self._set_cue_state(tags["#EXT-X-SCTE35"]["CUE"], new_line)
        return None

    #  return self._invalid(line)

    def _chk_x_daterange(self, tags, line):
        """
        _chk_x_daterange handles #EXT-X-DATERANGE tags.
        """
        ##        if "#EXT-X-DATERANGE" not in self.prof.hls_tags:
        ##            return self._invalid(line)
        self._show_tags(tags["#EXT-X-DATERANGE"])
        for scte35_tag in ["SCTE35-OUT", "SCTE35-IN"]:
            if scte35_tag in tags["#EXT-X-DATERANGE"]:
                cue = Cue(tags["#EXT-X-DATERANGE"][scte35_tag])
                pts, new_line = self.prof.validate_cue(cue)
                if pts and new_line:
                    return self._set_cue_state(
                        tags["#EXT-X-DATERANGE"][scte35_tag], new_line
                    )
        return None

    # return self._invalid(line)

    def _chk_x_oatcls(self, tags, line):
        """
        _chk_x_oatcls handles
        #EXT-OATCLS-SCTE35
        HLS tags.
        """
        ##    if "#EXT-X-OATCLS-SCTE35" not in self.prof.hls_tags:
        ##        return self._invalid(line)
        cue = Cue(tags["#EXT-OATCLS-SCTE35"])
        pts, new_line = self.prof.validate_cue(cue)
        if pts and new_line:
            if abs(pts - self.pts) > 5:  # Handle Cues out of sync with video PTS
                pts = self.pts
                return self._set_cue_state(tags["#EXT-OATCLS-SCTE35"], new_line)
        #   return self._invalid(line)
        return line

    def _dump_by_key(self, pts, line, keys):
        for key in keys:
            if key in line:
                self._to_dump(self.pts, line)

    def scte35(self, line):
        """
        threefive processes SCTE-35 related tags.
        """
        scte35_map = {
            "#EXT-X-DATERANGE": self._chk_x_daterange,
            "#EXT-X-SCTE35": self._chk_x_scte35,
            "#EXT-X-CUE-OUT-CONT": self._chk_x_cue_out_cont,
            "#EXT-OATCLS-SCTE35": self._chk_x_oatcls,
            "#EXT-X-CUE-IN": self._chk_x_cue_in,
            "#EXT-X-CUE-OUT": self._chk_x_cue_out,
        }
        tags = TagParser([line]).tags
        keys = list(scte35_map.keys())
        self._dump_by_key(self.pts, line, keys)
        if self.prof.parse_manifests:
            for que, vee in scte35_map.items():
                if que in line:
                    if que not in self.prof.hls_tags:
                        return self._invalid(line)
                    return vee(tags, line)
        return line

    def _auto_cont(self):
        """
        _auto_cont automatically add CUE-OUT-CONT tags
        """
        self.cue_state = "CONT"
        line = (
            f"#EXT-X-CUE-OUT-CONT:{round(self.break_timer,3)}/{self.break_duration}\n"
        )
        line = self._set_cue_state(line, line)
        return line

    def _auto_cuein(self, line):
        """
        _auto_cuein handles cue.command.auto-return
        """
        # if self.cue_state == "CONT":
        if self.break_timer and self.break_duration:
            if self.break_timer >= self.break_duration:
                self.cue_state = "IN"
                self._clear()
                first = f"{iso8601()}{REV} AUTO CUE-IN {NORM}{self._pts_stuff()}"
                second = f"{self._diff_stuff()}{NSUB}{self._media_stuff()}"
                blue(f"{first}{second}")
                self._reset_break()
                self._to_sidecar(self.pts, "#AUTO\n#EXT-X-CUE-IN\n")
                return "#AUTO\n#EXT-X-CUE-IN\n" + line
        return line

    def _reset_break(self):
        """
        _reset_break resets
        break_duration, break_timer,
        and cue_state after a CUE-IN
        """
        if self.cue_state == "IN":
            self.break_duration = None
            self.break_timer = None
            self.cue_state = None

    def _extinf(self, line):
        """
        _extinf parses lines that start with #EXTINF
        for the segment duration.
        """
        tags = TagParser([line]).tags
        if "#EXTINF" in tags:
            if isinstance(tags["#EXTINF"], str):
                tags["#EXTINF"] = tags["#EXTINF"].rsplit(",", 1)[0]
            seg_time = round(pif(tags["#EXTINF"]), 6)
            #    line = self._auto_cuein(line)
            if self.pts is not None:
                self.pts += seg_time
            if self.break_timer is not None:
                self.break_timer += seg_time
        return line

    def _print_time(self):
        """
        _print_time prints wall clock and pts.
        """
        if self.break_timer:
            gonzo = f"{REV} Break\033[;107m\033[44m {round(self.break_timer,3)}"
            if self.break_duration:
                gonzo = f"{gonzo}/{round(self.break_duration,3)}"
        ##                if self.break_timer > self.break_duration:
        ##                    print("AUTO IN HERE")
        ##                    self._auto_cuein("## AUTO IN")
        ##   \033[;107m\033[44m
        else:
            first = f"{REV}Media {NORM}"
            second = f'{self.media[-1].rsplit("/", 1)[1].split("?", 1)[0].strip()}'
            gonzo = f"{first}{second}"
        third = f"{REV}{self.hls_pts} {NORM}"
        reblue(f"{NORM}  {third}{self.pts:.6f} {gonzo}")

    def _ts_pts(self, seg):
        """
        _ts_pts set pts from segment
        """
        if seg.pts_start:
            self.pts = seg.pts_start
            self._print_time()
            self.hls_pts = "PTS"

    def _ts_cues(self, seg):
        """
        _ts_cues process SCTE-35 cues
        found in a segment.
        """
        for cue in seg.cues:
            if cue.has("packet_data"):
                self.pts = cue.packet_data.pts
            if cue.encode() != self.last_cue:
                self.last_cue = cue.encode()
                self._ts_set_cue(cue)

    def _ts_set_cue(self, cue):
        """
        _ts_set_cue validate and set cue from ts segment.
        """
        cue_pts, line = self.prof.validate_cue(cue)
        if cue_pts and line:
            self._set_cue_state(cue.encode(), line)
            self._clear()
            print(
                (NSUB).join(
                    [
                        f"\n{iso8601()}{REV} MPEGTS SCTE-35  {NORM}",
                        f"Stream PTS: {round(self.pts,6)}",
                        f"PreRoll: {round(cue_pts - self.pts,6)}",
                        f"Splice Point: {round(cue_pts,6)}",
                        f"Type: {cue.command.name}",
                        f"{self._media_stuff()}\n",
                    ]
                )
            )

    def _chk_ts(self, this):
        """
        _chk_ts  check MPEGTS for PTS and SCTE-35.
        """
        if ".ts" in this:
            if self.first_segment:
                Segment(this, key_uri=self.key_uri, iv=self.iv).show()
                print("\n\n")
            seg = Segment(this, key_uri=self.key_uri, iv=self.iv)
            seg.shushed()
            seg.decode()
            self._ts_pts(seg)
            if self.prof.parse_segments:
                self._ts_cues(seg)
            self._print_time()

    def _chk_aac(self, this):
        """
        _chk_aac check aac and ac3  HLS audio segments
        for PTS in ID3 header tags.
        """
        if ".aac" in this or ".ac3" in this:
            aac_parser = AacParser()
            pts = aac_parser.parse(this)
            if pts:
                self.pts = pts
                self.hls_pts = "PTS"
                self._print_time()

    def _new_media(self, this):
        """
        _new_media check to see
        if the media is new in a
        live sliding window
        """
        if this not in self.media:
            self.media.append(this)
            if len(self.media) > self.window_size + 1:
                self.media.popleft()
            return True
        return False

    def _parse_target_duration(self, line):
        """
        _ parse_target_duration reads target duration
         off the manifest to set self.sleep_duration.
         self.sleep_duration is used to throttle manifest
         requests.
        """
        if "TARGETDURATION" in line:
            if self.sleep_duration == 0:
                target_duration = pif(line.split(":")[1])
                self.sleep_duration = round(target_duration * 0.5, 3)
                print(f"    {REV} Target Duration {NORM} {target_duration}\n ")

    def _mk_window_size(self, lines):
        return len([line for line in lines if "#EXTINF:" in line])

    def _chk_window_size(self, lines):
        """
        mk_window_size sets the sliding window size
        for the output to match that off the input and
        determine how long to keep media data info
        for segments.
        """
        if not self.window_size:
            self.window_size = self._mk_window_size(lines)
            self.sliding_window.size = self.window_size
            print(f"    {REV} Window Size {NORM} {self.window_size}\n")

    def _update_cue_state(self):
        """
        _update_cue_state changes CUE state.
        """
        if self.cue_state == "OUT":
            self.cue_state = "CONT"
        if self.cue_state == "IN":
            self.cue_state = None

    @staticmethod
    def _decode_lines(lines):
        """
        _decode_lines convert bytes to ascii
        """
        return [line.decode() for line in lines]

    def _parse_line(self, line):
        """
        _parse_line parse a line from the manifest
        """
        if "#EXT-X-PROGRAM-DATE-TIME" in line:
            return None

        if "#EXTINF:" in line:
            line = self._extinf(line)
            return line
        self._chk_aes(line)
        line = self.scte35(line)
        return line

    def _parse_header(self, line):
        """
        _parse_headers parses m3u8 files for HLS header tags.
        """
        if "#EXT-X-PROGRAM-DATE-TIME" in line:
            return False
        splitline = line.split(":", 1)
        if splitline[0] in HEADER_TAGS:
            self._parse_target_duration(line)
            self.hls_headers.append(line)
            return True
        return False

    def _chk_endlist(self, line):
        """
        _chk_endlist disables manifest reloading
        if line contains ENDLIST tag.
        """
        if "#EXT-X-ENDLIST" in line:
            self.reload = False

    def _write_flat(self, lines, media):
        """
        _write_flat flatten out the sliding window
        and write all data to flat.m3u8.
        """
        with open(self.flat, "a", encoding="utf-8") as flat:
            if self.first_segment:
                flat.write("#EXTM3U\n")
                for hls_header in self.hls_headers:
                    flat.write(hls_header)
            for line in lines:
                flat.write(line)
            flat.write(media)

    def write_manifest(self):
        """
        write_manifest write data to sc.m3u8
        with profile rules applied.
        """
        with open(self.m3u8, "w", encoding="utf-8") as out:
            out.write("#EXTM3U\n")
            out.write("".join(self.headers))
            out.write(self.sliding_window.all_panes())

    def _parse_new_media(self, lines, media):
        self._write_flat(lines, media)
        parsed = [self._parse_line(line) for line in lines]
        lines = [line for line in parsed if line is not None]
        media = media.replace("\n", "")
        try:
            self._chk_ts(media)
        except ERR:
            try:
                self._chk_aac(media)
            except ERR:
                red(f"Skipping {media}\n")
                return
        pane = Pane(media, lines)
        self.sliding_window.slide_panes(pane)
        self.first_segment = False

    def _fixup_media(self, lines, media):
        if not media.startswith("http"):
            media = self.base_uri + "/" + media
        if self._new_media(media):
            self._parse_new_media(lines, media)

    def _post_parse(self):
        self.write_manifest()
        self.hls_headers = []
        self._update_cue_state()
        time.sleep(self.sleep_duration)

    def _parse_manifest(self):
        """
        _parse_manifest, parses m3u8 files.
        """
        if not self.rendition:
            red("No rendition to parse")
            return
        self.rendition = self.rendition.strip()
        with reader(self.rendition, headers=self.headers) as m3u8:
            lines = []
            m3u8_lines = self._decode_lines(m3u8.readlines())
            self._chk_window_size(m3u8_lines)
            for line in m3u8_lines:
                self._chk_endlist(line)
                if line.startswith("#"):
                    if not self._parse_header(line):
                        lines.append(line)
                else:
                    media = line
                    self._fixup_media(lines, media)
                    lines = []
            self._post_parse()

    def pull(self):
        """
        pull m3u8 and parse it.
        """
        print(f"{REV} Parsing Started {NORM} {iso8601()}\n")
        print(f"    {REV} Rendition Selected {NORM} {self.rendition}\n ")
        self.base_uri = self.rendition.rsplit("/", 1)[0]
        self.sliding_window = SlidingWindow()
        while self.reload:
            self._parse_manifest()
        with open(self.flat, "a", encoding="utf-8") as flat:
            flat.write("#EXT-X-ENDLIST\n")

    def _pick_one(self, arg, uri):
        """
        _pick_one  if lines come from a master.m3u8
        find the first rendition and make a uri or return uri.
        pick the first audio  only rendition or the last rendition found.
        audio  only renditions are much smaller and parse much faster.
        """
        while arg:
            line = arg.readline()
            if not line:
                break
            if line.startswith(b"#EXT-X-STREAM-INF"):
                nline = arg.readline()
                self.base_uri = uri.rsplit("/", 1)[0]
                nuri = self.base_uri + "/" + nline.decode("utf-8")
                nuri.replace("\n", "")
                print(f"{REV} Rendition Found {NORM} {nuri} ")
                self.rendition = nuri
                return
        if not self.rendition:
            self.rendition = uri

    def find_renditions(self, uri):
        """
        find_renditions search master.m3u8 for playable renditions.
        """
        with reader(uri, headers=self.headers) as arg:
            self._pick_one(arg, uri)


def _chk_help():
    for h in ['help','-h', '--help']:
        if h in sys.argv:
            print(HELPME)
            sys.exit()


def _chk_profile():
    if "profile" in sys.argv:
        scp = Scte35Profile()
        scp.write_profile("hls.profile")
        sys.exit()


def precheck():
    """
    precheck sys.argv for keywords
    that trigger a sys.exit().
    """
    _chk_help()
    _chk_profile()


def cli():
    """
    cli is a function to use in a command line tool

        #!/usr/bin/env python3

        from threefive.hls import cli

        if __name__ == "__main__":
            cli()


     is all that's required.
    """
    precheck()
    hlsparser = HlsParser()
    print(hlsparser.prof)
    print("\n\n")
    time.sleep(0.3)
    manifest = sys.argv[1]
    hlsparser.find_renditions(manifest)
    hlsparser.pull()
    sys.exit()


HELPME = """

[ scte35hls ]

[ Input ]

    scte35hls takes an m3u8 URI as input.

[what is supported]

    M3U8 formats: master, rendition
    Segment types: AAC, AC3, MPEGTS
    Video codecs: mpeg2, h.264, h.265
	Audio codecs: mpeg2, aac, ac3, mp3
    Protocols: File, Http(s), Multicast, SRT, Stdin, UDP
    Encryption: AES-128 (automatic)

[ SCTE-35 ]

  scte35hls parses SCTE-35 Embedded Cues as well as SCTE-35 HLS Tags.
  
  [ Supported HLS Tags ]
  
	* #EXT-OATCLS-SCTE35
    * #EXT-X-CUE-OUT-CONT
    * #EXT-X-DATERANGE
    * #EXT-X-SCTE35
    * #EXT-X-CUE-IN
    * #EXT-X-CUE-OUT

[ SCTE-35 Parsing Profiles ]

    SCTE-35 parsing can be fine tuned by setting a parsing profile.

    running the command:   scte35hls profile

    will generate a default profile and write a file named hls.profile
    in the current working directory.

    a@fu:~$ cat hls.profile

    expand_cues = False
    parse_segments = False
    parse_manifests = True
    hls_tags = #EXT-OATCLS-SCTE35,#EXT-X-CUE-OUT-CONT,
    #EXT-X-DATERANGE,#EXT-X-SCTE35,#EXT-X-CUE-IN,#EXT-X-CUE-OUT
    command_types = 0x6,0x5
    descriptor_tags = 0x2
    starts = 0x22,0x30,0x32,0x34,0x36,0x44,0x46

    ( Integers are show in hex (base 16),
      base 10 unsigned integers can also be used in .35rc )

    * expand_cues:       set to True to show cues fully expanded as JSON
    * parse_segments:    set to true to enable parsing SCTE-35 from MPEGTS.
    * parse_manifests:   set to true to parse the m3u8 file for SCTE-35 HLS Tags.
    * hls_tags:          set which SCTE-35 HLS Tags to parse.
    * command_types:     set which Splice Commands to parse.
    * descriptor_tags:   set which Splice Descriptor Tags to parse.
    * starts:            set which Segmentation Type IDs to use to start breaks.

    Edit the file as needed and then run threefive hls.

[ Profile Formatting Rules ]

    * Values do not need to be quoted.
    * Multiple values are separated by a commas.
    * No partial line comments. Comments must be on a separate lines.
    * Comments can be started with a # or //
    * Integers can be base 10 or base 16

[ Output Files ]
	scte35 hls creates a few output files.
        
	* Profile rules applied to the output:
    
		* hls.m3u8  - live playable rewrite of the m3u8 with the profile SCTE-35 rules.
        * hls.sidecar - list of ( pts, HLS SCTE-35 tag ) pairs
   
	* Profile rules not applied to the output:
        
		* hlsflat.m3u8  - hls live streams are flattened out into a vod playlist.
                     When the live m3u8  first loads, every line is written to hlsflat.m3u8
                     Wnen a live m3u8 is reloaded, everything except the headers
                    is appended to hlsflat.m3u8. This give you a VOD style m3u8
                    so you can fast forward or rewind while playing.
                    GREAT for debugging SCTE-35 live hls.

[ Cool Features ]

    * threefive hls can resume when started in the middle of an ad break.

            2023-10-13T05:59:50.24Z Resuming Ad Break
            2023-10-13T05:59:50.34Z Setting Break Timer to 17.733
            2023-10-13T05:59:50.44Z Setting Break Duration to 60.067

[ Example Usage ]

	* Show this help:   scte35hls help

	* Generate a new hls.profile:   scte35hls profile

	* parse an m3u8:    scte35hls  https://example.com/out/master.m3u8


scte35hls is part of threefive.

"""


if __name__ == "__main__":
    cli()
