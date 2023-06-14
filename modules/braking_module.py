from .module import Module
from components.pot_meter import POTMeter
from libraries import Servo


class BrakingModule(Module):
    def __init__(self, lv_pin_name: int, rv_pin_name: int, la_pin_name: int, ra_pin_name: int, pot_meter: POTMeter):
        self._lv_pin = Servo(pin=lv_pin_name)
        self._rv_pin = Servo(pin=rv_pin_name)
        self._la_pin = Servo(pin=la_pin_name)
        self._ra_pin = Servo(pin=ra_pin_name)
        self._pot_meter = pot_meter

        self._front_balance = 0.6
        self._rear_balance = 1 - self._front_balance

        self.front_brake = None
        self.rear_brake = None

    def front_brake_factor(self):
        if self._front_balance < 0.5:
            factor = self._front_balance / self._rear_balance
        else:
            factor = 1
        return factor

    def rear_brake_factor(self):
        if self._rear_balance < 0.5:
            factor = self._rear_balance / self._front_balance
        else:
            factor = 1
        return factor

    def update(self):
        value = self._pot_meter.value
        self.front_brake = self.front_brake_factor() * value / 65536 * 180
        self.rear_brake = self.rear_brake_factor() * value / 65536 * 180

        self._lv_pin.move(180 - self.front_brake)
        self._rv_pin.move(180 - self.front_brake)
        self._la_pin.move(180 - self.rear_brake)
        self._ra_pin.move(180 - self.rear_brake)
