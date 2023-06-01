from machine import Pin, PWM, I2C
from utime import sleep_ms
from time import ticks_us, ticks_diff
from libraries import test
from modules import Module, POTMeter


class SteeringModule(Module):
    def __init__(self, led_pin_name: int, pot_meter: POTMeter):
        # declare pin variables
        led_pin = Pin(led_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # declare PWM modus
        self._pin_pwm = PWM(led_pin)

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value  # get POTMeter value

        led_duty = value

        self._pin_pwm.duty_u16(led_duty)

        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print('LED value:', led_duty)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time


class AcceleratorModule(Module):
    def __init__(self, led_pin_name: int, pot_meter: POTMeter):
        # declare pin variables
        led_pin = Pin(led_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # declare PWM modus
        self._pin_pwm = PWM(led_pin)

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value  # get POTMeter value

        led_duty = value

        self._pin_pwm.duty_u16(led_duty)

        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print('LED value:', led_duty)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time


class BrakingModule(Module):
    def __init__(self, led_pin_name: int, pot_meter: POTMeter):
        # declare pin variables
        led_pin = Pin(led_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # declare PWM modus
        self._pin_pwm = PWM(led_pin)

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value  # get POTMeter value

        led_duty = value

        self._pin_pwm.duty_u16(led_duty)

        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print('LED value:', led_duty)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time


class Dashboard(Module):
    def __init__(self):
        pass

    def update(self):
        pass


class VehicleTest(Module):
    def __init__(self, left_pin_name: int, middle_pin_name: int, right_pin_name: int, pot_meter: POTMeter):  # set type of pot_meter to POTMeter, linked to class name
        # declare pin variables
        left_pin = Pin(left_pin_name, Pin.OUT)
        middle_pin = Pin(middle_pin_name, Pin.OUT)
        right_pin = Pin(right_pin_name, Pin.OUT)
        self._pot_meter = pot_meter

        # declare PWM modus
        self._left_pwm = PWM(left_pin)
        self._middle_pwm = PWM(middle_pin)
        self._right_pwm = PWM(right_pin)

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        value = self._pot_meter.value  # get POTMeter value
        pwm_correction = 2  # 1 for LED's going sequentially, 2 for LEDs staying lit

        left_duty = max(0, min(3 * value, 2**16 - pwm_correction))
        middle_duty = max(0, min(3 * (value - 21845), 2**16 - pwm_correction))
        right_duty = max(0, min(3 * (value - 43690), 2**16 - pwm_correction))

        # write PWM signal to the LEDs
        self._left_pwm.duty_u16(left_duty)
        self._middle_pwm.duty_u16(middle_duty)
        self._right_pwm.duty_u16(right_duty)

        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print('Green value:', left_duty)
            print('Yellow value:', middle_duty)
            print('Red value:', right_duty)
            print(self._pot_meter.__str__())
            print()

            self._previous_time = current_time


def main():

    sleep_ms(4000)  # pause before startup

    steering_wheel = POTMeter('steering wheel', 28)  # get POTmeter for steering module
    accelerator_pedal = POTMeter('accelerator pedal', 27)  # get POTMeter for accelerator pedal
    brake_pedal = POTMeter('brake pedal', 26)  # get POTMeter for brake pedal

    # steering_module = SteeringModule(18, steering_wheel)
    # accelerator_module = AcceleratorModule(17, accelerator_pedal)
    # braking_module = BrakingModule(16, brake_pedal)

    print(steering_wheel)

    # i2c = I2C(0, sda=Pin(0, Pin.OUT), scl=Pin(1, Pin.OUT), freq=10000)  # Raspberry Pi Pico
    #
    # display = ssd1327.SSD1327_I2C(128, 128, i2c, addr=0b0111101)
    #
    # display.text('Hello World', 0, 0, 255)
    # display.show()
    #
    # display.fill(0)
    # for y in range(0, 12):
    #     display.text('Hello World', 0, y * 8, 15 - y)
    # display.show()

    # list of modules in the vehicle
    modules = [
        steering_wheel,  # pot pin number GP28 or ADC2
        accelerator_pedal,  # pot pin number GP27 or ADC1
        brake_pedal,  # pot pin number GP26 or ADC0

        # steering_module,
        # accelerator_module,
        # braking_module,

        SteeringModule(18, steering_wheel),
        AcceleratorModule(17, accelerator_pedal),
        BrakingModule(16, brake_pedal),

        # Dashboard(steering_module, accelerator_module, braking_module)
        VehicleTest(10, 11, 12, steering_wheel)  # LED pin numbers GP10 GP11 GP12, Pico pins 14 15 16
    ]

    print("Modules loaded, program is running.")

    while True:
        for module in modules:
            module.update()  # update each module


if __name__ == '__main__':
    main()
