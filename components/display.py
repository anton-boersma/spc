from machine import Pin, SPI
from libraries.ssd1306 import SSD1306_SPI


class Display:

    def __init__(self, line_height: int = 8):
        self.display = SSD1306_SPI(128, 64, SPI(0), Pin(17), Pin(20), Pin(16))
        self.line_height = line_height

    def clear(self):
        self.display.fill(0)

    def text(self, text: str, x: int = 0, y: int = 0):
        for index, line in enumerate(text.split('\n')):
            self.display.text(line, x, y + index * self.line_height, 1)

    def box(self):
        pass

    def show(self):
        self.display.show()

# Pico => Oled
# Ground => Gnd
# 3V3 OUT => Vin
# RX => CS
# GP# => Rst
# CSn => DC/SA0
# Sck => Clk
# TX => Data
