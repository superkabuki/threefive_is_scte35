'''
socks.py      udp/multicast socket setting functions
'''



import socket
from.stuff import blue


def setSO_RCVBUF(socked):
    """
    setSO_RCVBUF  left shift socket.SO_RCVBUF
    """
    shift = 3
    rcvbuf_size = socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Was { rcvbuf_size}")
    try_rcvbuf=rcvbuf_size << shift
    socked.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, try_rcvbuf)
    new_rcvbuf= socked.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    blue(f"SO_RCVBUF Now { new_rcvbuf}")


def setSO_SNDBUF(socked):
    """
    setSO_SNDBUF  left shift socket.SO_SNDBUF
    """
    shift=3
    sndbuf_size = socked.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    blue(f"SO_SNDBUF Was { sndbuf_size}")
    try_sndbuf= sndbuf_size << shift 
    socked.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, try_sndbuf)
    new_sndbuf= socked.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    blue(f"SO_SNDBUF Now {new_sndbuf}")


def setSO_REUSEADDR(socked):
    """
    setSO_REUSEADDR  turn on REUSEADDR
    if present
    """
    if hasattr(socked, "SO_REUSEADDR"):
        socked.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        blue(f"SO_REUSEADDR {socked.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)}")


def setSO_REUSEPORT(socked):
    """
    setSO_REUSEPORT  turn on REUSEPORT
    if present
    """
    if hasattr(socked, "SO_REUSEPORT"):
        socked.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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
    if getattr(socked, "IP_MULTICAST_LOOP"):
        socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        blue(f"IP_MULTICAST_LOOP {socked.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP)}")


def setIP_MULTICAST_TTL(socked,ttl):
    """
    setIP_MULTICAST_TTL set IP_MULTICAST_TTL to ttl
    """
    socked.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    blue(f"IP_MULTICAST_TTL {socked.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)}")
    
