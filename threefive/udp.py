"""
udp.py      udp/multicast socket setting functions
"""

import socket
from .stuff import blue


TIMEOUT = 60


def mcast_ttl(socked, ttl):
    """
    mcast_ttl
    """
    socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    print(
        f"IP_MULTICAST_TTL {socked.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)}"
    )


def set_timeout(socked, timeout):
    """
    set_timeout set timeout on socket
    """
    socked.settimeout(timeout)
    blue(f"Socket Timeout {socked.gettimeout()}")


def _set_so_rcvbuf(socked):
    """
    _set_so_rcvbuf  left shift socket.SO_RCVBUF
    """
    shift = 5
    rcvbuf_size = socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Was { rcvbuf_size}")
    try_rcvbuf = rcvbuf_size << shift
    socked.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, try_rcvbuf)
    new_rcvbuf = socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Now { new_rcvbuf}")


def _iter_flags(socked):
    """
    _iter_flags iterate and set socket flags
    """
    for k,v in { socket.SO_REUSEADDR:socket.SOL_SOCKET,
                    socket.SO_REUSEPORT:socket.SOL_SOCKET,
                    socket.IP_MULTICAST_LOOP:socket.IPPROTO_IP ,}.items():
        try:
            socked.setsockopt(v,k,1)
        except:
            pass


def _udp_flags(socked):
    """
    _udp_flags for udp and multicast sockets
    """
    _set_so_rcvbuf(socked)
    _iter_flags(socked)
    set_timeout(socked,TIMEOUT)


def udp_receiver():
    """
    udp_receiver create
    a udp receiver socket from the Socked class
    """
    socked = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    _udp_flags(socked)
    return socked
