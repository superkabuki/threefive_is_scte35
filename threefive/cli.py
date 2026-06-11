#!/usr/bin/env python3

"""
threefive.cli.py

scte35 command line SCTE35 decoder.

threefivecli() is the call for the threefive cli.
"""


import select
import sys
from .iframes import IFramer
from .new_reader import reader
from .cue import Cue
from .hls import cli as hlscli
from .stream import Stream
from .stuff import print2
from .stuff import ERR
from .version import version

# import cProfile
# from sideways import cli as sidecli

REV = "\033[7;1m"
NORM = "\033[27m\033[0m"
NORM = "\033[0m"
BLUE = "\033[36;1;1m"
G = "\033[32;1;1m"
B = "\033[7;1m"
U = "\033[m"


HELP = f"""
 {B}threefive{U}{BLUE} cli tool{U}

 {B} Default      {U} {BLUE}The default action is to read a input and write a SCTE-35 output.{U}

    {BLUE}Inputs {U} mpegts, base64, hex, json,and xml, and xmlbin{U}.

    {BLUE}Outputs{U} base64, bytes, hex, int, json, xml, and xmlbin.{U}

    {BLUE}SCTE-35 can be read from {U} strings, files, stdin, DASH, HLS,
                http(s), multicast, SRT, and UDP.

 {U}{B}Input {U}    {B}Output{U}  {B}Example Command{U}

 {U}mpegts {U}   base64 {U}{BLUE} threefive https://example.com/video.ts base64{NORM}
 {U}base64 {U}   hex    {U}{BLUE} threefive '/DAWAAAAAAAAAP/wBQb+AKmKxwAACzuu2Q==' hex{NORM}
 {U}xmlbin {U}   int    {U}{BLUE} threefive < xmlbin.xml int{NORM}
 {U}xml    {U}   json   {U}{BLUE} threefive < xml.xml{NORM}
 {U}mpegts {U}   json   {U}{BLUE} threefive video.ts{NORM}
 {U}json{U}      xml    {U}{BLUE} threefive < json.json  xml{NORM}

{BLUE} Additional Commands{U}

 {B} iframes     {U}{BLUE} Show MPEGTS iframes{NORM}
    threefive iframes video.ts
 {B} proxy       {U}{NORM}{BLUE} Parse a MPEGTS stream, copy it to stdout{NORM}
    threefive proxy video.ts
 {B} pts         {U}{NORM}{BLUE} Print PTS from MPEGTS video{NORM}
    threefive pts video.ts
 {B} rt          {U}{NORM}{BLUE} Parse a MPEGTS stream, copy to stdout at realtime.{NORM}
    threefive rt video.ts
 {B} sidecar     {U}{NORM}{BLUE} Create a SCTE-35 sidecar file{NORM}
    threefive sidecar video.ts
 {B} show        {U}{NORM}{BLUE} Probe MPEGTS video{NORM}
    threefive show video.ts
 {B} speedo      {U}{NORM}{BLUE} Show MPEGTS video parse speed{NORM}
    threefive speedo video.ts
 {B} version     {U}{NORM}{BLUE} Show version{NORM}
    threefive version
 {B} help        {U}{NORM} {BLUE}Help{NORM}
    threefive help

"""


def done():
    """
    done prints the threefive version, interpreter version,
    and calls sys.exit()
    """
    print2(f"# threefive: {version} on python: {sys.version}")
    sys.exit()


def mk_sidecar(cue):
    """
    mk_sidecar generates a sidecar file with the SCTE-35 Cues
    """
    rollover = 95443.717678
    pts = 0.001
    with open("sidecar.txt", "a") as sidecar:
        cue.show()
        if cue.packet_data.pts:
            pts = cue.packet_data.pts
        if cue.command.pts_time:
            pts = (cue.command.pts_time + cue.info_section.pts_adjustment) % rollover
        data = f"{pts},{cue.encode()}\n"
        sidecar.write(data)


def mk_args(keys):
    """
    mk_args generates a list of args for inputs
    if no args are present,read from sys.stdin.buffer
    """
    return [arg for arg in sys.argv[1:] if arg not in keys]


# print_map functions
def hls():
    sys.argv.remove("hls")
    hlscli()


def print_help():
    """
    print_help checks sys.argv for the word help
    and displays the help if found
    """
    print2(HELP)
    done()


def print_version():
    """
    print_version print the threefive version
    """
    print2(version)
    done()


print_map = {
    "hls": hls,
    "-h": print_help,
    "--help": print_help,
    "help": print_help,
    "-v": print_version,
    "--version": print_version,
    "version": print_version,
}


def print_key_in_argv(key, val):
    """
    print_key_in_argv  if the key in sys.argv call val()
    """
    if key in sys.argv:
        val()
        done()


def chk_print_map():
    """
    chk_print_map checks for print_map.keys() in sys.argv
    """
    _ = [v() for k, v in print_map.items() if k in sys.argv]
    #   print_key_in_argv(k, v)


# functions for mpegts_map
def iframe_chk(this):
    """
    iframe_chk show iframes pts
    for a mpegts video.
    """
    iframer = IFramer()
    iframer.do(this)


def proxy_chk(this):
    """
    proxy_chk checks for the proxy keyword
    and proxies the stream to stdout if present.
    proxy_chk also writes pts,cue pairs to sidecar.txt
    """
    strm = Stream(this)
    strm.proxy(func=mk_sidecar)


def pts_chk(this):
    """
    pts_chk is used to display PTS.
    """
    strm = Stream(this)
    strm.show_pts()


def rt_chk(this):
    """
    rt_chk checks for the rt keyword
    and proxies the stream to stdout at realtime speed.
    rt_chk also creates a sidecar file.
    """
    strm = Stream(this)
    strm.rt(func=mk_sidecar)


def show_chk(this):
    """
    show_chk checks for the show keyword
    and displays the streams if present.
    """
    strm = Stream(this)
    strm.show()


def sidecar_chk(this):
    """
    sidecar_chk checks for the sidecar keyword and
    generates a sidecar file if present.
    """
    strm = Stream(this)
    strm.decode(func=mk_sidecar)


def speedo_chk(this):
    """
    speedo_chk displays parse speed for mpegts streams
    """
    strm = Stream(this)
    strm.speed()


mpegts_map = {
    "proxy": proxy_chk,
    "pts": pts_chk,
    "rt": rt_chk,
    "show": show_chk,
    "sidecar": sidecar_chk,
    "speedo": speedo_chk,
    "iframes": iframe_chk,
}


def mpegts_key_in_argv(args, key):
    """
    key_in_argv check if a key
    from mpegts_map is in sys.argv
    """
    if key in sys.argv:
        for arg in args:
            print2(arg)
            mpegts_map[key](arg)
        done()


def chk_mpegts_map():
    """
    chk_mpegts_map check sys.argv for mpegts_map keys
    """
    m_keys = list(mpegts_map.keys())
    args = mk_args(m_keys)
    for key in m_keys:
        mpegts_key_in_argv(args, key)


# func_map is used to generate  SCTE-35 output formats


def base64_out(cue):
    """
    print SCTE-35 from mpegts as base64
    """
    print2(cue.base64())


def bytes_out(cue):
    """
    print SCTE-35 from mpegts as base64
    """
    print2(cue.bites)


def hex_out(cue):
    """
    print SCTE-35 from mpegts as hex
    """
    print2(cue.hex())


def int_out(cue):
    """
    print SCTE-35 from mpegts as int
    """
    print2(cue.int())


def json_out(cue):
    """
    print SCTE-35 from mpegts as json
    """
    cue.show()


def xmlbin_out(cue):
    """
    xml_out prints cue as xml+binary
    """
    print2(cue.xmlbin())


def xml_out(cue):
    """
    xml_out prints cue as xml
    """
    print2(cue.xml())


funk_map = {
    "base64": base64_out,
    "bytes": bytes_out,
    "hex": hex_out,
    "int": int_out,
    "json": json_out,
    "xml": xml_out,
    "xmlbin": xmlbin_out,
}


def funk():
    """
    return a func
    if a key in out_map
    is also in sys.argv
    """
    func = json_out
    for k, v in funk_map.items():
        if k in sys.argv:
            func = v
    return func


def try_stream(this):
    """
    try_stream attempts to decode `this`
    with a Stream class instance.
    """
    strm = Stream(this)
    strm.decode(func=funk())  # funk() works here


def try_cue(this):
    """
    try_cue attempts to decode `this`
    with a Cue class instance.
    """
    cue = None
    try:
        cue = Cue(this)
        if cue:
            funk()(cue)  #   funk works here too.
    finally:
        return


def to_funk(this):
    """
    to_funk prints a cue in a variety of formats.
    """
    if this in ["", b""]:
        return
    try:
        try_stream(this)
    except ERR:
        try_cue(this)


def not_pkt(args, rdr, one):
    """
    not_pkt , runs when stdin is NOT an mpegts stream
    """
    two = rdr.read()
    args.append((one + two).decode())  # no rewind on stdin?


def is_pkt(rdr, one):
    """
    is_pkt,  runs when stdin is an mpegts stream
    """
    two = rdr.read(187)
    strm = Stream(sys.stdin.buffer)
    strm._parse(one + two)  # dont drop first packet
    strm.decode(func=funk())
    done()  # I keep forgetting why I do this


def stdin_is_readable():
    """
    stdin_is readable,  detect data on stdin.
    """
    readable, _, _ = select.select([sys.stdin], [], [], 0)
    return sys.stdin in readable  # check stdin for data


def read_stdin(args):
    """
    read_stdin read from stdin
    """
    rdr = reader(sys.stdin.buffer)
    one = rdr.read(1)
    if one not in [b"G"]:  # is this a packet?
        not_pkt(args, rdr, one)
    else:
        is_pkt(args, rdr, one)


def chk_stdin(args):
    """
    chk_stdin autodetects input from stdin.
    """
    if stdin_is_readable():
        read_stdin(args)
    return args


def chk_funk_map():
    """
    chk_func_map checks for func_map.keys() in sys.argv
    """
    funk_keys = list(funk_map.keys())
    args = mk_args(funk_keys)
    args = chk_stdin(args)
    _ = [to_funk(arg) for arg in args if args]  # multiple file input
    done()


def dashdashhelp():
    """
    dashdashhelp swaps out "help" with "--help"
    for keys in cli_map. Pure bureaucracy.
    I still can't believe I can just edit sys.argv at will,
    it kind of makes sense, since I wrote sys.argv in the first place,
    but it just feels so wrong.
    """
    if "help" in sys.argv:
        idx = sys.argv.index("help")
        sys.argv[idx] = "--help"


def chk_hls():
    """
    chk_hls  check if an  m3u8 has
    been passed on the command line
    and call the hlscli if it is an m3u8
    """
    this = sys.argv[1]
    try:
        packet = reader(this).read(188)
        if b"#EXTM3U"  in packet :
            hlscli()
            done()           
    except:
        pass


def threefivecli():
    """
    threefivecli check all the maps
    and the call functions.
    I have to do this because of
    python's  packaging drama.

    a toml file instead of python code,
    yeah, that makes sense.

    """
    dashdashhelp()
    chk_hls()
    chk_print_map()
    chk_mpegts_map()
    chk_funk_map()
