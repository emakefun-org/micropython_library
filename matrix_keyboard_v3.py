import i2c_device

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


class MatrixKeyboardV3(i2c_device.I2cDevice):
    DEFAULT_I2C_ADDRESS: int = const(0x65)

    KEY_0: int = const(1 << 7)
    KEY_1: int = const(1 << 0)
    KEY_2: int = const(1 << 4)
    KEY_3: int = const(1 << 8)
    KEY_4: int = const(1 << 1)
    KEY_5: int = const(1 << 5)
    KEY_6: int = const(1 << 9)
    KEY_7: int = const(1 << 2)
    KEY_8: int = const(1 << 6)
    KEY_9: int = const(1 << 10)
    KEY_A: int = const(1 << 12)
    KEY_B: int = const(1 << 13)
    KEY_C: int = const(1 << 14)
    KEY_D: int = const(1 << 15)
    KEY_ASTERISK: int = const(1 << 3)
    KEY_NUMBER_SIGN: int = const(1 << 11)

    def __init__(self, i2c, i2c_address=DEFAULT_I2C_ADDRESS):
        super().__init__(i2c, i2c_address)
        self._key_states = 0
        self._last_key_states = 0

    def update(self):
        key_state = -1
        count: int = const(4)

        while key_state == -1:
            key_state = self.i2c_read_uint16le()
            for i in range(count):
                if key_state != self.i2c_read_uint16le():
                    key_state = -1
                    break

        self._last_key_states = self._key_states
        self._key_states = key_state

    def key_states(self):
        return self._key_states

    def pressed(self, key):
        return self._last_key_states & key == 0 and self._key_states & key != 0

    def pressing(self, key):
        return self._last_key_states & key != 0 and self._key_states & key != 0

    def released(self, key):
        return self._last_key_states & key != 0 and self._key_states & key == 0
