from modules import Module
from machine import Pin, ADC


class POTMeter(Module):
    def __init__(self, name: str, pot_pin_name: int):
        self._name = name
        pot_pin = Pin(pot_pin_name, Pin.IN)  # set pot_pin modus to input
        self._adc = ADC(pot_pin)  # create ADC instance for this pin
        self.value = self._adc.read_u16()  # read voltage of pin using ADC

    def update(self):
        pass

