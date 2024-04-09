# Original license
"""
This is a derived work, modified from https://github.com/mcauser/micropython-max7219.
The following newly added and/or modified code, is licensed under MIT

MicroPython max7219 cascadable 8x8 LED matrix driver
https://github.com/mcauser/micropython-max7219

MIT License
Copyright (c) 2017 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from micropython import const
import framebuf
from time import sleep

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)

__NARROWCHARACTERS = const((":", " "))


# 0-9 :
digit_pixels = [
    0x000F09090909090F,
    0x0004040404040404,
    0x000F01010F08080F,
    0x000F08080F08080F,
    0x000808080F090909,
    0x000F08080F01010F,
    0x000F09090F01010F,
    0x000808080808080F,
    0x000F09090F09090F,
    0x000F08080F09090F,
    0x0000000100010000,
]

letter_pixels = [
    0x0909090F09090600,
    0x0709090709090700,
    0x0F09010101090F00,
    0x0709090909090700,
    0x0F01010F01010F00,
    0x0101010F01010F00,
    0x0F09090D01090F00,
    0x0909090F09090900,
    0x0702020202020700,
    0x0705050404040F00,
    0x0905030303050900,
    0x0F01010101010100,
    0x111111151B111100,
    0x09090D0F0B090900,
    0x0F09090909090F00,
    0x0101010F09090F00,
    0x0C07070505050700,
    0x090D070F09090F00,
    0x0F09080F01090F00,
    0x0202020202020700,
    0x0E05050505050500,
    0x060F090909090900,
    0x111B151511111100,
    0x11111B041B111100,
    0x0606060F09090900,
    0x0F0103060C080F00,
]


class Matrix8x8:
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.

        >>> import max7219
        >>> from machine import Pin, SPI
        >>> spi = SPI(1)
        >>> display = max7219.Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234',0,0,1)
        >>> display.show()

        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num
        fb = framebuf.FrameBuffer(self.buffer, 8 * num, 8, framebuf.MONO_HLSB)
        self.framebuf = fb
        # Provide methods for accessing FrameBuffer graphics primitives. This is a workround
        # because inheritance from a native class is currently unsupported.
        # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
        self.fill = fb.fill  # (col)
        self.pixel = fb.pixel  # (x, y[, c])
        self.hline = fb.hline  # (x, y, w, col)
        self.vline = fb.vline  # (x, y, h, col)
        self.line = fb.line  # (x1, y1, x2, y2, col)
        self.rect = fb.rect  # (x, y, w, h, col)
        self.fill_rect = fb.fill_rect  # (x, y, w, h, col)
        self.text = fb.text  # (string, x, y, col=1)
        self.scroll = fb.scroll  # (dx, dy)
        self.blit = fb.blit  # (fbuf, x, y[, key])
        self.init()

    def _write(self, command, data):
        self.cs(0)
        for m in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(
                    bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]])
                )
            self.cs(1)

    def time_dense(self, text, x, y, col=1):
        i = 0
        for j in range(0, len(text)):
            self.dense_digit(text[j], x + i, y, col)
            if j < len(text) - 1:
                if text[j + 1] in __NARROWCHARACTERS or text[j] in __NARROWCHARACTERS:
                    i = i + 3
                    continue
            i = i + 5

    def time_dense_and_show(self, text, x=0, y=0, col=1):
        self.time_dense(text, x, y, col)
        self.show()

    def read_bit_from_byte(self, byte, nth_bit):
        """
        The first bit starts from the right
        """
        return byte >> nth_bit & 1

    def read_byte_from_byte_sequence(self, byte_sequence, nth_sequence):
        """
        The first byte sequence starts from the right
        """
        return byte_sequence >> nth_sequence * 8 & 0xFF

    def byte_sequence(self, byte_sequence, x, y, col=1):
        for row in range(8):
            row_byte = self.read_byte_from_byte_sequence(byte_sequence, row)
            for column in range(8):
                if self.read_bit_from_byte(row_byte, column) == 1:
                    self.pixel(column + x, row + y, col)

    def dense_digit(self, digit, x, y, col=1):
        digit_index = ord(digit) - 48

        if digit_index < 0 or digit_index > 10:
            return

        self.byte_sequence(digit_pixels[digit_index], x, y, col)

    def scroll_text(self, msg, refresh_rate=10, y=0, col=1):
        msg_len = len(msg)
        for x in range(self.num * 8, -msg_len * 8, -1):
            self.text(msg, x, y, col)
            self.show()
            sleep(1 / refresh_rate)
            self.fill(0)
