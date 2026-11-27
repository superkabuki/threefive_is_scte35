"""
crc.py  crc32 function for encoding.
"""

from .crctable import CRCTABLE

INIT_VALUE = 0xFFFFFFFF
EIGHT = 0x08
TWENTYFOUR = 0x18
TWOFIFTYFIVE = 0xFF


def crc32(data):
    """
    generate a 32 bit crc
    """
    crc = INIT_VALUE
    for bite in data:
        crc = CRCTABLE[bite ^ ((crc >> TWENTYFOUR) & TWOFIFTYFIVE)] ^ (
            (crc << EIGHT) & (INIT_VALUE - TWOFIFTYFIVE)
        )
    return crc


def crc32hex(data):
    """
    crc32hex crc32 returned as hex
    """
    return hex(crc32(data))
