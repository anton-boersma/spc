from machine import Pin, PWM


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
        if self.duty > 2**16 - 1:
            self.increment = -1
        elif self.duty < 1:
            self.increment = 1
        self.duty += self.increment
        self.led_pwm.duty_u16(self.duty)


modules = [LEDFader("GP15")]

while True:
    for module in modules:
        module.update()
        # print("check")
