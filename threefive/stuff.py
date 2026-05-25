"""
stuff.py functions and such common to threefive.

print2, pif, iso8601, red, blue
"""

import datetime
from os import environ
import re
from sys import stderr

ERR = (
    LookupError,
    ValueError,
    OSError,
    TypeError,
    IndexError,
    NameError,
    AttributeError,
    KeyError,
)

BLUE = "\033[7m"  # \033[44m"
RED = "\033[107m\033[41m"
RESET = " \033[0m"


write2 = True


def clean(data):
    """
    clean strip and if it's a byte string
    convert to a string
    """
    if isinstance(data, bytes):
        data = data.decode("utf8", errors="ignore")
    #   codec, data = codec_detect(data)
    if not isinstance(data, str):
        badtype(data, str)
    else:
        data = data.strip()
    return data


def ishex(data):
    """
        ishex determine if a string is a hex value.

    example:
                    >>> from threefive.stuff import ishex
                    >>> a='0x1234'
                    >>> ishex(a)
                    True

    """
    data = clean(data)
    if data is None:
        return False
    hexed = "0123456789abcdef"
    data = data.lower().strip("0x")
    return all([c in hexed for c in data])
    # return False


def isjson(data):
    """
    isjson determine if a string or bytestring
    is json.
    """
    data = clean(data)
    if data is None:
        return False
    return data.startswith("{") & data.endswith("}")


def isfloat(value):
    """
        isfloat determine if a str or bytes is a float

    example:
                    >>> from threefive.stuff import isfloat
                    >>> isfloat('1.23')
                    True
                    >>> isfloat('1.23g')
                    False
                   >>> isfloat('1.2.3')
                   False

    """
    value = clean(value)
    if value is None:
        return False
    return "." in value and value.replace(".", "", 1).isdigit()


def isxml(data):
    """
    isxml determine if a string or bytestring
    is xml.
    """
    data = clean(data)
    if data is None:
        return False
    return data.startswith("<") & data.endswith(">")


def pif(value):
    """
        pif  parses  an int or float from byte strings and strings and hex
        if it's not a string or byte string it  just returns the value.
    example:
                    >>> from threefive.stuff import pif
                    >>>> pif("bob")
                    'bob'
                    >>>> pif("12.4")
                    12.4
                    >>>> pif("0x3456")
                    13398
                    >>>> pif(b"13")
                    13
                    >>>> pif(0xdead)
                    57005
                    >>>> pif('7')
                    7

    """
    if not isinstance(
        value,
        (
            str,
            bytes,
        ),
    ):
        return value
    value = clean(value)
    value = value.strip()
    value = value.strip(",")
    if value.isdigit():
        value = int(value)
    elif ishex(value):
        value = int(value, 16)
    elif isfloat(value):
        value = float(value)
    return value


def k_by_v(adict, avalue):
    """
    dict key lookup by value
    """
    flipped = {v: k for k, v in adict.items()}
    return (None, flipped[avalue])[avalue in flipped]


def rmap(data, amap):
    """
    rmap multiple replaces applied to a string.
    works like translate but smoother
    data: string
    amap: dict

    returns string
    """
    data = data.strip()
    for k, v in amap.items():
        data = data.replace(k, v)
    return data


def _type2string(atype):
    """
    _type2string turn <class 'int'> into the string 'int'
    """
    replace_map = {
        "<class '": "",
        "'>": "",
    }
    return rmap(str(atype), replace_map)


def badtype(data, shouldbe):
    """
    badtype shows a red message that we have a wrong type.
    data can be anything.
    shouldbe is a string like "int", or "SpliceCommand"
    data: anything
    shouldbe: type
    """
    t = _type2string(type(data))
    red(f"Data needs to be type {shouldbe} not {t}")
    return False


def no_ESC(a_string):
    """
    no_ESC removes ansi colors
    from astring
    """
    esc_codes = re.compile("\x1B\\[[0-9;]*m")
    blank = ""
    return re.sub(esc_codes, blank, a_string)


def print2(gonzo=b""):
    """
        print2 prints to 2 aka stderr.

    example:
                    >>> from threefive.stuff import print2
                    >>> print2('hello')
                    hello


    """
    if "HTTP_USER_AGENT" in environ:
        print(f'<script>alert("{gonzo}");</script>')
        return
    if stderr.isatty():
        print(gonzo, file=stderr, flush=True)
        return
    no_color = no_ESC(gonzo)
    print(no_color, file=stderr, flush=True)
    return


def iso8601():
    """
    return UTC time in iso8601 format.

    '2023-05-11T15:55:51.'

    example:
                    >>> from threefive.stuff import iso8601
                    >>> iso8601()
                    '2026-02-12T13:21:05.32Z '
    """
    return f"{datetime.datetime.utcnow().isoformat()[:-4]}Z "


def red(message):
    """
    red  print error messages in red to stderr.
    """
    message = f"{RED}{message}{RESET}"
    print2(f"# {message}")
    return False


def blue(message):
    """
    blue  print info messages in blue to stderr.
    """
    message = f"{BLUE}{message}{RESET}"
    print2(f"# {message}")


def reblue(message):
    """
    reblue overwrites the last line in place
    """
    if stderr.isatty():
        message = f"{BLUE}{message}{RESET}"
    print(message, end="\r", file=stderr, flush=True)
