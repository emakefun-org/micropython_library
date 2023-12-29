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

    def i2c_write_to(self, register_address, *args) -> None:
        self.i2c_write(register_address, args)

    def i2c_write_int8(self, value) -> None:
        self._i2c_write(self._address, struct.pack("b", value))

    def i2c_write_uint8(self, value) -> None:
        self._i2c_write(self._address, struct.pack("B", value))

    def i2c_write_int16le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<h", value))

    def i2c_write_uint16le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<H", value))

    def i2c_write_int32le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<i", value))

    def i2c_write_uint32le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<I", value))

    def i2c_write_int64le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<q", value))

    def i2c_write_uint64le(self, value) -> None:
        self._i2c_write(self._address, struct.pack("<Q", value))

    def i2c_write_int16be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">h", value))

    def i2c_write_uint16be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">H", value))

    def i2c_write_int32be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">i", value))

    def i2c_write_uint32be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">I", value))

    def i2c_write_int64be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">q", value))

    def i2c_write_uint64be(self, value) -> None:
        self._i2c_write(self._address, struct.pack(">Q", value))

    def i2c_write_int8_to(self, register_address, value) -> None:
        self._i2c_write(self._address, struct.pack("Bb", register_address,
                                                   value))

    def i2c_write_uint8_to(self, register_address, value) -> None:
        self._i2c_write(self._address, struct.pack("BB", register_address,
                                                   value))

    def i2c_write_int16le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<Bh", register_address, value))

    def i2c_write_uint16le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<BH", register_address, value))

    def i2c_write_int32le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<Bi", register_address, value))

    def i2c_write_uint32le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<BI", register_address, value))

    def i2c_write_int64le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<Bq", register_address, value))

    def i2c_write_uint64le_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack("<BQ", register_address, value))

    def i2c_write_int16be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">Bh", register_address, value))

    def i2c_write_uint16be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">BH", register_address, value))

    def i2c_write_int32be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">Bi", register_address, value))

    def i2c_write_uint32be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">BI", register_address, value))

    def i2c_write_int64be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">Bq", register_address, value))

    def i2c_write_uint64be_to(self, register_address, value) -> None:
        self._i2c_write(self._address,
                        struct.pack(">BQ", register_address, value))

    def i2c_read(self, count) -> bytes:
        return self._i2c_read(self._address, count)

    def i2c_read_from(self, register_address, count) -> bytes:
        self.i2c_write_uint8(register_address)
        return self._i2c_read(self._address, count)

    def i2c_read_byte(self):
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int8(self):
        return struct.unpack("b", self.i2c_read(1))[0]

    def i2c_read_uint8(self):
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int16le(self):
        return struct.unpack("<h", self.i2c_read(2))[0]

    def i2c_read_uint16le(self):
        return struct.unpack("<H", self.i2c_read(2))[0]

    def i2c_read_int32le(self):
        return struct.unpack("<i", self.i2c_read(4))[0]

    def i2c_read_uint32le(self):
        return struct.unpack("<I", self.i2c_read(4))[0]

    def i2c_read_int64le(self):
        return struct.unpack("<q", self.i2c_read(8))[0]

    def i2c_read_uint64le(self):
        return struct.unpack("<Q", self.i2c_read(8))[0]

    def i2c_read_int16be(self):
        return struct.unpack(">h", self.i2c_read(2))[0]

    def i2c_read_uint16be(self):
        return struct.unpack(">H", self.i2c_read(2))[0]

    def i2c_read_int32be(self):
        return struct.unpack(">i", self.i2c_read(4))[0]

    def i2c_read_uint32be(self):
        return struct.unpack(">I", self.i2c_read(4))[0]

    def i2c_read_int64be(self):
        return struct.unpack(">q", self.i2c_read(8))[0]

    def i2c_read_uint64be(self):
        return struct.unpack(">Q", self.i2c_read(8))[0]

    def i2c_read_byte_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int8_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("b", self.i2c_read(1))[0]

    def i2c_read_uint8_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("B", self.i2c_read(1))[0]

    def i2c_read_int16le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<h", self.i2c_read(2))[0]

    def i2c_read_uint16le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<H", self.i2c_read(2))[0]

    def i2c_read_int32le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<i", self.i2c_read(4))[0]

    def i2c_read_uint32le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<I", self.i2c_read(4))[0]

    def i2c_read_int64le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<q", self.i2c_read(8))[0]

    def i2c_read_uint64le_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack("<Q", self.i2c_read(8))[0]

    def i2c_read_int16be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">h", self.i2c_read(2))[0]

    def i2c_read_uint16be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">H", self.i2c_read(2))[0]

    def i2c_read_int32be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">i", self.i2c_read(4))[0]

    def i2c_read_uint32be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">I", self.i2c_read(4))[0]

    def i2c_read_int64be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">q", self.i2c_read(8))[0]

    def i2c_read_uint64be_from(self, register_address):
        self.i2c_write_uint8(register_address)
        return struct.unpack(">Q", self.i2c_read(8))[0]
