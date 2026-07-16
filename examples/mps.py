"""
mps.py - improve performance of threefive on python 3.11 and 3.14
via multiprocessing.***

*** pypy3 is still faster with just a single process.

"""
import sys
from functools import partial
from multiprocessing import Pool, set_start_method
from threefive.stream import Stream, show_cue
from threefive import reader

PKTSIZE = 188
CHUNKSIZE = PKTSIZE * 7777
POOLSIZE = 4


class MPStream:
    """
        mps = MPStream(tsstream)
        mps.decode()
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def init_pool2(self):
        """
        init_pool2 discovers the stucture of an
        MPEGTS stream to prime
        Stream instances in the pool
        init_pool2 is only called once before the Pool
        is started.(init_pool was called once per  Pool member.
        """
        stp = Stream(self.filepath)
        stp.show()
        stp.maps.prgm_pts = {}
        stp.maps.partial = {}
        return stp.pids, stp.maps

    def chunk_parser(self, pids, maps, chunk):
        """
        chunk_parser parse a chunk
        """
        st = Stream(None)
        st.pids = pids
        st.maps = maps
        return [cue for cue in [st.parse(pkt) for pkt in st.packetize(chunk)] if cue]

    def chunker(self):
        """
        chunker video chunk generator
        """
        with reader(self.filepath) as r:
            while chunk := r.read(CHUNKSIZE):
                yield chunk

    def decode(self, func=show_cue):
        """
        run create pool and parse mpegts stream
        """
        with Pool(
            POOLSIZE,
        ) as pool:
            pids, maps = self.init_pool2()
            pfunc = partial(self.chunk_parser, pids, maps)
            results = pool.imap(pfunc, self.chunker(), chunksize=3)
            _ = [func(cue) for cues in results for cue in cues]

if  __name__ == '__main__':
        tsstream=sys.argv[1]
        mps = MPStream(tsstream)
        mps.decode()
