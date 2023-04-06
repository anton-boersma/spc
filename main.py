from machine import Pin, PWM, ADC
from utime import sleep_ms
from time import ticks_us, ticks_diff


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
        if self.duty > 2 ** 16 - 1:
            self.increment = -1
        elif self.duty < 1:
            self.increment = 1
        self.duty += self.increment
        self.led_pwm.duty_u16(self.duty)


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


class POTMeter(Module):
    def __init__(self, pot_pin_name, led_pin_name):
        sleep_ms(2000)
        print("POTMeter loading.")
        self.pot_pin = Pin(pot_pin_name, Pin.IN)
        self.adc = ADC(pot_pin_name)
        self.value = self.adc.read_u16()

        self.led_pin = Pin(led_pin_name, Pin.OUT)
        self.led_pwm = PWM(self.led_pin)

        print("POTMeter loaded.")

        self.current_time = ticks_us()
        self.previous_time = self.current_time

    def update(self):
        self.current_time = ticks_us()
        if ticks_diff(self.current_time, self.previous_time) >= 10000:  # time in micro seconds
            self.value = self.adc.read_u16()
            self.led_pwm.duty_u16(self.value)
            print(self.value)
            self.previous_time = self.current_time

#
# class Speedometer(Module):
#     def __init__(self, constant):
#         self.previous = None
#         self.constant = constant
#
#     def meting(self):
#         pass  # beter om in class functies te maken
#
#     def update(self):
#         if self.previous is None:
#             self.previous = self.meting()
#         else:
#             current = meting() # tijd meting of distance meting
#             diff = current - self.previous
#             spood = distance_constant / diff
#             self.previous = current
#

#
# class HallEffectSensor(Module):
#     def __init__(self, hall_pin_name, led_pin_name):
#         sleep_ms(2000)
#         print("Hall effect loading.")
#         self.hall_pin = Pin(hall_pin_name, Pin.IN)
#         self.led_pin = Pin(led_pin_name, Pin.OUT)
#
#         print("Hall effect loaded.")
#
#         self.current_time = ticks_us()
#         self.previous_time = self.current_time
#
#     def update(self):
#         pass
#         # try:
#         #     if self.hall_pin.value() == 0:
#         #         self.led_pin.value(0)
#         #         print("HIGH")
#         #     elif self.hall_pin.value() == 1:
#         #         self.led_pin.value(1)
#         #         print("LOW")
#         #     print(self.hall_pin.value())
#



""""
Opties voor synchroon lopende modules

timer runt update method, per method - meerdere timers tegelijk
keep track of time en stuur dat naar de update methods

voor snelheid meten
fancy troep:
    schedulers voor update puls hierarchie
multithread:
    eentje voor continuous zoals sturen, remmen, gas
    ander voor tweederangs taken en periodieke spul

Sensor input typen (Wessel)
- potmeter
- laser met slotted wiel (let op meetfrequentie) nyquist frequentie, check topsnelheid, radius, number of slots
- hall effect sensor (potmeter zonder slijtage, maar duur)
- accelerometer (kan voor snelheid en G-kracht)
- compas (dashboard)
- absolute rotary encoder

Rotatie sensoren: (Ruben)
Optisch sensor met slotted disk
Gyroscoop
Potmeter
Strainmeters

"""

modules = [
    # LEDFader("GP14"),  # led pin GP14
    # LEDFader(15)  # led pin GP15
    POTMeter(28, 15)  # pot pin number GP28 or ADC2, led pin GP15
    # Speedometer(constantValue)  # constant value van wiel of
    # HallEffectSensor(26,15)
]

sleep_ms(2000)  # pause voor startup

while True:
    for module in modules:
        module.update()


