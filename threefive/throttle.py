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

    def __init__(self, shush=False):
        self.first = None
        self.second = None
        self.actualstart = None
        self.actualstop = None
        self.ifr = IFramer(shush=True)
        self.shush = shush

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
        if not self.shush:
            print2(f"first: {pts} actualstart: {self.actualstart}")

    def print_throttle(self,diff):
        """
        print_throttle print the amount of throttle
        """
        if not self.shush:
            print2(f"throttling: {diff}", file=sys.stderr, end="\r")

    def sleep(self,diff):
        """
        sleep sleep for diff
        """
        if 0 < diff < 10:
            self.print_throttle(diff)
            time.sleep(diff)
            self.reset_end()
        else:
            self.reset()        

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
            self.sleep(diff)

    def _set_first(self,pts):
        if not self.first:
            self.set_start(pts)
            
    def _set_second(self,pts):
        if not self.second:
            self.diff(pts)        

    def throttle(self, packet):
        """
        throttle pts base throttle to maintain realtime stream.
        """
        pts = self.ifr.parse(packet)
        if pts:
            self._set_first(pts)
            if self.first:
                self._set_second(pts)
            

##class SupaStream(Stream):
##    """
##    SupaStream -Stream class with throttling
##    """
##
##    def slow(self):
##        timr = Throttle()
##        for pkt in self.iter_pkts():
##            timr.throttle(pkt)
##            cue = self._parse(pkt)
##            if cue:
##                cue.show()
##        #    sys.stdout.buffer.write(pkt)
##        #    sys.stdout.buffer.flush()
##
##
##if __name__ == "__main__":
##    ss = SupaStream(sys.argv[1])
##    ss.slow()
