"""
aac.py
home of the AacParser for audio only hls renditions
"""

from .new_reader import reader
from .stuff import ERR

ROLLOVER = 95443.717678


class AacParser:
    """
    AacParser parses aac segments.
    """

    applehead = b"com.apple.streaming.transportStreamTimestamp"

    @staticmethod
    def _is_header(header):
        """
        _is_header tests aac and ac3 files for ID3 headers.
        """
        if header[:3] == b"ID3":
            return True
        return False

    @staticmethod
    def _id3_len(header):
        """
        _id3_len parses the length value from ID3 headers
        """
        id3len = int.from_bytes(header[6:], byteorder="big")
        return id3len

    @staticmethod
    def _syncsafe5(somebytes):
        """
        _syncsafe5 parses PTS from ID3 tags.
        """
        lsb = len(somebytes) - 1
        syncd = 0
        for idx, bite in enumerate(somebytes):
            syncd += bite << ((lsb - idx) << 3)
        return round(syncd / 90000.0, 6)

    def _has_applehead(self, data):
        """
        _has_applehead check for
        apple's ID3  Timestamp header
        """
        if self.applehead in data:
            return data
        return False

    def _read_id3(self, media):
        """
        _read_id3 check aac for id3 header.
        """
        data = b""
        aac = reader(media)
        header = aac.read(10)
        if self._is_header(header):
            id3len = self._id3_len(header)
            data = aac.read(id3len)
        return self._has_applehead(data)

    def _parse_timestamp(self, data, pts):
        """
        _parse_timestamp parse timestamp for pts from header.
        """
        try:
            pts = float(data.split(self.applehead)[1].split(b"\x00", 2)[1])
        except ERR:
            pts = self._syncsafe5(data.split(self.applehead)[1][:9])
        return round((pts % ROLLOVER), 6)

    def parse(self, media):
        """
        aac_pts parses the ID3 header tags in aac and ac3 audio files
        """
        pts = 0.0
        data = self._read_id3(media)
        if data:
            pts = self._parse_timestamp(data, pts)
        return pts
