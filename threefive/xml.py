"""
xml.py  The Node class for converting to xml,
        The NameSpace Class.
        and several helper functions
"""

from .stuff import red, pif
from .stuff import clean, rmap, ERR

MAXCHILDREN = 1024
MAXDEPTH = 128


def t2s(v):
    """
    _t2s converts
    90k ticks to seconds and
    rounds to six decimal places
    """
    u = pif(v)
    if isinstance(u, int) and u > 90000:
        u = round(u / 90000.0, 6)
    return u


def un_camel(k):
    """
    camel changes camel case xml names
    to underscore_format names.
    """
    k = strip_ns(k)
    k = "".join([f"_{i.lower()}" if i.isupper() else i for i in k])
    return (k, k[1:])[k[0] == "_"]


def un_xml(v):
    """
    un_xml converts an xml value
    to ints, floats and booleans.
    """
    mapped = {
        "false": False,
        "true": True,
    }
    v = pif(v)
    if v in mapped:
        return mapped[v]
    return v


def strip_ns(this):
    """
    strip_ns strip namespace off this.
    """
    if "xmlns:" in this:
        return "xmlns"
    return this.split(":")[-1]


def iter_attrs(attrs):
    """
    iter_attrs normalizes xml attributes
    and adds them to the gonzo dict.
    """
    conv = {un_camel(k): un_xml(v) for k, v in attrs.items()}
    pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
    return {k: (t2s(v) if k in pts_vars else v) for k, v in conv.items()}


def val2xml(val):
    """
    val2xmlconvert val for xml
    """
    return str(pif(val)).lower()


def key2xml(string):
    newstring = string.title().replace("_", "")
    return newstring[0:1].lower() + newstring[1:]


def mk_xml_attrs(attrs):
    """
    mk_xml_attrs converts a dict into
    a dict of xml friendly keys and values
    """
    return "".join([f' {key2xml(k)}="{val2xml(v)}"' for k, v in attrs.items()])


class NodeList(list):
    """
    A NodeList instance is returned by Node.find()
    """

    def __init__(self, *args):
        super().__init__(*args)

    def pop(self, idx=-1):
        """
        pop remove node from list
        and from parent node by index
        """
        node = self[idx]
        node.drop()
        super().pop(idx)

    def remove(self, node):
        """
        remove drop node from parent
        and remove from list
        """
        node.drop()
        super().remove(node)


class NameSpace:
    """
    Each Node instance has a NameSpace instance
    to track namespace settings.
    @ns is the name of the namespace
    @uri is the xmlns uri
    @all is a flag to signal that all elements and
    attributes will have the namespace prefixed.
    By default only  the elements are prefixed with the namespace.
    """

    def __init__(self, ns=None, uri=None):
        self.ns = ns
        self.uri = uri
        self.all = False

    def __repr__(self):
        return str(vars(self))

    def prefix_all(self, abool=True):
        """
        prefix_all apply namespace to tags and attributes.
        True turns it on, False turns it off.
        """
        self.all = abool

    def xmlns(self):
        """
        xmlns return xmlns attribute
        """
        if not self.uri:
            return ""
        if not self.ns:
            return f'xmlns="{self.uri}"'
        return f'xmlns:{self.ns}="{self.uri}"'

    def clear(self):
        """
        clear clear namespace info
        """
        self.ns = None
        self.uri = None
        self.all = False


class Node:
    """
        The Node class is to create an xml node.

        An instance of Node has:

            tag :      <tag> </tag>

            value  :    <tag>value</tag>

            attrs :     <tag attrs[k]="attrs[v]">

            children :  <tag><children[0]></children[0]</tag>

            depth:      tab depth for printing (automatically set)

            namespace:    a NameSpace instance for the Node

    example:

            >>> from threefive.xml import Node
            >>> ts = Node('TimeSignal')
            >>> st = Node('SpliceTime',attrs={'pts_time':3442857000})
            >>> ts.addchild(st)
            >>> print(ts)
    """

    def __init__(self, tag, value="", attrs=None, ns=None):
        self.tag = tag
        self.value = value
        self.depth = 0
        self.namespace = NameSpace()
        self.namespace.ns = ns
        self.attrs = None
        self._handle_attrs(attrs)
        self.children = NodeList()
        self.parent = None

    def __repr__(self):
        return self.mk()

    def _chk_obj(self, obj):
        """
        _chk_obj determines if
        obj is self, or another obj
        for self.set_ns and self.mk
        """
        if obj is None:
            obj = self
        return obj

    def _handle_attrs(self, attrs):
        if not attrs:
            attrs = {}
        if "xmlns" in attrs:
            self.namespace.uri = attrs.pop("xmlns")
        self.attrs = attrs

    def addchild(self, child, slot=None):
        """
        addchild adds a child node
        set slot to insert at index slot.
        """
        while len(self.children) > MAXCHILDREN:
            red(f"{len(self.children)} is too many children")
            return False
        if self.value:
            red("Node.value is set, cannot add child")
            return False
        if slot is None:
            slot = len(self.children)
        if slot == 0:
            self.children = [child] + self.children
            self.mk()
        else:
            self.children = self.children[:slot] + [child] + self.children[slot:]
        self._set_parent()
        self.mk()

    def addcomment(self, comment, slot=None):
        """
        addcomment add a Comment node
        """
        self.addchild(Comment(comment), slot)
        self._set_parent()

    def addattr(self, attr, value):
        """
        addattr add an attribute
        """
        self.attrs[attr] = value

    def dropchild(self, child):
        """
        dropchild remove a child

        example:
        a_node.dropchild(a_node.children[3])
        """
        self.children.remove(child)

    def dropattr(self, attr):
        """
        dropattr remove an attribute
        """
        self.attrs.pop(attr)

    def drop(self, obj=None):
        """
        drop delete self

        """
        obj = self._chk_obj(obj)
        obj.parent.dropchild(obj)

    def findattr(self, attr, obj=None):
        """
        findattr  recursively searches children for all nodes that
        have an attribute that matches attr. findattr returns a NodeList.
        """
        results = NodeList()
        obj = self._chk_obj(obj)
        for child in obj.children:
            if attr in mk_xml_attrs(child.attrs):
                results.append(child)
            results += self.findattr(attr, obj=child)
        return results

    def findtag(self, tag, obj=None):
        """
        findtag  recursively searches children for
        all nodes with a tag that matches tag.
        findtag returns a NodeList.
        """
        results = NodeList()
        obj = self._chk_obj(obj)
        obj.mk()
        for child in obj.children:
            if tag == child.tag:
                results.append(child)
            results += self.findtag(tag, obj=child)
        return results

    def a2c(self):
        """
        a2c convert attrs to child nodes
        """
        for child in self.children:
            child.a2c()
            self.mk()
        for k, v in self.attrs.items():
            self.addchild(Node(key2xml(k), v))
        self.attrs = {}
        self.mk()

    def _valid4attr(self, child):
        """
        _valid4attr checks if a child Node
        can be converted to an attr.
        """
        if len(child.children) == 0:
            if child.attrs == {}:
                if child.value:
                    return True
        return False

    def c2a(self):
        """
        c2a convert children to attributes
        if the child has no attributes or children
        """
        for child in self.children:
            child.c2a()
        for child in self.children:
            if self._valid4attr(child):
                self.attrs[child.tag] = child.value
                self.dropchild(child)
                self.mk()
                self.c2a()
        self.mk()

    def mk(self, obj=None):
        """
        mk make the Node as xml.
        """
        obj = self._chk_obj(obj)
        obj._set_depth()
        obj._set_parent()
        obj.children_namespaces()
        tag = obj._mk_tag()
        ndent = obj._get_indent()
        if isinstance(obj, Comment):
            return obj.mk(obj)
        return obj._rendr_all(ndent, tag)

    def _mk_tag(self):
        """
        _mk_tag add namespace to node tag
        if present.
        """
        tag = self.tag
        if self.namespace.ns:
            tag = f"{self.namespace.ns}:{tag}"
        return tag

    def _mk_ans(self, attrs):
        """
        _mk_ans set namespace on attributes
        """
        new_attrs = {}
        if self.namespace.all:
            for k, v in attrs.items():
                new_attrs[f"{self.namespace.ns}:{k}"] = v
        return new_attrs

    def _rendr_attrs(self, ndent, tag):
        """
        rendrd_attrs renders xml attributes
        """
        attrs = self.attrs
        if self.namespace.all:
            attrs = self._mk_ans(self.attrs)
        new_attrs = mk_xml_attrs(attrs)
        if self.depth == 0:
            if self.namespace.uri:
                return f"{ndent}<{tag}{self.namespace.xmlns()} {new_attrs}>"
        return f"{ndent}<{tag}{new_attrs}>"

    def _rendrd_children(self, rendrd, ndent, tag):
        for child in self.children:
            rendrd += self.mk(child)
        return self._replaced(f"{rendrd}{ndent}</{tag}>\n")

    def _replaced(self, rendrd):
        """
        _replaced clean up spaces
        """
        return rendrd.replace(" >", ">").replace("\t", "    ")

    def _rendr_all(self, ndent, tag):
        """
        _rendr_all renders the Node instance and it's children in xml.
        """
        rendrd = self._rendr_attrs(ndent, tag)
        if self.value:
            return f"{rendrd}{self.value}</{tag}>\n"
        rendrd = f"{rendrd}\n"
        rendrd = self._replaced(rendrd)
        if self.children:
            return self._rendrd_children(rendrd, ndent, tag)
        rendrd = rendrd.replace(">", "/>")
        return rendrd

    def _set_depth(self):
        """
        _set_depth is used to format
        tabs in output
        """
        for child in self.children:
            while self.depth > MAXDEPTH:
                red(f"{self.depth} is too deep for SCTE-35 nodes.")
                return False
            child.depth = self.depth + 1

    def set_ns(self, ns=None):
        """
        set_ns set namespace on the Node
        """
        self.namespace.ns = ns

    def _set_parent(self, obj=None):
        """
        _set_parent set the parent node of this node.
        a top level node's parent will be None.
        """
        obj = self._chk_obj(obj)
        for child in obj.children:
            child.parent = obj
            child._set_parent(child)

    def children_namespaces(self):
        """
        children_namespaces give children your namespace
        """
        for child in self.children:
            child.namespace.ns = self.namespace.ns
            child.namespace.all = self.namespace.all
            child.namespace.uri = ""

    def _get_indent(self):
        """
        _get_indent returns a string of spaces the required depth for a node
        """
        tab = "\t"
        return tab * self.depth


class Comment(Node):
    """
    The Comment class is to create a Node representing a xml comment.

    An instance of Comment has:

        tag:      <!-- tag -->
        depth:      tab depth for printing (automatically set)

    Since Comment is a Node, it also has attrs, value and children but
    these are ignored. cf etree.Comment
    Use like this:

        from threefive.xml import Comment, Node

        n = Node('root')
        c = Comment('my first comment')

        n.addchild(c)
        print(n)

    See also Node.addcomment:
    """

    def mk(self, obj=None):
        obj = self._chk_obj(obj)
        obj._set_depth()
        return f"{obj._get_indent()}<!-- {obj.tag} -->\n"


class XmlP:
    """
    XmlP Xml Parser
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


UltraXmlParser = XmlP
