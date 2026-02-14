"""
threefive.__init__.py
"""

from .base import SCTE35Base
from .cue import Cue
from .encode import mk_splice_insert, mk_splice_null, mk_time_signal
from .iframes import IFramer
from .new_reader import reader
from .section import SpliceInfoSection
from .segment import Segment

from .stream import Stream

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

ADRIAN = "Super Cool"
