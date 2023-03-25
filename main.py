from machine import Pin, PWM
from utime import sleep_ms

led_pin = Pin("GP15", Pin.OUT)
led_pwm = PWM(led_pin)
duty = 0
increment = 1

while True:
    led_pwm.duty_u16(duty)
    if duty > 2**16 - 1:
        increment = -1
    elif duty < 1:
        increment = 1

    duty += increment
# led_pin.low()