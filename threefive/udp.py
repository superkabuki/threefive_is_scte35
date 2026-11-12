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


def setTIMEOUT(socked, timeout):
    """
    setTIMEOUT set TIMEOUT to timeout
    """
    socked.settimeout(timeout)
    blue(f"Socket Timeout {socked.gettimeout()}")


def _udp_flags(socked):
    """
    _udp_flags for udp and multicast sockets
    """
    for k,v in {socket.SOL_SOCKET: socket.SO_REUSEADDR,
                    socket.SOL_SOCKET: socket.SO_REUSEPORT,
                    socket.IPPROTO_IP: socket.IP_MULTICAST_LOOP,}.items():
        try:
            socked.setsockopt(k,v,1)
            blue(f'{v} {socked.getsockopt(k,v)}')
        except:
            pass
    socked.settimeout(TIMEOUT)
    blue(f"Socket Timeout {socked.gettimeout()}")



def udp_receiver():
    """
    udp_receiver create
    a udp receiver socket from the Socked class
    """
    socked = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    _setSO_RCVBUF(socked)
    _udp_flags(socked)
    return socked
