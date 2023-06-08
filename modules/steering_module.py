from .module import Module
from components.pot_meter import POTMeter
from machine import Pin
from utime import ticks_us, ticks_diff


class SteeringModule(Module):
    def __init__(self, led_pin_name: int, pot_meter: POTMeter):
        self._led_pin = Pin(led_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value

        if value > 32000:
            self._led_pin.high()
            status = "high"

        else:
            self._led_pin.low()
            status = "low"

        # print out LED values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print(status)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time
