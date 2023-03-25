from machine import Pin
from utime import sleep_ms

led_pin = Pin("GP15", Pin.OUT)
enabled = False

while True:
    if enabled:
        led_pin.low()
        enabled = False
    else:
        led_pin.high()
        enabled = True
    sleep_ms(500)
    # print(enabled)

