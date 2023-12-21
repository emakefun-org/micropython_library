import i2c_device
import time
import struct

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


class SpeechRecognizer(i2c_device.I2cDevice):
    DEFAULT_I2C_ADDRESS: int = const(0x30)

    MAX_KEYWORD_DATA_BYTES: int = const(50)

    RECOGNITION_AUTO: int = const(0)
    BUTTON_TRIGGER: int = const(1)
    KEYWORD_TRIGGER: int = const(2)
    KEYWORD_OT_BUTTON_TRIGGER: int = const(3)

    EVENT_NONE: int = const(0)
    EVENT_START_WAITING_FOR_TRIGGER: int = const(1)
    EVENT_BUTTON_TRIGGERED: int = const(2)
    EVENT_KEYWORD_TRIGGERED: int = const(3)
    EVENT_START_RECOGNIZING: int = const(4)
    EVENT_SPEECH_RECOGNIZED: int = const(5)
    EVENT_SPEECH_RECOGNITION_TIMED_OUT: int = const(6)

    DATA_ADDRESS_VERSION: int = const(0x00)
    DATA_ADDRESS_BUSY: int = const(0x01)
    DATA_ADDRESS_RESET: int = const(0x02)
    DATA_ADDRESS_RECOGNITION_MODE: int = const(0x03)
    DATA_ADDRESS_RESULT: int = const(0x04)
    DATA_ADDRESS_EVENT: int = const(0x06)
    DATA_ADDRESS_TIMEOUT: int = const(0x08)
    DATA_ADDRESS_KEYWORD_INDEX: int = const(0x0C)
    DATA_ADDRESS_KEYWORD_DATA: int = const(0x0D)
    DATA_ADDRESS_KEYWORD_LENGTH: int = const(0x3F)
    DATA_ADDRESS_ADD_KEYWORD: int = const(0x40)
    DATA_ADDRESS_RECOGNIZE: int = const(0x41)

    def __init__(self, i2c, i2c_address=DEFAULT_I2C_ADDRESS):
        super().__init__(i2c, i2c_address)
        print("SpeechRecognizer version:", self.version())
        self.reset()

    def _wait_until_idle(self):
        while True:
            self.i2c_write(SpeechRecognizer.DATA_ADDRESS_BUSY)
            if self.i2c_read_uint8() == 0:
                break
            time.sleep(0.001)

    def reset(self):
        self._wait_until_idle()
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_RESET, 1)

    def version(self):
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_VERSION)
        return self.i2c_read_uint8()

    def set_recognition_mode(self, mode):
        self._wait_until_idle()
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_RECOGNITION_MODE, mode)

    def set_timeout(self, timeout_ms):
        self._wait_until_idle()
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_TIMEOUT,
                       struct.pack("<H", timeout_ms))

    def add_keyword(self, index: int, keyword: str):
        keyword_bytes = bytes(keyword, "utf8")
        if len(keyword_bytes) > SpeechRecognizer.MAX_KEYWORD_DATA_BYTES:
            raise ValueError("the keyword length is longer than 50 bytes")

        self._wait_until_idle()
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_KEYWORD_INDEX, index)
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_KEYWORD_DATA,
                       keyword_bytes)
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_KEYWORD_LENGTH,
                       len(keyword_bytes))
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_ADD_KEYWORD, 1)

    def recognize(self) -> int:
        self._wait_until_idle()
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_RECOGNIZE, 1)
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_RESULT)
        return self.i2c_read_int16_le()

    def get_event(self):
        self.i2c_write(SpeechRecognizer.DATA_ADDRESS_EVENT)
        return self.i2c_read_uint8()
