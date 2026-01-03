"""
throttle.py
MPEGTS packet level throttlinig to simulate real time streaming. 

"""

import sys
import time
from threefive import IFramer, Stream, print2


class Throttle:
    """
    Throttle
    The Throttle class is used generate a real time stream from a static source, like a file.
    pts is compared to actual elapsed time and the difference is throttled to keep the two in sync.
    the Throttle class works at the MPEGTS packet level.
    """

    def __init__(self):
        self.first = None
        self.second = None
        self.actualstart = None
        self.actualstop = None
        self.ifr = IFramer(shush=True)

    def reset(self):
        """
        reset reinitialize all four stop/start times
        """
        self.first = self.second = self.actualstart = self.actualstop = None

    def reset_end(self):
        """
        reset_end only reset the two stop tines
        """
        self.second = self.actualstop = None

    def set_start(self, pts):
        """
        set_start set first and actualstart
        """
        self.first = pts
        self.actualstart = time.time()
        print2(f"first: {pts} actual: {self.actualstart}")

    def diff(self, pts):
        """
        diff calculate the difference betweeen start and stop times,
        compare pts to actual and sleep the difference.
        """
        if pts > self.first:
            self.actualstop = time.time()
            ptime = round(pts - self.first, 6)
            atime = round(self.actualstop - self.actualstart, 6)
            diff = round((ptime - atime), 6)
            if 0 < diff < 10:
                print(f"throttling: {diff}", file=sys.stderr, end="\r")
                time.sleep(diff)
                self.reset_end()
            else:
                self.reset()

    def throttle(self, packet):
        """
        throttle pts base throttle to maintain realtime stream.
        """
        pts = self.ifr.parse(packet)
        if pts:
            if not self.first:
                self.set_start(pts)
            else:
                if not self.second:
                    self.diff(pts)


class SupaStream(Stream):
    """
    SupaStream -Stream class with throttling
    """

    def slow(self):
        timr = Throttle()
        for pkt in self.iter_pkts():
            timr.throttle(pkt)
            cue = self._parse(pkt)
            if cue:
                cue.show()
        #    sys.stdout.buffer.write(pkt)
        #    sys.stdout.buffer.flush()


if __name__ == "__main__":
    ss = SupaStream(sys.argv[1])
    ss.slow()
