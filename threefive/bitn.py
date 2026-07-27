"""
The bitn.Bitn and bitn.NBin classes
"""

from .stuff import red, pif




class Bitn:
    """
        bitn.Bitbin takes a byte string and
        converts it to a integer, a very large integer.
        This is used to slice off bits that are not byte-aligned
        and convert them as needed.


    example:
                    >>> from threefive.bitn import Bitn
                    >>> somebites=b'Byte String'
                    >>> bn=Bitn(somebites)
                    >>> allthebits=bin(bn.bits) # this is Bitn.bits displayed as bits
                    >>> elevenbits=bin(bn.as_int(11)) # this is the first eleven bits
                    >>> allthebits.startswith(elevenbits)
                    True
                    >>> allthebits
                    '0b100001001111001011101000110010100100000010100110111010001110010011010010110111001100111'
                    >>> elevenbits
                    '0b1000010011'
                    >>> bn.as_hex(5)
                    '0x19'
                    >>> bn.as_int(32)
                    1952784467
                    >>> next4bytes=bn.as_bytes(32)
                    >>> next4bytes
                    b'trin'


    """
    class NegShiftError(Exception):
        """
        NegShiftError inner Exception subclass
        """
        pass

    def __init__(self, bites):
        self.idx = len(bites) << 3  # This is correct, int.bit_length() is Not.
        self.bits = int.from_bytes(bites, byteorder="big")

    def __repr__(self):
        return str(vars(self))

    def as_90k(self, num_bits):
        """
        Returns num_bits
        of bits as 90k time
        """
        inted = self.as_int(num_bits)
        ninetyk= round((inted/ 90000.0),6)
        return ninetyk

    def as_int(self, num_bits):
        """
        Starting at self.idx of self.bits,
        slice off num_bits of bits.
        """
        if self.chkidx(num_bits):
            self.idx -= num_bits
            inted = (self.bits >> (self.idx)) & ~(~0 << num_bits)
            return inted
        return None

    def as_hex(self, num_bits):
        """
        Returns the hex value
        of num_bits of bits
        """
        inted =self.as_int(num_bits)
        hexed =hex(inted)
        hexed= (hexed.replace("0x", "0x0", 1), hexed)[len(hexed) % 2 == 0]
        return hexed

    def as_charset(self, num_bits, charset="ascii"):
        """
        Returns num_bits of bits
        as bytes decoded as charset
        default charset is ascii.
        """
        # print(charset)
        inted= self.as_int(num_bits)
        wide = num_bits >> 3
        if charset is None:
            chared= int.to_bytes(inted, wide, byteorder="big")
        else:
            chared= int.to_bytes(inted, wide, byteorder="big").decode(
        charset, errors="replace")
        return chared

    def as_bytes(self, num_bits):
        """
        Returns num_bits of bits
        as bytes
        """
        inted= self.as_int(num_bits)
        wide = num_bits >> 3
        byted=int.to_bytes(inted, wide, byteorder="big")
        return byted

    def as_flag(self, num_bits=1):
        """
        Returns one bit as True or False
        """
        inted= self.as_int(num_bits)
        flag = inted & 1 == 1
        return flag

    def forward(self, num_bits):
        """
        Advances the start point
        forward by num_bits
        """
        if self.chkidx(num_bits):
            self.idx -= num_bits

    def chkidx(self,num_bits):
        """
        chkidx check if we have enough
        idx left to cover num_bits.
        You can't shift what you don't have.
        """
        if self.idx < num_bits:
            mesg=f"\n\n\t\t{num_bits} bits requested, but only {self.idx} bits remain.\n"
            raise self.NegShiftError(mesg)
            return False
        return True


class NBin:
    """
    bitn.NBin is
    the reverse Bitn.
    Encodes data to integers
    and then bytes
    """

    def __init__(self):
        self.nbits = 0
        self.idx = 0
        self.bites = b""

    def nbits2bites(self):
        """
        nbits2bites converts
        the int self.nbits to bytes as self.bites
        and sets self.nbits  and self.idx to 0
        """
        bites_wide = self.idx >> 3
        self.bites += int.to_bytes(self.nbits, bites_wide, byteorder="big")
        self.nbits = 0
        self.idx = 0

    def add_bites(self, plus_bites):
        """
        add_bites appends plus_bites
        to self.bites
        """
        if isinstance(plus_bites, int):
            plus_bites = bytes.fromhex(hex(plus_bites)[2:])
        self.bites += plus_bites

    #  if self.idx % 8 == 0:
    #     self.nbits2bites()

    def add_int(self, int_bits, bit_len):
        """
        left shift nbits and append new_bits
        """
        self.idx += bit_len
        self.nbits = (self.nbits << bit_len) | int_bits
        if self.idx % 8 == 0:
            self.nbits2bites()

    def add_90k(self, pts, bit_len=33):
        """
        Converts 90k  float timestamps
        to an int and appends it to nbits
        via self.add_int
        """
        ninetyk = int(pts * 90000.0)
        self.add_int(ninetyk, bit_len)

    def add_hex(self, hex_str, bit_len):
        """
        add_hex converts a
        hex encoded string to an int
        and appends it to self.nbits
        via self.add_int
        """
        if isinstance(hex_str, str):
            dehexed = pif(hex_str)
        # just in case hex_str is an int....
        else:
            dehexed = hex_str
        self.add_int(dehexed, bit_len)

    def add_flag(self, flg, bit_len=1):
        """
        add_flag takes a boolean
        value and adds it as an integer
        to self.nbits via self.add_int
        """
        bit_len = 1
        self.add_int(flg.real, bit_len)

    def reserve(self, num):
        """
        reserve sets 'num'  bits to 1
        and appends them to self.nbits
        via self.add_int
        """
        bit_len = 1
        while num:
            self.add_int(1, bit_len)
            num -= 1

    def forward(self, num):
        """
        Currently just an alias to reserve
        """
        self.reserve(num)

    def zeroed(self, num):
        """
        zeroed sets num bits to zero
        """
        bit_len = 1
        while num:
            self.add_int(0, bit_len)
