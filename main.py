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

    # def get_output(self):
    #     global POTMeter_output  # get global variable POTMeter_output
    #     POTMeter_output = self.value  # give the global variable to class variable


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

        # declare duty cycle values
        self._left_duty = 0
        self._middle_duty = 0
        self._right_duty = 0

        # declare LED modus
        self._pwm_correction = 2  # 1 for LED's going sequentially, 2 for LEDs staying lit

        # time keeping
        self._previous_time = ticks_us()

    def update(self):
        # self.input = VehicleTest.get_input(self)  # get POTMeter value
        value = self._pot_meter.value

        if value < 21845:  # operate left LED
            self._left_duty = value * 3
            self._middle_duty = 0
            self._right_duty = 0
        elif 21845 <= value < 43690:  # operate middle LED
            self._left_duty = 2 ** 16 - self._pwm_correction
            self._middle_duty = (value - 21845) * 3
            self._right_duty = 0
        elif 43690 <= value < 65535:  # operate right LED
            self._left_duty = 2 ** 16 - self._pwm_correction
            self._middle_duty = 2 ** 16 - self._pwm_correction
            self._right_duty = (value - 43690) * 3
        else:  # all LED's at maximum
            self._left_duty = 2 ** 16 - self._pwm_correction
            self._middle_duty = 2 ** 16 - self._pwm_correction
            self._right_duty = 2 ** 16 - self._pwm_correction

        # write PWM signal to the LEDs
        self._left_pwm.duty_u16(self._left_duty)
        self._middle_pwm.duty_u16(self._middle_duty)
        self._right_pwm.duty_u16(self._right_duty)

        # print out LED PWM values every 2 seconds
        current_time = ticks_us()
        if ticks_diff(current_time, self._previous_time) >= 2000000:  # time in micro seconds, us
            print('Green value:', self._left_duty)
            print('Yellow value:', self._middle_duty)
            print('Red value:', self._right_duty)
            print()

            self._previous_time = current_time

    # get POTMeter value from global memory
    # def get_input(self):
    #     global POTMeter_output
    #     return POTMeter_output


def main():

    sleep_ms(3000)  # pause before startup

    stuurkolom = POTMeter('stuurkolom', 28)

    print(stuurkolom)

    # stuurkolom = POTMeter(A)
    # aandrijving = POTMeter(B)

    modules = [
        stuurkolom,  # pot pin number GP28 or ADC2
        # aandrijving,
        # stuurkolom,
        VehicleTest(10, 11, 12, stuurkolom)  # LED pin numbers GP10 GP11 GP12, Pico pins 14 15 16
    ]

    # POTMeter_output = 0  # global variable to read POTMeter value
    print("Modules loaded, program is running.")

    while True:
        for module in modules:
            module.update()


main()

# if __name__ == '__main__':
#     main()
