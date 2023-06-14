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
    steering_module = SteeringModule(15, 14, 13, 12, steering_wheel)
    dashboard = DashboardModule(frequency, gas_pedal, brake_pedal, steering_wheel, steering_module, display_mode)

    modules = [
        frequency,
        gas_pedal,
        brake_pedal,
        steering_wheel,
        steering_module,
        dashboard
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()
