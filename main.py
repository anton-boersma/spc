from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


class Module:
    # update method is run repeatedly
    def update(self):
        raise NotImplementedError("update method not implemented")


class POTMeter(Module):

    # declare class variables
    value: int

    def __init__(self, name: str, pot_pin_name: int):
        print("POTMeter loading.")

        self._name = name

        # alle 3 typen variabele hier,
        # geen self -> deze method alleen
        # wel self. en _ is alleen deze class, ook andere methods
        # wel self. zonder _ is variabele die ook naar andere classes gaat
        pot_pin = Pin(pot_pin_name, Pin.IN)  # set pot_pin modus to input
        self._adc = ADC(pot_pin)  # create ADC instance for this pin
        self.value = self._adc.read_u16()  # read voltage of pin using ADC

        print("POTMeter loaded.")

        # time keeping
        self._previous_time = ticks_us()  # store current time
        # self._var_name _ indicates var is only used here, must be self. variable

    def __str__(self):
        return f"POTMeter(name = {self._name}, value = {self.value})"

    def update(self):
        current_time = ticks_us()  # stack variable, current time is only a thing when update is called

        # only do the following code after time has elapsed
        if ticks_diff(current_time, self._previous_time) >= 10000:  # time in micro seconds, us
            self.value = self._adc.read_u16()
            self._previous_time = current_time


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


class VehicleTest(Module):
    def __init__(self, left_pin_name: int, middle_pin_name: int, right_pin_name: int, pot_meter: POTMeter):  # set type of pot_meter to POTMeter
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
        right_duty = max(0, min(3 * (value - 43690), 2**16 - pwm_correction))\

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

    sleep_ms(3000)  # pause before startup

    steering_wheel = POTMeter('steering wheel', 28)  # get POTmeter for steering module
    accelerator_pedal = POTMeter('accelerator pedal', 27)  # get POTMeter for accelerator pedal
    brake_pedal = POTMeter('brake pedal', 26)  # get POTMeter for brake pedal

    print(steering_wheel)

    # list of modules in the vehicle
    modules = [
        steering_wheel,  # pot pin number GP28 or ADC2
        accelerator_pedal,  # pot pin number GP27 or ADC1
        brake_pedal,  # pot pin number GP26 or ADC0

        SteeringModule(18, steering_wheel),
        AcceleratorModule(17, accelerator_pedal),
        BrakingModule(16, brake_pedal)
        # VehicleTest(10, 11, 12, steering_wheel)  # LED pin numbers GP10 GP11 GP12, Pico pins 14 15 16
    ]

    print("Modules loaded, program is running.")

    while True:
        for module in modules:
            module.update()  # update each module


# main()

if __name__ == '__main__':
    main()
