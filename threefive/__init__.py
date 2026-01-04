"""
threefive.__init__.py
"""

from .base import SCTE35Base
from .cue import Cue
from .encode import mk_splice_insert, mk_splice_null, mk_time_signal
from .hls import HlsParser
from .hlstags import TagParser
from .iframes import IFramer
from .new_reader import reader
from .section import SpliceInfoSection
from .segment import Segment
from .sixfix import SixFix
from .speedo import Speedo
from .stream import Stream
from .superkabuki import SuperKabuki
from .throttle import Throttle
from .upids import AirId, Atsc, Eidr, Isan, Mid, Mpu, NoUpid, Umid, Upid, upid_map
from .uxp import UltraXmlParser
from .version import version
from .xml import Node

from .commands import (
    BandwidthReservation,
    PrivateCommand,
    SpliceCommand,
    SpliceInsert,
    SpliceNull,
    TimeSignal,
    command_map,
)

from .descriptors import (
    AvailDescriptor,
    DVBDASDescriptor,
    DtmfDescriptor,
    SegmentationDescriptor,
    SpliceDescriptor,
    TimeDescriptor,
    descriptor_map,
)

from .stuff import (
    badtype,
    blue,
    clean,
    codec_detect,
    ERR,
    k_by_v,
    ishex,
    isjson,
    isxml,
    iso8601,
    pif,
    print2,
    red,
    reblue,
    rmap,
)

ADRIAN = "Super Cool"
