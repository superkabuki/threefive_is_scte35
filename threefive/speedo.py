"""
threefive.speedo.py
A Speedo class is used to
calulate data transfer rates.


"""

import sys
import time
from .stuff import print2, reblue

MILLION = 2 << 19


class Speedo:
    """
    Speedo class to calculate current transfer rate
    """

    def __init__(self):
        self.start = time.time()
        self.now = time.time
        self.total_bytes = 0

    def plus(self, this_many):
        """
        plus add to the running byte tota;l
        print current stats.
        """
        self.total_bytes += this_many
        elapsed = self.now() - self.start
        mb = self.total_bytes / MILLION
        rate = mb / elapsed
        out = f"\t{mb:0.2f} MB sent in {elapsed:5.2f} seconds. {rate:3.2f} MB/Sec     "
        reblue(out)

    def end(self):
        """
        end advance the cursor past the \r
        """
        out = "\n\n"
        print2(out)
