import machine
import struct


class I2cDevice:

    def __init__(self, i2c, i2c_address) -> None:
        self._i2c = i2c
        self._address = i2c_address
        self._i2c_write = self._i2c.writeto
        self._i2c_read = self._i2c.readfrom

    def i2c_write(self, *args) -> None:
        data = bytearray()
        for arg in args:
            if isinstance(arg, (bytes, bytearray)):
                data += arg
            elif isinstance(arg, str):
                data += bytes(arg, "utf8")
            elif isinstance(arg, (tuple, list)):
                data += bytes(arg)
            else:
                data.append(arg)
        return self._i2c_write(self._address, data)

    def i2c_read(self, count) -> bytes:
        return self._i2c_read(self._address, count)

    def i2c_read_byte(self):
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int8(self):
        return struct.unpack("b", self.i2c_read(1))[0]

    def i2c_read_uint8(self):
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int16_le(self):
        return struct.unpack("<h", self.i2c_read(2))[0]

    def i2c_read_uint16_le(self):
        return struct.unpack("<H", self.i2c_read(2))[0]

    def i2c_read_int32_le(self):
        return struct.unpack("<i", self.i2c_read(4))[0]

    def i2c_read_uint32_le(self):
        return struct.unpack("<I", self.i2c_read(4))[0]

    def i2c_read_int64_le(self):
        return struct.unpack("<q", self.i2c_read(8))[0]

    def i2c_read_uint64_le(self):
        return struct.unpack("<Q", self.i2c_read(8))[0]

    def i2c_read_int16_be(self):
        return struct.unpack(">h", self.i2c_read(2))[0]

    def i2c_read_uint16_be(self):
        return struct.unpack(">H", self.i2c_read(2))[0]

    def i2c_read_int32_be(self):
        return struct.unpack(">i", self.i2c_read(4))[0]

    def i2c_read_uint32_be(self):
        return struct.unpack(">I", self.i2c_read(4))[0]

    def i2c_read_int64_be(self):
        return struct.unpack(">q", self.i2c_read(8))[0]

    def i2c_read_uint64_be(self):
        return struct.unpack(">Q", self.i2c_read(8))[0]
