from modules import DashboardModule, FrequencyModule, SteeringModule
from components import POTMeter
from libraries import Servo


def main():

    # sleep_ms(5000)  # pause before startup

    display_mode = 1

    frequency = FrequencyModule()
    gas_pedal = POTMeter("Gas pedaal", 28)
    brake_pedal = POTMeter("Rem pedaal", 27)
    steering_wheel = POTMeter("Stuurwiel", 26)
    dashboard = DashboardModule(frequency, gas_pedal, brake_pedal, steering_wheel, display_mode)
    led_blinker = SteeringModule(15, steering_wheel)

    modules = [
        frequency,
        gas_pedal,
        brake_pedal,
        steering_wheel,
        led_blinker,
        dashboard
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()
