# from modules import LEDFader
#
# modules = [LEDFader("GP15")]
#
# while True:
#     for module in modules:
#         module.update()

from machine import Pin

Pin("GP15", Pin.OUT).high()