from machine import Pin, PWM, ADC
from utime import sleep_ms


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

    def update(self):
        if self.enabled:
            self.led_pin.low()
            self.enabled = False
        else:
            self.led_pin.high()
            self.enabled = True
        sleep_ms(500)


class POTMeter(Module):
    def __init__(self, pot_pin_name, led_pin_name):
        sleep_ms(2000)
        print("POTMeter loaded.")
        self.pot_pin = Pin(pot_pin_name, Pin.IN)
        self.adc = ADC(pot_pin_name)
        self.value = self.adc.read_u16()

        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)

    def update(self):
        self.value = self.adc.read_u16()
        self.led_pwm.duty_u16(self.value)
        print(self.value)
        sleep_ms(250)


modules = [
    # LEDFader("GP14"),  # led pin GP14
    # LEDFader("GP15"),  # led pin GP15
    POTMeter(28, 15)  # pot pin number GP28 or ADC2, led pin GP15
]

while True:
    for module in modules:
        module.update()
