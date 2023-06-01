from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff
from modules import DashboardModule, FrequencyModule


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


# werkt
class POTMeter(Module):

    # declare class variables
    value: int

    def __init__(self, name: str, pot_pin_name: int):
        self._name = name
        pot_pin = Pin(pot_pin_name, Pin.IN)
        self._adc = ADC(pot_pin)
        self.value = self._adc.read_u16()

        # time keeping
        self._previous_time = ticks_us()  # store current time

    def __str__(self):
        return f"POTMeter(name = {self._name}, value = {self.value})"

    def update(self):
        current_time = ticks_us()  # stack variable, current time is only a thing when update is called

        # only do the following code after time has elapsed
        if ticks_diff(current_time, self._previous_time) >= 10000:  # time in micro seconds, us
            self.value = self._adc.read_u16()
            self._previous_time = current_time


# werkt
class LEDBlinker(Module):
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


# werkt
class LEDFader(Module):
    def __init__(self, led_pin_name: int, pot_meter: POTMeter):
        # declare pin & PWM variables
        led_pin = Pin(led_pin_name, Pin.OUT)
        self._pot_meter = pot_meter
        self._pin_pwm = PWM(led_pin, freq=1000, duty_u16=0)

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value
        led_duty = value - 2
        self._pin_pwm.duty_u16(led_duty)

        # print out values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:
            print('PWM value:', led_duty)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time


def main():

    # sleep_ms(5000)  # pause before startup

    frequency = FrequencyModule()
    gas_pedal = POTMeter("Gas pedaal", 28)
    brake_pedal = POTMeter("Rem pedaal", 27)
    steering_wheel = POTMeter("Stuurwiel", 26)
    dashboard = DashboardModule(frequency, gas_pedal, brake_pedal, steering_wheel)

    modules = [
        frequency,
        gas_pedal,
        brake_pedal,
        steering_wheel,
        dashboard
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()
