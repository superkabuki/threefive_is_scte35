"""
Ultra Xml Parser.... Supreme
"""

from .segmentation import table20, table22
from .stuff import clean, rmap, ERR
from .upids import upid_map
from .xml import Node, iter_attrs


class UltraXmlParser:
    """
    UltraXmlParser  (Supreme)
    """

    def __init__(self):
        self.openlist = []

    @staticmethod
    def _mk_attrs(line):
        """
        mk_attrs parses the current line for attributes
        """
        replace_map = {
            '"': "",
            "<": "",
            "/>": "",
            ">": "",
        }
        line = rmap(line, replace_map)
        attrs = {
            y[0]: y[1] for y in [x.split("=") for x in line.split(" ") if "=" in x]
        }
        return iter_attrs(attrs)

    @staticmethod
    def _mk_tag(data):
        """
        _mk_tag parse out the
        next available xml tag from data
        """
        return data[1:].split(" ", 1)[0].split(">")[0].strip()

    @staticmethod
    def _mk_line(exemel):
        """
        _mk_line grabs the next '<' to '>' section of xml
        """
        line = exemel.split(">", 1)[0] + ">"
        exemel = exemel.replace(line, "", 1).strip()
        return line, exemel

    def _mk_node(self, tag, line, exemel):
        """
        _mk_node marshal xml data
        into a  threefive.xml.Node instance.

        """
        ns = None
        attrs = self._mk_attrs(line)
        if ":" in tag:
            ns, tag = tag.split(":", 1)
        tag = tag.strip(">")
        node = Node(tag, attrs=attrs, ns=ns)
        if not exemel.startswith("<"):
            node.value = exemel.split("<", 1)[0]
            exemel = exemel.replace(node.value, "", 1).strip()
        return node, exemel

    def _starttag(self, line, node):
        """
        _starttag self-terminating nodes
        are added as children to the last
        node in openlist.
        open nodes (nodes that aren't self-terminating)
        are appended to openlist
        """
        if line.endswith("/>"):
            self.openlist[-1].addchild(node)
        else:
            self.openlist.append(node)

    def _endtag(self):
        """
        endtag when a node is closed
        pop it off openlist and then
        add it as a child to the last node
        in openlist, if any nodes are still in
        openlist
        """
        closed = False
        if self.openlist:
            closed = self.openlist.pop()
            if self.openlist:
                self.openlist[-1].addchild(closed)
        return closed

    @staticmethod
    def _ultraclean(exemel):
        """
        ultraclean unescapes and sanitizes exemel

        """
        exemel = clean(exemel)
        if isinstance(exemel, str):
            replace_map = {
                "\n": "",
                "&lt;": "<",
                "&gt;": ">",
                "&amp": "&",
            }
            return rmap(exemel, replace_map)
        return False

    @staticmethod
    def _nocomment(line):
        return (not line.startswith("<!")) and (not line.startswith("<?xml"))

    def parse(self, exemel):
        """
        parse xml into a node instance and
        children.
        """
        final = False
        self.openlist = []
        exemel = self._ultraclean(exemel)
        while exemel:
            line, exemel = self._mk_line(exemel)
            if self._nocomment(line):
                tag = self._mk_tag(line)
                if "/" not in tag:
                    node, exemel = self._mk_node(tag, line, exemel)
                    self._starttag(line, node)
                else:
                    final = self._endtag()
        return final


class NodeConverter:
    """
    NodeConverter class converts A SpliceInfoSection Node to a dict.
    """

    def _xmlspliceinfosection(self, node):
        """
        spliceinfosection parses exemel for info section data
        and returns a loadable dict
        """
        if "SpliceInfoSection" in node.tag:
            node.attrs["tier"] = hex(node.attrs["tier"])
            return node.attrs
        return {}

    def _xmlcommand(self, node):
        """
        command parses exemel for a splice command
        and returns a loadable dict

        """
        cmap = {
            "TimeSignal": self._xmltimesignal,
            "SpliceInsert": self._xmlspliceinsert,
            "PrivateCommand": self._xmlprivatecommand,
        }
        for child in node.children:
            if child.tag in cmap:
                out = cmap[child.tag](child)
                return out
        return {}

    def _xmltimesignal_children(self, node):
        """
        xmltimesignal_children parse vars
        from the children of a TimeSignal
        """
        for child in node.children:
            splice_time = self._xmlsplicetime(child)
            node.attrs.update(splice_time)
        return node

    def _xmltimesignal(self, node):
        """
        _xmltimesignal parses exemel for TimeSignal data
        and creates a loadable dict for the Cue class.
        """
        setme = {
            "name": "Time Signal",
            "command_type": 6,
        }

        node.attrs.update(setme)
        node = self._xmltimesignal_children(node)
        return node.attrs

    def _xmlprivatecommand(self, node):
        """
        _xmlprivatecommand parses exemel for PrivateCommand
        data and creates a loadable dict for the Cue class.
        """
        setme = {
            "command_type": 255,
            "private_bytes": node.value,
        }

        node.attrs.update(setme)
        return node.attrs

    @staticmethod
    def _xmlsplicetime(node):
        """
        splicetime parses xml from a splice command
        to get pts_time, sets time_specified_flag to True
        """
        if node.tag == "SpliceTime":
            return {
                "pts_time": node.attrs["pts_time"],
                "time_specified_flag": True,
            }
        return {}

    @staticmethod
    def _xmlbreakduration(node):
        """
        _breakduration parses xml for break duration, break_auto_return
        and sets duration_flag to True.
        """
        if node.tag == "BreakDuration":
            return {
                "break_duration": node.attrs["duration"],
                "break_auto_return": node.attrs["auto_return"],
                "duration_flag": True,
            }
        return {}

    def _xmlspliceinsert_children(self, node):
        for child in node.children:
            splice_time = self._xmlsplicetime(child)
            node.attrs.update(splice_time)
            if "pts_time" in node.attrs:
                node.attrs["program_splice_flag"] = True
            break_duration = self._xmlbreakduration(child)
            node.attrs.update(break_duration)
        return node

    def _xmlspliceinsert(self, node):
        """
        spliceinsert parses exemel for SpliceInsert data
        and creates a loadable dict for the Cue class.
        """
        setme = {
            "command_type": 5,
            "event_id_compliance_flag": True,
            "program_splice_flag": False,
            "duration_flag": False,
        }
        node.attrs.update(setme)
        node = self._xmlspliceinsert_children(node)
        return node.attrs

    @staticmethod
    def _xmldeliveryrestrictions(node):
        if node.tag == "DeliveryRestrictions":
            setme = {
                "delivery_not_restricted_flag": False,
                "device_restrictions": table20[node.attrs["device_restrictions"]],
            }
            node.attrs.update(setme)
            return node.attrs
        return {}

    @staticmethod
    def xmlupid(node):
        """
        upids parses out upids from a splice descriptors xml
        """
        if node.tag == "SegmentationUpid":
            try:
                seg_upid = bytes.fromhex(node.value.lower().replace("0x", ""))
            except ERR:
                seg_upid = node.value
            seg_upid_type = node.attrs["segmentation_upid_type"]
            return {
                "segmentation_upid": node.value,
                "segmentation_upid_type": seg_upid_type,
                "segmentation_upid_type_name": upid_map[seg_upid_type][0],
                "segmentation_upid_length": len(seg_upid),
            }
        return {}

    def _xmlsegmentationdescriptor_children(self, node):
        """
        xmlsegmentationdescriptor_children parse the children
        of a SegmentationDescriptor.
        """
        for child in node.children:
            dr = self._xmldeliveryrestrictions(child)
            node.attrs.update(dr)
            the_upid = self.xmlupid(child)
            node.attrs.update(the_upid)
        return node

    def _xmlsegmentation_message(self, node):
        if node.attrs["segmentation_type_id"] in table22:
            node.attrs["segmentation_message"] = table22[
                node.attrs["segmentation_type_id"]
            ]
        return node

    def _xmlsegmentationdescriptor(self, node):
        """
        segmentationdescriptor creates a dict to be loaded.
        """
        setme = {
            "tag": 2,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_id_compliance_indicator": True,
            "program_segmentation_flag": True,
            "segmentation_duration_flag": False,
            "delivery_not_restricted_flag": True,
            "segmentation_event_id": hex(node.attrs["segmentation_event_id"]),
        }
        node.attrs.update(setme)
        node = self._xmlsegmentation_message(node)
        node = self._xmlsegmentationdescriptor_children(node)
        return node.attrs

    def _xmlavaildescriptor(self, node):
        setme = {
            "tag": 0,
            "identifier": "CUEI",
        }
        node.attrs.update(setme)
        return node.attrs

    @staticmethod
    def _xmltimedescriptor(node):
        setme = {
            "tag": 3,
            "identifier": "CUEI",
        }
        node.attrs.update(setme)
        return node.attrs

    def _xmldescriptors(self, node):
        """
        xmldescriptors parse xml for descriptors
        """
        dmap = {
            "AvailDescriptor": self._xmlavaildescriptor,
            # "DTMFDescriptor",
            "SegmentationDescriptor": self._xmlsegmentationdescriptor,
            "TimeDescriptor": self._xmltimedescriptor,
        }
        dscripts = []
        for child in node.children:
            if child.tag in dmap:
                dscripts.append(dmap[child.tag](child))
        return dscripts

    def convert(self, node):
        return {
            "info_section": self._xmlspliceinfosection(node),
            "command": self._xmlcommand(node),
            "descriptors": self._xmldescriptors(node),
        }


def xml2cue(ex):
    """
    xml2cue parse xml to find SCTE-35 data
    """
    u = UltraXmlParser()
    if isinstance(ex,Node):
        ex=ex.mk()
    bignode = u.parse(ex)
    if isinstance(bignode, Node):
        nc = NodeConverter()
        return nc.convert(bignode)
    return False
