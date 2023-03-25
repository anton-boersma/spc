from machine import Pin, PWM

from module import Module


class LEDFader(Module):
    def __init__(self, led_pin_name):
        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)
        self.duty = 0

    def update(self):
        self.duty += 1
        self.led_pwm.duty_u16(self.duty)
