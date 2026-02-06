#!/usr/bin/env python3

"""

gums, Grande Unicast Multicast Sender


"""
import argparse
import os
import socket
import sys
import time
from functools import partial
from .udp import udp_sender, mcast_ttl
from .new_reader import reader
from .stuff import blue, reblue, print2, pif
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

    def __init__(self, addr=None, mttl=64, bind_addr="0.0.0.0"):
        self.dest_ip, self.dest_port = addr.rsplit(":", 1)
        self.src_ip = bind_addr.rsplit(":", 1)[0]
        self.src_port = 0
        self.ttl = mttl
        self.dest_grp = (self.dest_ip, pif(self.dest_port))
        self.socked = udp_sender()
        self.socked.bind((self.src_ip, self.src_port))

    def is_multicast(self):
        """
        is_multicast tests the first byte of an ipv4 address
        to see if it is in the multicast range.
        """
        net_id = pif(self.dest_ip.split(".", 1)[0])
        if net_id in range(224, 240):
            return True
        return False

    def burst(self, vid, speedo):
        """
        burst send a burst of unthrottled dgrams
        at start of stream
        """
        burst_size = 10
        blue(f"bursting {burst_size} dgrams")

        while burst_size:
            dgram = vid.read(DGRAM)
            self.socked.sendto(dgram, self.dest_grp)
            speedo.plus(len(dgram))
            burst_size -= 1

    def iter_dgrams(self, vid):
        """
        iter_dgrams iterates over the video and sends
        self.dgram_size chunks of video to the socket.
        """
        time.sleep(0.0001)
        throttle = Throttle(shush=True)
        speedo = Speedo()
        with reader(vid) as video:
            for dgram in iter(partial(video.read, DGRAM), b""):
                packets = []
                while dgram:
                    packets.append(dgram[:188])
                    dgram = dgram[188:]
                throttle.throttle(packets[0])
                dgram = b"".join(packets)
                self.socked.sendto(dgram, self.dest_grp)
                speedo.plus(len(dgram))
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
        if self.is_multicast():
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

        self.iter_dgrams(vid)
        self.socked.close()


def parse_args():
    """
    parse_args parse command line args
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default=sys.stdin.buffer,
        help=f"""like "/home/a/vid.ts"
                or "udp://@235.35.3.5:3535"
                or "https://futzu.com/xaa.ts"
                [default:{REV}sys.stdin.buffer{NORM}]
             """,
    )

    parser.add_argument(
        "-a",
        "--addr",
        default=DEFAULT_MULTICAST,
        help=f"Destination IP:Port  [default:{REV}235.35.3.5:3535{NORM}]",
    )

    parser.add_argument(
        "-b",
        "--bind_addr",
        default="0.0.0.0",
        help=f" Local IP to bind [default:{REV}0.0.0.0{NORM}]",
    )

    parser.add_argument(
        "-t",
        "--ttl",
        default=64,
        help=f"Multicast TTL (1 - 255) [default:{REV}32{NORM}]",
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
    ttl = int(args.ttl).to_bytes(1, byteorder="big")
    dest_addr = args.addr
    gummie = GumS(dest_addr, ttl, args.bind_addr)
    gummie.send_stream(args.input)
    sys.exit()


if __name__ == "__main__":
    cli()
