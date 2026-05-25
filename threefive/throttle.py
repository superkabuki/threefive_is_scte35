"""
throttle.py
MPEGTS packet level throttlinig to simulate real time streaming.

"""

import sys
import time
from .iframes import IFramer


class Throttle:
    """
    Throttle
    The Throttle class is used generate a real time stream from a static source, like a file.
    pts is compared to actual elapsed time and the difference is throttled to keep the two in sync.
    the Throttle class works at the MPEGTS packet level.
    """

    def __init__(self, shush=False):
        self.first = None
        self.second = None
        self.actualstart = None
        self.actualstop = None
        self.ifr = IFramer(shush=True)
        self.shush = shush

    def ssleep(self, duration):
        """
        ssleep- a more accurate sleep.
        """
        now = time.perf_counter()
        end = now + duration
        buff = 0.002
        if duration > buff:
            time.sleep(duration - buff)
        # witness on a spin-lock
        while time.perf_counter_ns() < end:
            pass

    def _reset(self):
        """
        _reset reinitialize all four stop/start times
        """
        self.first = self.second = self.actualstart = self.actualstop = None

    def _reset_end(self):
        """
        _reset_end only reset the two stop tines
        """
        self.second = self.actualstop = None

    def _set_start(self, pts):
        """
        _set_start set first and actualstart
        """
        self.first = pts
        self.actualstart = time.perf_counter()
        if not self.shush:
            print(f"first: {pts} actualstart: {self.actualstart}")

    def _print_throttle(self, diff):
        """
        _print_throttle print the amount of throttle
        """
        if not self.shush:
            print(f"throttling: {diff}", file=sys.stderr, end="\r")

    def _diffsleep(self, diffed):
        """
        _diffsleep - sleep for diff
        """
        if 0 < diffed < 10:
            self.ssleep(diffed)
            self._print_throttle(diffed)
            self._reset_end()
        else:
            print(f"Slow: {diffed}", file=sys.stderr, end="\r")
            self._reset()

    def _diff(self, pts):
        """
        _diff - calculate the difference betweeen start and stop times,
        compare pts to actual and sleep the difference.
        """
        if pts > self.first:
            self.actualstop = time.perf_counter()
            ptime = round(pts - self.first, 6)
            atime = round(self.actualstop - self.actualstart, 6)
            diffed = round((ptime - atime) * 0.99, 6)
            self._diffsleep(diffed)

    def _set_first(self, pts):
        if not self.first:
            self._set_start(pts)

    def _set_second(self, pts):
        if not self.second:
            self._diff(pts)

    def throttle(self, packet):
        """
        throttle - throttle packet to maintain realtime stream.
        """
        pts = self.ifr.parse(packet)
        self._throttle_pts(pts)

    def throttle_time(self, seconds):
        """
        throttle_time - throttle for this many seconds

        """
        self.ssleep(seconds)

    def _throttle_pts(self, pts):
        """
        _throttle_pts - throttle by pts instead of an mpegts packet
        to maintain a realtime stream.
        """
        if pts:
            self._set_first(pts)
            if self.first:
                self._set_second(pts)
