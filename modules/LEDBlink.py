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