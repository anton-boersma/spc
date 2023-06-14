from .module import Module
from components.pot_meter import POTMeter
from libraries import Servo


class SteeringModule(Module):
    def __init__(self, lv_pin_name: int, rv_pin_name: int, la_pin_name: int, ra_pin_name: int, pot_meter: POTMeter):
        self._lv_pin = Servo(pin=lv_pin_name)
        self._rv_pin = Servo(pin=rv_pin_name)
        self._la_pin = Servo(pin=la_pin_name)
        self._ra_pin = Servo(pin=ra_pin_name)
        self._pot_meter = pot_meter

        self._multiplication_factor = 1

    def lv_steering_angle(self):
        value = self._pot_meter.value
        if value < 32767:
            max_angle = -18.43 * 2
        else:
            max_angle = -12.53 * 2
        lv_angle = (value-32768)/65535 * max_angle * self._multiplication_factor + 90
        return lv_angle

    def rv_steering_angle(self):
        value = self._pot_meter.value
        if value > 32767:
            max_angle = -18.43 * 2
        else:
            max_angle = -12.53 * 2
        rv_angle = (value-32768)/65535 * max_angle * self._multiplication_factor + 90
        return rv_angle

    def la_steering_angle(self):
        value = self._pot_meter.value
        if value < 32767:
            max_angle = 18.43 * 2
        else:
            max_angle = 12.53 * 2
        la_angle = (value-32768)/65535 * max_angle * self._multiplication_factor + 90
        return la_angle

    def ra_steering_angle(self):
        value = self._pot_meter.value
        if value > 32767:
            max_angle = 18.43 * 2
        else:
            max_angle = 12.53 * 2
        ra_angle = (value-32768)/65535 * max_angle * self._multiplication_factor + 90
        return ra_angle

    def update(self):
        lv_angle = self.lv_steering_angle()
        rv_angle = self.rv_steering_angle()
        la_angle = self.la_steering_angle()
        ra_angle = self.ra_steering_angle()

        self._lv_pin.move(lv_angle)
        self._rv_pin.move(rv_angle)
        self._la_pin.move(la_angle)
        self._ra_pin.move(ra_angle)

