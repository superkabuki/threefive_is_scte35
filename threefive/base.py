"""
threefive.base contains
the class SCTE35Base.
"""

import json
from .bitn import NBin
from .stuff import print2, red


class SCTE35Base:
    """
    SCTE35Base is a base class for
    SpliceCommand and SpliceDescriptor classes
    """

    ROLLOVER = 8589934591

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def _chk_nbin(nbin):
        if not nbin:
            nbin = NBin()
        return nbin

    @staticmethod
    def _err2(var_name, var_value, bit_count, var_type):
        var_type = str(var_type).split("'")[1]
        mesg = f"{var_name} is {var_value},"
        err_mesg = f"{mesg} it should be type {var_type}, {bit_count} bit(s) long."
        red(err_mesg)

    @staticmethod
    def _bool_int(var_value, var_type):
        if var_type == int:
            return isinstance(var_value, bool)
        return False

    @staticmethod
    def _wrong_type(var_value, var_type):
        return not isinstance(var_value, var_type)

    @staticmethod
    def as_90k(int_time):
        """
        ticks to 90k timestamps
        """
        return round((int_time / 90000.0), 6)

    @staticmethod
    def as_ticks(float_time):
        """
        90k timestamps to ticks
        """
        return int(round(float_time * 90000))

    @staticmethod
    def as_hms(secs_of_time):
        """
        as_hms converts timestamp to
        00:00:00.000 format
        """
        hours, seconds = divmod(secs_of_time, 3600)
        mins, seconds = divmod(seconds, 60)
        seconds = round(seconds, 3)
        output = f"{int(hours):02}:{int(mins):02}:{seconds:02}"
        if len(output.split(".")[1]) < 2:
            output += "0"
        return output

    @staticmethod
    def fix_hex(hexed):
        """
        fix_hex adds padded zero if needed for byte conversion.
        """
        return (hexed.replace("0x", "0x0", 1), hexed)[len(hexed) % 2 == 0]

    @staticmethod
    def idxsplit(gonzo, sep):
        """
        idxsplit is like split but you keep
        the sep.

        example:
                >>> idxsplit('123456789',4)
                >>>'456789'
        """
        if sep in gonzo:
            return gonzo[gonzo.index(sep) :]
        return gonzo

    @staticmethod
    def _json2dict(gonzo):
        if isinstance(gonzo, str):
            gonzo = json.loads(gonzo)
        return gonzo

    def _chk_var(self, var_type, nbin_method, var_name, bit_count):
        """
        _chk_var is used to check var values and types before encoding
        """
        var_value = self.__dict__[var_name]
        if self._bool_int(var_value, var_type) or self._wrong_type(var_value, var_type):
            self._err2(var_name, var_value, bit_count, var_type)
            return -1
        else:
            nbin_method(var_value, bit_count)
            return 0

    def get(self):
        """
        Returns instance as a kv_clean'ed dict
        """
        return self.kv_clean()

    def has(self, what):
        """
        has runs hasattr with self and what
        returns value if set.
        """
        obj = self
        if hasattr(obj, what):
            return getattr(obj, what)
        return None

    def json(self):
        """
        json returns self as kv_clean'ed json
        """
        return json.dumps(self.get(), indent=4)

    def kv_clean(self):
        """
        kv_clean recursively removes items
        from a dict if the value is None.
        """

        def b2l(val):
            if isinstance(val, SCTE35Base):
                val.kv_clean()
            if isinstance(val, (list)):
                val = [b2l(v) for v in val]
            if isinstance(val, (dict)):
                val = {k: b2l(v) for k, v in val.items()}
            if isinstance(val, (bytes, bytearray)):
                val = list(val)
            return val

        return {
            k: b2l(v)
            for k, v in vars(self).items()
            if v
            not in [
                None,
                [],
            ]
        }  # added empty list []

    def _chk_vars(self, k, v):
        if k in vars(self):
            self.__dict__[k] = v

    def _vrfy_load(self, gonzo):
        _ = {self._chk_vars(k, v) for k, v in gonzo.items()}

    def _load_dict(self, gonzo):
        if isinstance(gonzo, dict):
            self._vrfy_load(gonzo)

    def load(self, gonzo):
        """
        load is used to load
        data from a dict or json string.
        only updates vars that exist in the obj.
        """
        gonzo = self._json2dict(gonzo)
        self._load_dict(gonzo)

    def show(self):
        """
        show prints self as json to stderr (2)
        """
        print2(self.json())
