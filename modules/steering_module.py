from .module import Module
from components.pot_meter import POTMeter
from machine import Pin
from utime import ticks_us, ticks_diff
from libraries import Servo


def steering_angle(pot_value):
    servo_angle = pot_value/65535*180
    return servo_angle


class SteeringModule(Module):
    def __init__(self, lv_pin_name: int, rv_pin_name: int, la_pin_name: int, ra_pin_name: int, pot_meter: POTMeter):
        self._lv_pin = Servo(pin=lv_pin_name)
        self._rv_pin = Pin(rv_pin_name, Pin.OUT)
        self._la_pin = Pin(la_pin_name, Pin.OUT)
        self._ra_pin = Pin(ra_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value

        lv_angle = steering_angle(value)

        self._lv_pin.move(lv_angle)

