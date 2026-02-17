"""
xml.py  The Node class for converting to xml,
        The NameSpace Class.
        and several helper functions
"""

from .stuff import red, pif

MAXCHILDREN = 128
MAXDEPTH = 64


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
        prefix_all takes a boolean
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

    def chk_obj(self, obj):
        """
        chk_obj determines if
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
        if not slot:
            slot = len(self.children)
        self.children = self.children[:slot] + [child] + self.children[slot:]
        self.set_parent()

    def addcomment(self, comment, slot=None):
        """
        addcomment add a Comment node
        """
        self.addchild(Comment(comment), slot)
        self.set_parent()

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
        obj = self.chk_obj(obj)
        obj.parent.dropchild(obj)

    def findattr(self, attr, obj=None):
        """
        findattr  recursively searches children for all nodes that
        have an attribute that matches attr. findattr returns a NodeList.
        """
        results = NodeList()
        obj = self.chk_obj(obj)
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
        obj = self.chk_obj(obj)
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
        for k, v in self.attrs.items():
            self.addchild(Node(key2xml(k), v))
        self.attrs = {}
        for child in self.children:
            child.a2c()

    def mk(self, obj=None):
        """
        mk make the Node as xml.
        """
        #     self.a2c()
        obj = self.chk_obj(obj)
        obj.set_depth()
        obj.set_parent()
        obj.children_namespaces()
        tag = obj.mk_tag()
        ndent = obj.get_indent()
        if isinstance(obj, Comment):
            return obj.mk(obj)
        return obj.rendr_all(ndent, tag)

    def mk_tag(self):
        """
        mk_tag add namespace to node name
        """
        tag = self.tag
        if self.namespace.ns:
            tag = f"{self.namespace.ns}:{tag}"
        return tag

    def mk_ans(self, attrs):
        """
        mk_ans set namespace on attributes
        """
        new_attrs = {}
        if self.namespace.all:
            for k, v in attrs.items():
                new_attrs[f"{self.namespace.ns}:{k}"] = v
        return new_attrs

    def rendr_attrs(self, ndent, tag):
        """
        rendrd_attrs renders xml attributes
        """
        attrs = self.attrs
        if self.namespace.all:
            attrs = self.mk_ans(self.attrs)
        new_attrs = mk_xml_attrs(attrs)
        if self.depth == 0:
            return f"{ndent}<{tag} {self.namespace.xmlns()} {new_attrs}>"
        return f"{ndent}<{tag}{new_attrs}>"

    def _rendrd_children(self, rendrd, ndent, tag):
        for child in self.children:
            rendrd += self.mk(child)
        return f"{rendrd}{ndent}</{tag}>\n".replace(" >", ">")

    def rendr_all(self, ndent, tag):
        """
        rendr_all renders the Node instance and it's children in xml.
        """
        rendrd = self.rendr_attrs(ndent, tag)
        if self.value:
            return f"{rendrd}{self.value}</{tag}>\n"
        rendrd = f"{rendrd}\n"
        rendrd.replace(" >", ">")
        if self.children:
            return self._rendrd_children(rendrd, ndent, tag)
        return rendrd.replace(">", "/>")

    def set_depth(self):
        """
        set_depth is used to format
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

    def set_parent(self, obj=None):
        """
        set_parent set the parent node of this node.
        a top level node's parent will be None.
        """
        obj = self.chk_obj(obj)
        for child in obj.children:
            child.parent = obj
            child.set_parent(child)

    def children_namespaces(self):
        """
        children_namespaces give children your namespace
        """
        for child in self.children:
            child.namespace.ns = self.namespace.ns
            child.namespace.all = self.namespace.all
            child.namespace.uri = ""

    def get_indent(self):
        """
        get_indent returns a string of spaces the required depth for a node
        """
        tab = "   "
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
        obj = self.chk_obj(obj)
        obj.set_depth()
        return f"{obj.get_indent()}<!-- {obj.tag} -->\n"
