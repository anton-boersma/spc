from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


class Module:
    def update(self):
        raise NotImplementedError("update methode not implemented")

    def get_output(self):
        pass


class POTMeter(Module):
    def __init__(self, pot_pin_name, led_pin_name):
        sleep_ms(2000)
        print("POTMeter loading.")
        self.pot_pin_name = pot_pin_name
        self.pot_pin = Pin(pot_pin_name, Pin.IN)
        self.adc = ADC(pot_pin_name)
        self.value = self.adc.read_u16()
        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)

        print("POTMeter loaded.")

        self.current_time = ticks_us()
        self.previous_time = self.current_time

        self.output = None

    def update(self):
        self.current_time = ticks_us()
        if ticks_diff(self.current_time, self.previous_time) >= 10000:  # time in micro seconds, us
            self.value = self.adc.read_u16()
            self.led_pwm.duty_u16(self.value)
            self.previous_time = self.current_time

    def get_output(self):
        self.output = [self.pot_pin_name, self.value]
        return self.output


class Drivetrain(Module):  # aandrijving module
    def __init__(self):
        pass

    def update(self):
        pass


modules = [
    POTMeter(28, 15)  # pot pin number GP28 or ADC2
    # Drivetrain()  # gets
]

sleep_ms(2000)  # pause voor startup

while True:
    for module in modules:
        module.update()
        print(module.get_output())

    sleep_ms(1000)


    # print(value)


