"""
threefive.Cue Class
"""

from base64 import b64decode, b64encode
import json
from .stuff import clean, red, isjson, isxml, pif
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map
from .crc import crc32
from .segmentation import table22
from .words import (
    MINUSONE,
    ZERO,
    ONE,
    TWO,
    THREE,
    FOUR,
    EIGHT,
    ELEVEN,
    FOURTEEN,
    EQUALSIGN,
)
from .xml import Node
from .uxp import xml2cue


class Cue(SCTE35Base):
    """
        The threefive.Cue class parses individual SCTE-35 Cues or messages.

    example:
        >>> import threefive
        >>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
        >>> cue = threefive.Cue(Base64)
        >>> cue.show()

        *Instance variables can be accessed via dot notation.

        >>> cue.command
        {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
        'pts_time': 21695.740089}

        >>> cue.command.pts_time=56.345
    """

    def __init__(self, data=None, packet_data=None):
        """
        data can be SCTE-35 as Base64 ,Bytes, Dict,
        Hex, Int, Json, Xml, Xml+binary,or raw MPEGTS packet.
        data can also be None.

        packet_data is a instance passed from a Stream instance
        """
        self.command = None
        self.descriptors = []
        self.info_section = SpliceInfoSection()
        self.bites = None
        if data:
            self._bits_decode(data)
        self.packet_data = packet_data
        self.decode()

    def __repr__(self):
        return str(self.__dict__)

    # decode stuff

    def _decode_descriptors(self, bites):
        """
        Cue._decode_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptor_loop
        """
        while bites:
            dll = (bites[ZERO] << EIGHT) | bites[ONE]
            self.info_section.descriptor_loop_length = dll
            bites = bites[TWO:]
            self._descriptor_loop(bites[:dll])
            return bites[dll:]
        return False

    def decode_info_section(self, bites):
        """
        Cue.decode_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = FOURTEEN
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _decode_splice_command(self, bites):
        """
        Cue._decode_splice_command parses
        the command section of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return red(f"Splice Command type {sct} not recognized")
        iscl = self.info_section.splice_command_length
        cmd_bites = bites[:iscl]
        self.command = command_map[sct](cmd_bites)
        self.command.command_length = iscl
        self.command.decode()
        del self.command.bites
        return bites[iscl:]

    def _decode_crc(self, bites):
        """
        _decode_crc decode the crc from bites
        """
        if bites:
            self.info_section.crc = hex(
                int.from_bytes(bites[ZERO:FOUR], byteorder="big")
            )
            return True
        return False

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data

        * decode doesn't need to be called directly

        """
        bites = self.bites
        self.descriptors = []
        while bites:
            bites = self.decode_info_section(bites)
            bites = self._decode_splice_command(bites)
            bites = self._decode_descriptors(bites)
            return self._decode_crc(bites)
        return False

    def _descriptor_loop(self, loop_bites):
        """
        Cue._descriptor_loop parses all splice descriptors
        """
        tag_n_len = TWO
        while len(loop_bites) > tag_n_len:
            dlen=loop_bites[1]
            sd_size = tag_n_len +  dlen #spliced.descriptor_length
            spliced = splice_descriptor(loop_bites[:sd_size])
            loop_bites = loop_bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def _get_packet_data(self, scte35_dict):
        if self.packet_data:
            scte35_dict["packet_data"] = self.packet_data.get()
        return scte35_dict

    def get(self):
        """
                Cue.get returns the SCTE-35 Cue
                data as a dict of dicts.

        example:
                >>> import threefive
                >>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
                >>> cue = threefive.Cue(Base64)
                >>> cue.get()

        """
        scte35_data = False
        if self.command and self.info_section:
            scte35_data = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            scte35_data = self._get_packet_data(scte35_data)
        return scte35_data

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def fix_bad_b64(self, data):
        """
                fix_bad_b64 fixes bad padding on Base64

        example:
                        >>> from threefive.cue import fix-bad_b64
                        >>> fix-bad_b64("/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g")
                        /DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=

        """
        while len(data) % FOUR != ZERO:
            data = data + EQUALSIGN
        return data

    # *_bits  is autodetection of SCTE-35 formats

    def _bits_b64(self, data):
        self.bites = b64decode(self.fix_bad_b64(data))

    def _bits_bytes(self, data):
        data = self._bits_pkt(data)
        self.bites = self.idxsplit(data, b"\xfc")

    def _bits_int(self, data):
        pdata = pif(data)
        if isinstance(pdata, int):
            length = pdata.bit_length() >> THREE
            bites = int.to_bytes(pdata, length, byteorder="big")
            self.bites = bites
            return True
        return False

    def _bits_node(self, data):
        """
        data is a threefive.Node instance
        """
        data = data.mk()
        self._from_xml(data)

    def _bits_pkt(self, data):
        """
        parse raw mpegts SCTE-35 packet
        """
        return data.split(b"\x00\x00\x01\xfc", ONE)[MINUSONE]

    def _bits_json_xml(self, data):
        if isjson(data) | isxml(data):
            return self.load(data)
        return False

    def _bits__bytes_or_str(self, data):
        if isinstance(
            data,
            (
                bytes,
                str,
            ),
        ):
            data = data.strip()
            return self._bits_json_xml(data)
        return False

    def _bits_precheck(self, data):
        return self._bits_int(data) | self._bits__bytes_or_str(data)

    def _bits_decode(self, data):
        """
        cue._bits_decode converts
        several SCTE-35 formats into bytes.
        """
        if not self._bits_precheck(data):
            type_map = {
                Node: self._bits_node,
                bytes: self._bits_bytes,
                dict: self.load,
                list: self.load,
                str: self._bits_b64,
            }
            td = type(data)
            if td in type_map:
                type_map[td](data)

    # encode stuff

    def _assemble(self):
        dscptr_bites = self._unloop_descriptors()
        dll = len(dscptr_bites)
        self.info_section.descriptor_loop_length = dll
        cmd_bites = self.command.encode()
        cmdl = self.command.command_length = len(cmd_bites)
        self.info_section.splice_command_length = cmdl
        self.info_section.splice_command_type = self.command.command_type
        # 11 bytes for info section + command + 2 descriptor loop length
        # + descriptor loop + 4 for crc
        self.info_section.section_length = ELEVEN + cmdl + TWO + dll + FOUR
        self.bites = self.info_section.encode()
        self.bites += cmd_bites
        self.bites += int.to_bytes(
            self.info_section.descriptor_loop_length, TWO, byteorder="big"
        )
        self.bites += dscptr_bites

    def base64(self):
        """
        base64 returns SCTE35
        encoded as a base64 string.

        example:
                >>> from threefive import Cue
                >>> cue=Cue('0xfc301600000000000000fff00506feceda3b7700000d10b0ea')
                >>> cue.base64()
                '/DAWAAAAAAAAAP/wBQb+zto7dwAADRCw6g=='
        """
        if self.command:
            self._assemble()
            self._encode_crc()
            self.decode()
            return b64encode(self.bites).decode()
        return False

    def bytes(self):
        """
        bytes returns SCTE-35
        as raw bytes

        example:
            >>> from threefive import Cue
            >>> cue=Cue('0xfc301600000000000000fff00506feceda3b7700000d10b0ea')
            >>> cue.bytes()
        """
        return self.bites

    def hex(self):
        """
        hex returns SCTE-35
        encoded as a hex string

        example:
            >>> from threefive import Cue
            >>> cue=Cue( '/DAWAAAAAAAAAP/wBQb+zto7dwAADRCw6g==')
             >>> cue.hex()
            '0xfc301600000000000000fff00506feceda3b7700000d10b0ea'
        """
        return hex(self.int())

    def int(self):
        """
        int returns SCTE-35
        encoded as an Integer

        example:
                    >>> from threefive import Cue
                    >>> cue=Cue( '/DAWAAAAAAAAAP/wBQb+zto7dwAADRCw6g==')
                    >>> cue.int()
                    1583008701074197245727019716796221243010008018887947691536618
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def encode(self):
        """
        encode is an alias for Cue.base64()
        """
        return self.base64()

    def encode_as_hex(self):
        """
        encode_as_hex  alias for Cue.hex()
        """
        return self.hex()

    def encode_as_int(self):
        """
        encode_as_int alias for Cue.int()
        """
        return self.int()

    def _encode_crc(self):
        """
        _encode_crc encode crc32
        """
        crc_int = crc32(self.bites)
        self.info_section.crc = hex(crc_int)
        self.bites += int.to_bytes(crc_int, FOUR, byteorder="big")

    def _unloop_descriptors(self):
        """
        _unloop_descriptors
        for each descriptor in self.descriptors
        encode descriptor tag, descriptor length,
        and the descriptor into all_bites.bites
        """
        nbin = NBin()
        dbite_chunks = [dsptr.encode() for dsptr in self.descriptors]
        for chunk, dsptr in zip(dbite_chunks, self.descriptors):
            dsptr.descriptor_length = len(chunk)
            nbin.add_int(dsptr.tag, EIGHT)
            nbin.add_int(dsptr.descriptor_length, EIGHT)
            nbin.add_bites(chunk)
        return nbin.bites

    # load stuff

    def _load_info_section(self, data):
        """
        load_info_section loads data for Cue.info_section
        data should be a dict.
        if 'splice_command_type' is included,
        an empty command instance will be created for Cue.command
        """
        info_sec = data
        if "info_section" in data:
            info_sec = data["info_section"]
            self.info_section.load(info_sec)

    def _load_cmd(self, data):
        """
        _load_cmd
        cmd= data or data['command']
        """
        cmd = data
        if "command" in cmd:
            cmd = data["command"]
        return cmd

    def _load_command(self, data):
        """
        load_command loads data for Cue.command
        data and data['command'] should both be dicts.
        if 'command_type' is included,
        the command instance will be created.
        """
        cmd = self._load_cmd(data)
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
            self.command.load(cmd)
        return "command_type" in cmd

    def _load_dstuff(self, dstuff):
        if "tag" in dstuff:
            dscptr = descriptor_map[dstuff["tag"]]()
            dscptr.load(dstuff)
            self.descriptors.append(dscptr)

    def _load_dlist(self, dlist):
        for dstuff in dlist:
            if isinstance(dstuff, dict):
                self._load_dstuff(dstuff)

    def _load_descriptors(self, data):
        """
        Load_descriptors loads descriptor data.
        data is a list of dicts.
        if 'tag' is included in each dict,
        a descriptor instance will be created.
        """
        dlist = data
        if "descriptors" in data:
            dlist = data["descriptors"]
        if not isinstance(dlist, list):
            return
        self._load_dlist(dlist)

    def load(self, data):
        """
        Cue.load loads SCTE35 data into the Cue instance.
        data is a dict or json or xml of a threefive.Cue instance,
        or part of a Cue instance.
       *threefive will try to determine what it is if possible.

        *You can load partial data into a Cue instance.
            for instance, you can load just the command if you want.

        *load doesn't need to be called directly
          unless you initialize a Cue without data.

        example:
                        >>> from threefive import Cue
                        >>> xml='''<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"
                        ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
                          <scte35:TimeSignal>
                              <scte35:SpliceTime ptsTime="38560.095189"/>
                            </scte35:TimeSignal>
                        </scte35:SpliceInfoSection>
                        '''
                        >>> cue=Cue()
                        >>> cue.load(xml)
                        True
        """
        if isinstance(data, bytes):
            data = clean(data)
        if isinstance(data, str):
            data=data.strip()
            if isxml(data):
                self._from_xml(data)
                return True
            data = json.loads(data)
        if isinstance(data, (dict,)):
            self._load_info_section(data)
            self._load_command(data)
        if isinstance(data, (dict,list,)):
            self._load_descriptors(data["descriptors"])
            self.encode()
            self.decode()
            return True
        return False

    ## xml stuff
    def _from_xml(self, data):
        """
        _from_xml converts xml to data that can
        be loaded by a Cue instance.
        """
        data = clean(data)
        if "Binary" in data:
            # Should be base64, but threefive allows any SCTE35 format
            b64 = data.split("Binary>", 1)[-1].split("<")[0]
            self._bits_decode(b64)
            self.decode()
        elif "SpliceInfoSection" in data:
            self.load(xml2cue(data))
        else:
            self.bites = b""
        return self.bites

    def _xml_segmentation_comment(self, dscptr, sis):
        if dscptr.segmentation_type_id in table22:
            comment = f"{table22[dscptr.segmentation_type_id]}"
        else:
            comment = (
                f"Segmentation type id {dscptr.segmentation_type_id} is not in table 22"
            )
        sis.addcomment(comment)

    def _xml_mk_descriptor(self, sis, ns):
        """
        _mk_descriptor_xml make xml nodes for descriptors.
        """
        for dscptr in self.descriptors:
            if dscptr.has("segmentation_type_id"):
                self._xml_segmentation_comment(dscptr, sis)
            sis.addchild(dscptr.xml(ns=ns))
        return sis

    def xml(self, ns="scte35"):
        """
                xml returns SCTE-35
                as xml

        example:
                        >>> import threefive
                        >>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
                        >>> cue = threefive.Cue(Base64)
                        >>> cue.xml()
        """
        self.encode()
        sis = self.info_section.xml(ns=ns)
        cmd = self.command.xml(ns=ns)
        sis.addchild(cmd)
        sis = self._xml_mk_descriptor(sis, ns)
        self.encode()
        return sis  # xml retuns a Node instance.

    def xmlbin(self, ns="scte35"):
        """
        xmlbin returns SCTE-35
        as xmlbin
        """
        xb = Node("Signal", attrs={"xmlns": "https://scte.org/schemas/35"}, ns=ns)
        xbb = Node("Binary", value=self.base64())
        xb.addchild(xbb)
        return xb
