"""
threefive.new_reader

Home of the reader function
"""

import socket
import struct
import sys
import urllib.request

from srtfu import SRTfu, SRTO_TRANSTYPE, SRT_LIVE, SRTO_RCVSYN, SRTO_RCVBUF
from .socks import *
from .stuff import blue, ERR, pif, print2


TIMEOUT = 60

CORS = {
    "Origin": "null",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
}


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


def corsreader(uri, headers={}):
    """
    corsreader calls reader with CORS headers
    set to allow all.
    """
    all_headers = {**CORS, **headers}
    return reader(uri, headers=all_headers)


def reader(uri, headers={}):
    """
    reader returns an open file handle.
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
     (http headers can be added by setting headers)
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"

    Use like:

    with reader('http://iodisco.com/') as disco:
        disco.read()

    with reader('http://iodisco.com/',headers={"myHeader":"DOOM"}) as doom:
        doom.read()

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)

    with reader("/home/you/video.ts") as data:
        fu = data.read()

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()

    """
    # read from stdin
    if uri in [None, sys.stdin.buffer]:
        return sys.stdin.buffer
    # Multicast
    if uri.startswith("udp://@"):
        return _open_mcast(uri)
    # UDP
    if uri.startswith("udp://"):
        return _open_udp(uri)
    # HTTP(S)
    if uri.startswith("http"):
        req = urllib.request.Request(uri, headers=headers)
        return urllib.request.urlopen(req)
    # SRT
    if uri.startswith("srt://"):
        return do_srt(uri, headers=headers)
    # File
    return open(uri, "rb")


def do_srt(srt_url,headers={}):
    """
    do_srt handle Secure Reliable Transport live streams
    """
    
    preflags = {
        SRTO_TRANSTYPE: SRT_LIVE,
        SRTO_RCVSYN: 1,
        SRTO_RCVBUF: 32768000,
    }
    
    preflag.update(headers)
    srtf = SRTfu(srt_url, preflags)
    srtf.conlive()
    srtf.connect()
    return srtf


    
def _mk_socked():
    socked = Socked(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    setSO_RCVBUF(socked)
    setSO_REUSEADDR(socked)
    setSO_REUSEPORT(socked)
    setTIMEOUT(socked,TIMEOUT)
    return socked


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    blue("Opening UDP  Unicast socket")
    print2('\n')
    udp_sock = _mk_socked()
    udp_sock.bind((udp_ip, udp_port))
    return udp_sock


def _open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).rsplit(":", 1)
    udp_port = pif(udp_port)
    return _mk_udp_sock(udp_ip, udp_port)


def _open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """
    ttl = 32
    interface_ip = "0.0.0.0"
    multicast_group, port = (uri.split("udp://@")[1]).rsplit(":", 1)
    multicast_port = pif(port)
    socked = _mk_socked()
    print2('\n')
    blue("Opening Multicast socket")
    print2('\n')
    setIP_MULTICAST_TTL(socked,ttl)
    print2('\n\n')
    socked.bind(("", multicast_port))
    socked.setsockopt(
        socket.SOL_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(multicast_group) + socket.inet_aton(interface_ip),
    )
    return socked
