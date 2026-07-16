"""
threefive.__init__.py
"""

from .version import version

__version__ = version

from .cue import Cue
from .iframes import IFramer
from .new_reader import reader
from .section import SpliceInfoSection
from .segment import Segment
from .stream import Stream
from .stuff import (
    print2,
    blue,
    reblue,
    red,
    pif,
    ERR,
)

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
    DtmfDescriptor,
    SegmentationDescriptor,
    SpliceDescriptor,
    TimeDescriptor,
    EventDescriptor,
    descriptor_map,
)

ADRIAN = "Super Cool"
