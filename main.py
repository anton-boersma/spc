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


class Display(Module):
    def __init__(self):
        from machine import Pin, I2C
        from lib.ssd1306 import SSD1306_I2C
        # Opzetten I2C protocol op pinnen
        oled_i2c = I2C(0, sda=Pin(8), scl=Pin(9))
        # Check of via i2c een chip te vinden is
        print(oled_i2c.scan())
        # I2C configureren voor ssd1306 display
        oled = SSD1306_I2C(width=128, height=32, i2c=oled_i2c, addr=0x3D)
        # Nu kunnen we gebruik maken van de functies die beschikbaar zijn
        # voor het SSD1306 object, inclusief Framebuffer
        oled.fill(0)
        oled.text('Hello', 0, 0, 0xffff)
        oled.text('MicroPython!', 0, 10, 0xffff)
        oled.hline(0, 20, 95, 0xffff)
        oled.show()

    def update(self):
        pass


def main():

    sleep_ms(5000)  # pause before startup

    print("starting")

    pot_meter = POTMeter('test meter', 28)
    pot_meter.__str__()

    modules = [
        pot_meter,
        LEDFader(15, pot_meter)
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()
