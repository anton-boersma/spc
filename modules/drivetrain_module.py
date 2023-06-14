from .module import Module
from components.pot_meter import POTMeter
from machine import Pin, PWM
from utime import ticks_us, ticks_diff


class DrivetrainModule(Module):
    def __init__(self, lv_pin_name: int, rv_pin_name: int, la_pin_name: int, ra_pin_name: int, pot_meter: POTMeter):
        self._lv_pin = Pin(lv_pin_name, Pin.OUT)
        self._rv_pin = Pin(rv_pin_name, Pin.OUT)
        self._la_pin = Pin(la_pin_name, Pin.OUT)
        self._ra_pin = Pin(ra_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

    def update(self):
        pass
