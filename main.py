from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


#  different modules, each in its own class
class Module:
    def update(self):
        raise NotImplementedError("update method not implemented")

    def get_message(self, message):
        pass

    def push_message(self):
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

    def push_message(self):
        self.output = self.value  # [self.pot_pin, self.value]
        print(self.output)
        return self.output

    def globalvariable(self):
        globalvar += 1
        return globalvar


class CommunicationTest(Module):
    def __init__(self, message):
        pass
        # self.message = message

    def update(self):
        pass

    def get_message(self, incomingmessage):
        print("The message is:")
        print(incomingmessage)


#  global variables
message = None
globalvar = 0

#  modules to run
modules = [
    POTMeter(28)  # pot pin number GP28 or ADC2
    # CommunicationTest(message)
    # Drivetrain()  # gets
]
sleep_ms(2000)  # pause voor startup

#  main loop
while True:
    for module in modules:
        module.update()
        # message = module.push_message()
        # module.get_message(message)
        module.globalvariable()

    sleep_ms(1000)
    # print(globalvar)
    print(message**2)


