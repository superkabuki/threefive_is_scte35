
import sys
import time


class Speedo:
    """
    Speedo class to calculate current transfer rate
    """

    def __init__(self):
        self.start=time.time()
        self.now =time.time
        self.total_bytes = 0
        self.million= 2 << 19

    @staticmethod
    def print_out(out):
        """
        print_out print  out
        and overwrite the previous out.
        """
        print(out, file=sys.stderr, end='\r')

    def speed(self,some_bytes):
        """
        speed calculate current transfer rate
        """
        self.total_bytes +=some_bytes
        elapsed= self.now()-self.start
        rate = (self.total_bytes/self.million)/elapsed
        mb = self.total_bytes/self.million
        out = f"\t{mb:0.2f} MB sent in {elapsed:5.2f} seconds. {rate:3.2f} MB/Sec"
        self.print_out(out)
        
    def end(self):
        """
        end advance the cursor past the \r 
        """
        out ='\n\n'
        self.print_out(out)
        


















