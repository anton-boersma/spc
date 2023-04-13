from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


class Module:
    def update(self):
        raise NotImplementedError("update method not implemented")

    def get_output(self):
        pass

    def get_input(self):
        pass


class POTMeter(Module):
    def __init__(self, pot_pin_name):
        sleep_ms(2000)
        print("POTMeter loading.")
        self.pot_pin = Pin(pot_pin_name, Pin.IN)
        self.adc = ADC(pot_pin_name)
        self.value = self.adc.read_u16()

        print("POTMeter loaded.")

        self.current_time = ticks_us()
        self.previous_time = self.current_time

        self.output = None

    def update(self):
        self.current_time = ticks_us()
        if ticks_diff(self.current_time, self.previous_time) >= 10000:  # time in micro seconds, us
            self.value = self.adc.read_u16()
            self.previous_time = self.current_time
            POTMeter.get_output(self)

    # def get_output(self):
    #     self.output = self.value
    #     print("The output is:", self.output)
    #     global POTMeter_output
    #     POTMeter_output = self.output
    #     # return self.output

    def get_output(self):
        global POTMeter_output
        POTMeter_output = self.value


class LEDFader(Module):
    def __init__(self, led_pin_name):
        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)
        self.duty = 0

    def update(self):
        self.duty = LEDFader.get_input(self)
        self.led_pwm.duty_u16(self.duty)
        # print("The PWM value is:", self.duty)

    def get_input(self):
        global POTMeter_output
        return POTMeter_output


modules = [
    POTMeter(28),  # pot pin number GP28 or ADC2
    LEDFader(10),
    LEDFader(11),
    LEDFader(12)
]

POTMeter_output = 0
sleep_ms(2000)  # pause before startup
print("Modules loaded")

while True:
    for module in modules:
        module.update()
        module.get_output()

    # print(POTMeter_output)
