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
        # print("The POT value is:", self.value)


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


class VehicleTest(Module):
    def __init__(self, left_pin_name, middle_pin_name, right_pin_name):
        self.left_pin = Pin(left_pin_name, Pin.OUT)
        self.middle_pin = Pin(middle_pin_name, Pin.OUT)
        self.right_pin = Pin(right_pin_name, Pin.IN)

        self.left_pwm = PWM(self.left_pin)
        self.middle_pwm = PWM(self.middle_pin)
        self.right_pwm = PWM(self.middle_pin)

        self.left_duty = 0
        self.middle_duty = 0
        self.right_duty = 0

        self.input = 0

        self.current_time = ticks_us()
        self.previous_time = self.current_time

    def update(self):
        self.input = VehicleTest.get_input(self)

        if self.input < 21845:
            self.left_duty = self.input * 3
            self.middle_duty = 0
            self.right_duty = 0
        elif 21845 <= self.input < 43690:
            self.left_duty = 2**16 - 2
            self.middle_duty = (self.input - 21845) * 3
            self.right_duty = 0
        elif 43690 <= self.input < 65535:
            self.left_duty = 2**16 - 2
            self.middle_duty = 2**16 - 2
            self.right_duty = (self.input - 43690) * 3
        else:
            self.left_duty = 2**16 - 2
            self.middle_duty = 2**16 - 2
            self.right_duty = 2**16 - 2

        self.left_pwm.duty_u16(self.left_duty)
        self.middle_pwm.duty_u16(self.middle_duty)
        self.right_pwm.duty_u16(self.right_duty)

        self.current_time = ticks_us()
        if ticks_diff(self.current_time, self.previous_time) >= 2000000:  # time in micro seconds, us
            print('Green value:', self.left_duty)
            print('Yellow value:', self.middle_duty)
            print('Red value:', self.right_duty)
            print()
            print('POTMeter value', VehicleTest.get_input(self))
            print()

            self.previous_time = self.current_time

    def get_input(self):
        global POTMeter_output
        return POTMeter_output


modules = [
    POTMeter(28),  # pot pin number GP28 or ADC2
    VehicleTest(10, 11, 12)  # LED pin numbers GP10 GP11 GP12, Pico pins 14 15 16
]

POTMeter_output = 0
sleep_ms(2000)  # pause before startup
print("Modules loaded, program is running.")

while True:
    for module in modules:
        module.update()
        # module.get_output()

    # print(POTMeter_output)
