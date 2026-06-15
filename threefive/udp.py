"""
udp.py      udp/multicast socket setting functions
"""

import socket
from .stuff import blue


TIMEOUT = 60


class Socked(socket.socket):
    """
    Socked class subclasses socket.socket
    and defines a read() method to maintain the interface.
    """

    def read(self, bites=1316):
        """
        read is just an alias for socket.socket.recv
        so anything returned by reader can call a
        read() method.
        """
        return self.recv(bites)


def _setSO_RCVBUF(socked):
    """
    _setSO_RCVBUF  left shift socket.SO_RCVBUF
    """
    shift = 7
    rcvbuf_size = socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Was { rcvbuf_size}")
    try_rcvbuf = rcvbuf_size << shift
    socked.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, try_rcvbuf)
    new_rcvbuf = socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Now { new_rcvbuf}")


def _setSO_SNDBUF(socked):
    """
    _setSO_SNDBUF  left shift socket.SO_SNDBUF
    """
    shift = 7
    sndbuf_size = socked.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    blue(f"SO_SNDBUF Was { sndbuf_size}")
    try_sndbuf = sndbuf_size << shift
    socked.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, try_sndbuf)
    new_sndbuf = socked.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    blue(f"SO_SNDBUF Now {new_sndbuf}")


def _setSO_REUSEADDR(socked):
    """
    _setSO_REUSEADDR  turn on REUSEADDR
    if present
    """
    try:
        socked.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    finally:
        blue(f"SO_REUSEADDR {socked.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)}")


def _setSO_REUSEPORT(socked):
    """
    _setSO_REUSEPORT  turn on REUSEPORT
    if present
    """
    try:
        socked.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    finally:
        blue(f"SO_REUSEPORT {socked.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT)}")


def setTIMEOUT(socked, timeout):
    """
    setTIMEOUT set TIMEOUT to timeout
    """
    socked.settimeout(timeout)
    blue(f"Socket Timeout {socked.gettimeout()}")


def setIP_MULTICAST_LOOP(socked):
    """
    setIP_MULTICAST_LOOP turn on IP_MULTICAST_LOOP
    """
    try:
        socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    finally:
        blue(
            f"IP_MULTICAST_LOOP {socked.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP)}"
        )


def mcast_ttl(socked, ttl):
    """
    mcast_ttl
    """
    socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    blue(
        f"IP_MULTICAST_TTL {socked.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)}"
    )


def _udp_flags(socked):
    """
    _udp_flags for udp and multicast sockets
    """
    setIP_MULTICAST_LOOP(socked)
    _setSO_REUSEADDR(socked)
    _setSO_REUSEPORT(socked)
    setTIMEOUT(socked, TIMEOUT)


def udp_sender():
    """
    udp_sender create
    a udp sender socket
    """
    socked = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    _setSO_SNDBUF(socked)
    _udp_flags(socked)
    return socked


def udp_receiver():
    """
    udp_receiver create
    a udp receiver socket from the Socked class
    """
    socked = Socked(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    _setSO_RCVBUF(socked)
    _udp_flags(socked)
    return socked
