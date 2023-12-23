import machine
import select
import struct

try:
    from micropython import const
except ImportError:

    def const(x):
        return x


class Gd5800Mp3Serial():
    EQUALIZER_NORMAL: int = const(0)
    EQUALIZER_POP: int = const(1)
    EQUALIZER_ROCK: int = const(2)
    EQUALIZER_JAZZ: int = const(3)
    EQUALIZER_CLASSIC: int = const(4)
    EQUALIZER_BASS: int = const(5)

    STATUS_STOPPED: int = const(0)
    STATUS_PLAYING: int = const(1)
    STATUS_PAUSED: int = const(2)
    STATUS_INTERRUPTING_PLAYING: int = const(5)

    LOOP_MODE_REPEAT_ALL: int = const(0)
    LOOP_MODE_REPEAT_FOLDER: int = const(1)
    LOOP_MODE_REPEAT_SINGLE: int = const(2)
    LOOP_MODE_SHUFFLE_PLAY: int = const(3)
    LOOP_MODE_SINGLE_PLAY: int = const(4)

    _COMMAND_PLAY: int = const(0x01)
    _COMMAND_PAUSE: int = const(0x02)
    _COMMAND_NEXT: int = const(0x03)
    _COMMAND_PREVIOUS: int = const(0x04)
    _COMMAND_VOLUME_UP: int = const(0x05)
    _COMMAND_VOLUME_DOWN: int = const(0x06)
    _COMMAND_PLAY_LOOP: int = const(0x07)
    _COMMAND_SHUFFLE_PLAY: int = const(0x08)
    _COMMAND_STOP_AND_PLAY_BACKGROUND_SOUND: int = const(0x09)
    _COMMAND_SHUTDOWN: int = const(0x0A)
    _COMMAND_RESET: int = const(0x0B)
    _COMMAND_STOP: int = const(0x0E)
    _COMMAND_RESUME_OR_PAUSE: int = const(0x0F)
    _COMMAND_CURRENT_PLAYING_TRACK: int = const(0x1A)
    _COMMAND_PLAY_BY_INDEX: int = const(0x41)
    _COMMAND_PLAY_SPECIFIC: int = const(0x42)
    _COMMAND_INTERLUDE: int = const(0x43)
    _COMMAND_INTERLUDE_SPECIFIC: int = const(0x44)
    _COMMAND_PLAY_ROOT_TRACK: int = const(0x45)
    _COMMAND_INTERJECT_ROOT_TRACK: int = const(0x46)
    _COMMAND_PLAY_COMBINED_LIST: int = const(0x47)
    _COMMAND_INTERJECT_COMBINED_LIST: int = const(0x48)
    _COMMAND_PLAY_SPECIFIED_TRACK_IN_LOOP: int = const(0x49)
    _COMMAND_PLAY_SPECIFIED_ROOT_TRACK: int = const(0x4A)
    _COMMAND_FAST_FORWARD: int = const(0x50)
    _COMMAND_FAST_REVERSE: int = const(0x51)

    _COMMAND_SET_VOLUME: int = const(0x31)
    _COMMAND_SET_EQUALIZER: int = const(0x32)
    _COMMAND_SET_LOOP_MODE: int = const(0x33)

    _COMMAND_GET_STATUS: int = const(0x10)
    _COMMAND_GET_VOLUME: int = const(0x11)
    _COMMAND_GET_EQUALIZER: int = const(0x12)
    _COMMAND_GET_MODE: int = const(0x13)

    def __init__(self, rx_pin, tx_pin) -> None:
        self._uart = machine.UART(1, 9600)
        self._uart.init(9600, bits=8, parity=None, stop=1, tx=tx_pin, rx=rx_pin)
        self._poll = select.poll()
        self._poll.register(self._uart, select.POLLIN)

    def _uart_read(self, count, timeout=100) -> bytearray:
        result = bytearray()
        while count > 0:
            self._poll.poll(timeout)
            if self._uart.any() == 0:
                raise OSError("uart read timeouted")
            while count > 0 and self._uart.any() > 0:
                result += self._uart.read(1)
                count -= 1
        return result

    def reset(self):
        self._write_command(self._COMMAND_RESET)

    def play(self):
        self._write_command(self._COMMAND_PLAY)

    def stop(self):
        self._write_command(self._COMMAND_STOP)

    def pause(self):
        self._write_command(self._COMMAND_PAUSE)

    def next(self):
        self._write_command(self._COMMAND_NEXT)

    def prev(self):
        self._write_command(self._COMMAND_PREVIOUS)

    def fast_forward(self):
        self._write_command(self._COMMAND_FAST_FORWARD)

    def fast_reserve(self):
        self._write_command(self._COMMAND_FAST_REVERSE)

    def play_by_index(self, index):
        # print('play_by_index:', index)
        if index < 0 or index > 0xFFFF:
            raise ValueError("index", index, "out of range (0 ~ 65535)")
        self._write_command(self._COMMAND_PLAY_BY_INDEX, (index >> 8) & 0xFF,
                            index & 0xFF)

    def volume_up(self):
        self._write_command(self._COMMAND_VOLUME_UP)

    def volume_down(self):
        self._write_command(self._COMMAND_VOLUME_DOWN)

    @property
    def status(self):
        response = self._write_command(self._COMMAND_GET_STATUS,
                                       response_length=3)
        return response[2]

    @property
    def equalizer(self):
        return self._write_command(self._COMMAND_GET_EQUALIZER,
                                   response_length=3)[2]

    @equalizer.setter
    def equalizer(self, equalizer):
        self._write_command(self._COMMAND_SET_EQUALIZER, equalizer)

    @property
    def volume(self):
        return self._write_command(self._COMMAND_GET_VOLUME,
                                   response_length=3)[2]

    @volume.setter
    def volume(self, volume):
        if volume < 0 or volume > 0x30:
            raise ValueError("volume", volume, "out of range (0 ~ 48)")
        self._write_command(self._COMMAND_SET_VOLUME, volume)

    @property
    def loop_mode(self):
        return self._write_command(self._COMMAND_GET_MODE, response_length=3)[2]

    @loop_mode.setter
    def loop_mode(self, loop_mode):
        self._write_command(self._COMMAND_SET_LOOP_MODE, loop_mode)

    # @property
    # def current_playing_track(self):
    #     return struct.unpack(
    #         ">H",
    #         self._write_command(self._COMMAND_CURRENT_PLAYING_TRACK,
    #                             response_length=3)[1:3])[0]

    def _write_command(self, *args, response_length=1):
        # print('command:', hex(args[0]))
        count = 3
        while count >= 0:
            try:
                # print('write', hex(args[0]))
                command = bytearray([0x7E])
                command.append(len(args) + 1)
                for arg in args:
                    command.append(arg)
                command.append(0xEF)
                self._uart.write(command)
                self._uart.flush()

                while True:
                    response = self._read_response()
                    if len(response
                          ) == response_length and response[0] == args[0]:
                        # print("return response:",
                        #       [hex(byte) for byte in response])
                        return response
            except Exception as ex:
                if count == 0:
                    raise ex
                # print('ex:', ex)
                pass
            count -= 1

    def _read_response(self):
        while self._uart_read(1, timeout=500)[0] != 0xAA:
            pass

        length = self._uart_read(1)[0]
        # print("length:", length)
        response = self._uart_read(length - 1)
        # print("response:", [hex(byte) for byte in response])
        if self._uart_read(1)[0] == 0xEF:
            return response
        else:
            return None
