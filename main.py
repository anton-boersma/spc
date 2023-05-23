from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


class Module:
    def update(self):
        raise NotImplementedError("update methode not implemented")


# werkt
class LEDBlink(Module):
    def __init__(self, led_pin_name):
        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.enabled = False

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            if self.enabled:
                self.led_pin.low()
                print("low")
                self.enabled = False
            else:
                self.led_pin.high()
                print("high")
                self.enabled = True

            self._previous_time = current_time


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
        current_time = ticks_us()  # stack variable, current time is only a thing when update is called

        # only do the following code after time has elapsed
        if ticks_diff(current_time, self._previous_time) >= 10000:  # time in micro seconds, us
            self.value = self._adc.read_u16()
            self._previous_time = current_time


class LEDBlinker(Module):
    def __init__(self):
        pass

    def update(self):
        pass


def main():

    sleep_ms(2000)  # pause before startup

    # pottie = POTMeter('')

    modules = [
        LEDBlink(15),  # led pin GP15
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()

