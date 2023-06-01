from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


class Module:
    def update(self):
        raise NotImplementedError("update methode not implemented")


class LEDFader(Module):
    def __init__(self, led_pin_name):
        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)
        self.duty = 0
        self.increment = 1

    def update(self):
        if self.duty > 2 ** 16 - 1:
            self.increment = -1
        elif self.duty < 1:
            self.increment = 1
        self.duty += self.increment
        self.led_pwm.duty_u16(self.duty)


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
    def __init__(self, pot_pin_name, led_pin_name):
        print("POTMeter loaded.")
        self.pot_pin = Pin(pot_pin_name, Pin.IN)
        self.adc = ADC(pot_pin_name)
        self.value = self.adc.read_u16()

        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)

        print("POTMeter initialized")

    def update(self):
        self.value = self.adc.read_u16()

        if self.value > 32000:
            self.led_pin.high()
        else:
            self.led_pin.low()

        # self.led_pwm.duty_u16(self.value)
        print(self.value)
        sleep_ms(250)


sleep_ms(5000)  # pause before startup

modules = [
    # LEDFader("GP14"),  # led pin GP14
    LEDBlink(15),  # led pin GP15
    # POTMeter(28, 9)  # pot pin number GP28 or ADC2, led pin GP15
]

while True:
    for module in modules:
        module.update()
