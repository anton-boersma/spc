from modules.module import Module
from machine import Pin, ADC
from time import ticks_us


class POTMeter(Module):

    # declare class variables
    value: int

    def __init__(self, name: str, pot_pin_name: int):
        print("POTMeter loading.")

        self._name = name

        # alle 3 typen variabele hier,
        # geen self -> deze method alleen
        # wel self. en _ is alleen deze class, ook andere methods
        # wel self. zonder _ is variabele die ook naar andere classes gaat
        pot_pin = Pin(pot_pin_name, Pin.IN)  # set pot_pin modus to input
        self._adc = ADC(pot_pin)  # create ADC instance for this pin
        self.value = self._adc.read_u16()  # read voltage of pin using ADC

        print("POTMeter loaded.")

        # time keeping
        self._previous_time = ticks_us()  # store current time
        # self._var_name _ indicates var is only used here, must be self. variable

    def __str__(self):
        return f"POTMeter(name = {self._name}, value = {self.value})"

    def update(self):
        self.value = self._adc.read_u16()
