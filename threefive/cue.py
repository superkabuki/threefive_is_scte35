"""
threefive.Cue Class
"""

from base64 import b64decode, b64encode
import json
import re
from .stuff import clean, red, ishex, isjson, isxml
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
    SIXTEEN,
    EQUALSIGN,
)
from .xml import Node
from .uxp import xml2cue


class Cue(SCTE35Base):
    """
    The THREEfive.Cue class handles parsing
    SCTE 35 message strings.
    Example usage:

     import threefive
     Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
     cue = THREEfive.Cue(Base64)
     cue.show()

    * A cue instance can be initialized with
     Base64, Bytes, Hex, Int, Json, or Xml+binary data.

    * Instance variables can be accessed via dot notation.

     cue.command
    {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
    'pts_time': 21695.740089}

     cue.command.pts_time
    21695.740089


    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a instance passed from a Stream instance
        """
        self.command = None
        self.descriptors = []
        self.info_section = SpliceInfoSection()
        self.bites = None
        if data:
            self._mk_bits(data)
        self.packet_data = packet_data
        self.dash_data = None
        self.decode()

    def __repr__(self):
        return str(self.__dict__)

    # decode stuff

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data

        *decode doesn't need to be called directly
           unless you initialize a Cue without data.
        """
        bites = self.bites
        self.descriptors = []
        while bites:
            bites = self.mk_info_section(bites)
            bites = self._set_splice_command(bites)
            bites = self._mk_descriptors(bites)
            if bites:
                crc = hex(int.from_bytes(bites[ZERO:FOUR], byteorder="big"))
                self.info_section.crc = crc
                return True
        return False

    def _descriptor_loop(self, loop_bites):
        """
        Cue._descriptor_loop parses all splice descriptors
        """
        tag_n_len = TWO
        while len(loop_bites) > tag_n_len:
            spliced = splice_descriptor(loop_bites)
            sd_size = tag_n_len + spliced.descriptor_length
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
        """
        while len(data) % FOUR != ZERO:
            data = data + EQUALSIGN
        return data

    # mk_bits stuff

    def _int_bits(self, data):
        """
        _int_bits convert a SCTE-35 Cue from integer to bytes.
        """
        length = data.bit_length() >> THREE
        bites = int.to_bytes(data, length, byteorder="big")
        self.bites = bites

    def _hex_bits(self, data):
        """
        _hex_bits convert a SCTE-35 Cue from hex to bytes.
        """
        i = int(data, SIXTEEN)
        self._int_bits(i)

    def _b64_bits(self, data):
        """
        _b64_bits decode base64 to bytes
        """

        self.bites = b64decode(self.fix_bad_b64(data))

    def _xj_bits(self, data):
        if isxml(data) or isjson(data):
            if self.load(data):
                return True
        return False

    def _digit_bits(self, data):
        if data.isdigit():
            data = int(data)
            self._int_bits(data)
            return True
        return False

    def _xjd_bits(self, data):
        """
        _xjd_bits auto-detect xml, json, and digits
        in bytes or strings.
        """
        if isinstance(data, (str, bytes)):
            data = data.strip()
            return self._xj_bits(data) | self._digit_bits(data)
        return False

    def _str_bits(self, data):
        if self._xjd_bits(data):
            return
        if ishex(data):
            self._hex_bits(clean(data))
        else:
            self._b64_bits(data)

    def _pkt_bits(self, data):
        """
        _pkt_bits parse raw mpegts SCTE-35 packet
        """
        if data.startswith(b"G"):
            data = data.split(b"\x00\x00\x01\xfc", ONE)[MINUSONE]
        return data

    def _byte_bits(self, data):
        if self._xjd_bits(data):
            return
        data = self._pkt_bits(data)
        self.bites = self.idxsplit(data, b"\xfc")

    def _node_bits(self, data):
        data = data.mk()
        self._from_xml(data)

    def _dict_bits(self, data):
        self.load(data)

    def _mk_bits(self, data):
        """
        cue._mk_bits converts
        several SCTE-35 formats into bytes.
        """
        type_map = {
            Node: self._node_bits,
            dict: self._dict_bits,
            str: self._str_bits,
            bytes: self._byte_bits,
            int: self._int_bits,
        }

        td = type(data)
        if td in type_map.keys():
            type_map[td](data)

    # mk stuff

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
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

    def mk_info_section(self, bites):
        """
        Cue.mk_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = FOURTEEN
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        Cue._set_splice_command parses
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
        base64 Cue.base64() converts SCTE35 data
        to a base64 encoded string.
        """
        if self.command:
            self._assemble()
            self._encode_crc()
            self.decode()
            return b64encode(self.bites).decode()
        return False

    def bytes(self):
        """
        get_bytes returns Cue.bites
        """
        return self.bites

    def hex(self):
        """
        hex returns self.bites as
        a hex string
        """
        return hex(self.int())

    def int(self):
        """
        int returns self.bites as an int.
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def encode(self):
        """
        encode is an alias for base64
        """
        return self.base64()

    def encode_as_hex(self):
        """
        encode_as_hex backward compatibility
        """
        return self.hex()

    def encode_as_int(self):
        """
        encode_as_int backward compatibility
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
        all_bites = NBin()
        dbite_chunks = [dsptr.encode() for dsptr in self.descriptors]
        for chunk, dsptr in zip(dbite_chunks, self.descriptors):
            dsptr.descriptor_length = len(chunk)
            all_bites.add_int(dsptr.tag, EIGHT)
            all_bites.add_int(dsptr.descriptor_length, EIGHT)
            all_bites.add_bites(chunk)
        return all_bites.bites

    # load stuff

    def _load_info_section(self, gonzo):
        """
        load_info_section loads data for Cue.info_section
        isec should be a dict.
        if 'splice_command_type' is included,
        an empty command instance will be created for Cue.command
        """
        if "info_section" in gonzo:
            self.info_section.load(gonzo["info_section"])

    def _load_command(self, gonzo):
        """
        load_command loads data for Cue.command
        cmd should be a dict.
        if 'command_type' is included,
        the command instance will be created.
        """
        if "command" not in gonzo:
            return self._no_cmd()
        cmd = gonzo["command"]
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
            self.command.load(cmd)
        return "command_type" in cmd

    def _load_descriptors(self, dlist):
        """
        Load_descriptors loads descriptor data.
        dlist is a list of dicts
        if 'tag' is included in each dict,
        a descriptor instance will be created.
        """
        if not isinstance(dlist, list):
            red("descriptors should be a list")
        for dstuff in dlist:
            dscptr = descriptor_map[dstuff["tag"]]()
            dscptr.load(dstuff)
            self.descriptors.append(dscptr)

    def _no_cmd(self):
        """
        _no_cmd raises an exception if no splice command.
        """
        return red("A splice command is required")

    def load(self, gonzo):
        """
        Cue.load loads SCTE35 data for encoding.
        gonzo is a dict or json
        with any or all of these keys
        gonzo = {
            'info_section': {dict} ,
            'command': {dict},
            'descriptors': [list of {dicts}],
            }

        * load doesn't need to be called directly
          unless you initialize a Cue without data.
        """
        if isinstance(gonzo, bytes):
            gonzo = gonzo.decode(errors="ignore")
        # gonzo = clean(gonzo)
        if isinstance(gonzo, str):
            if isxml(gonzo):
                self._from_xml(gonzo)
                return self.bites
            gonzo = json.loads(gonzo)
        self._load_info_section(gonzo)
        self._load_command(gonzo)
        self._load_descriptors(gonzo["descriptors"])
        self.encode()
        self.decode()
        return self.bites

    ## xml stuff
    def _from_xml(self, gonzo):
        """
        _from_xml converts xml to data that can
        be loaded by a Cue instance.
        """
        gonzo = clean(gonzo)
        if "Binary" in gonzo:
            re_start = re.compile("<scte35:Binary>|<Binary>")
            re_stop = re.compile("</scte35:Binary>|</Binary>")
            dat = re.split(re_start, gonzo, 1)[1]
            dat = re.split(re_stop, dat, 1)[0]
            self._mk_bits(dat)
            self.decode()
        elif "SpliceInfoSection" in gonzo:
            self.load(xml2cue(gonzo))
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
        xml returns a threefive.Node instance
        which can be edited as needed or printed.
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
        xmlbin returns a threefive.Node instance
        which can be edited as needed or printed.
        """
        xb = Node("Signal", attrs={"xmlns": "https://scte.org/schemas/35"}, ns=ns)
        xbb = Node("Binary", value=self.base64())
        xb.addchild(xbb)
        return xb
