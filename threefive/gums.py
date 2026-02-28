#!/usr/bin/env python3

"""

gums, Grande Unicast Multicast Sender


"""
import argparse
import os
import sys
import time
from functools import partial
from .udp import udp_sender, mcast_ttl
from .new_reader import reader
from .stuff import blue, print2, pif
from .speedo import Speedo
from .throttle import Throttle

DGRAM = 1316

DEFAULT_MULTICAST = "235.35.3.5:3535"


REV = "\033[7m"
NORM = "\033[27m"


class GumS:
    """
    GumS is the Gonzo Unicast and Multicast Sender
    """

    def __init__(self, addr=None, mttl=32, bind_addr="0.0.0.0"):
        self.dest_ip, self.dest_port = addr.rsplit(":", 1)
        self.src_ip = bind_addr.rsplit(":", 1)[0]
        self.src_port = 0
        self.ttl = mttl
        self.dest_grp = (self.dest_ip, pif(self.dest_port))
        self.socked = udp_sender()
        self.socked.bind((self.src_ip, self.src_port))

    def _is_multicast(self):
        """
        _is_multicast tests the first byte of an ipv4 address
        to see if it is in the multicast range.
        """
        net_id = pif(self.dest_ip.split(".", 1)[0])
        if net_id in range(224, 240):
            return True
        return False

    def _iter_dgrams(self, vid):
        """
        _iter_dgrams iterates over the video and sends
        self.dgram_size chunks of video to the socket.
        """
        time.sleep(0.0001)
        throttle = Throttle(shush=True)
        speedo = Speedo()
        with reader(vid) as video:
            for dgram in iter(partial(video.read, DGRAM), b""):
                packets = []
                while dgram:
                    packet = dgram[:188]
                    packets.append(packet)
                    dgram = dgram[188:]
                dgram = b"".join(packets)
                self.socked.sendto(dgram, self.dest_grp)
                throttle.throttle(packets[-1])
                speedo.plus(len(dgram))
            flush=b'\xff' * 1316
            self.socked.sendto(flush, self.dest_grp)

        speedo.end()

    def send_stream(self, vid):
        """
        send_stream sets multicast ttl if needed,
        prints socket address info,
        calls self.iter_dgrams,
        and closes the socket
        """
        proto = "udp://"
        pre = "Unicast"
        if self._is_multicast():
            print2("\n")
            blue("Opening Multicast socket")
            print2("\n")
            mcast_ttl(self.socked, self.ttl)
            #     setIP_MULTICAST_LOOP(self.socked)
            proto = proto + "@"
            pre = "Multicast"
        src_ip, src_port = self.socked.getsockname()
        print2(f"\n\t{pre} Stream\n\t{proto}{self.dest_ip}:{self.dest_port}")
        print2(f"\n\tSource\n\t{src_ip}:{src_port}\n")
        self._iter_dgrams(vid)
        time.sleep(3)
        self.socked.close()


def parse_args():
    """
    parse_args parse command line args
    """

    parser = argparse.ArgumentParser( epilog="gums is part of threefive.\n\n")

    parser.add_argument(
        "-i",
        "--input",
        default=sys.stdin.buffer,
        help="""like "/home/a/vid.ts"
                or "https://futzu.com/xaa.ts"
                [default: sys.stdin.buffer]
             """,
    )


    parser.add_argument(
        "-a",
        "--addr",
        default=DEFAULT_MULTICAST,
        help="Destination IP:Port  [default: 235.35.3.5:3535]",
    )

    parser.add_argument(
        "-b",
        "--bind_addr",
        default="0.0.0.0",
        help=" Local IP to bind [default: 0.0.0.0]",
    )

    parser.add_argument(
        "-t",
        "--ttl",
        default=32,
        help="Multicast TTL (1 - 255) [default: 32]",
    )

    return parser.parse_args()


def fork():
    """
    fork
    """

    pid = os.fork()
    if pid > 0:
        sys.exit(0)


def daemonize():
    """
    The Steven's double fork
    detach process from controling tty
    """

    fork()
    fork()


def cli():
    """
    cli adds command line args
    passes them to a Gums instance
    and calls self.send_stream
    in just one function call

    Use like this

    import gums

    if __name__ == "__main__":
        gums.cli()


    """

    args = parse_args()
    # daemonize()
    ttl = pif(args.ttl).to_bytes(1, byteorder="big")
    dest_addr = args.addr
    gummie = GumS(dest_addr, ttl, args.bind_addr)
    gummie.send_stream(args.input)
    sys.exit()


if __name__ == "__main__":
    cli()
