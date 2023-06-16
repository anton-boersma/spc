from modules import DashboardModule, FrequencyModule, SteeringModule, DrivetrainModule, BrakingModule
from components import POTMeter


def main():
    display_mode = 1

    frequency = FrequencyModule()

    gas_pedal = POTMeter("Gas pedaal", 28)
    brake_pedal = POTMeter("Rem pedaal", 27)
    steering_wheel = POTMeter("Stuurwiel", 26)

    braking_module = BrakingModule(7, 6, 5, 4, brake_pedal)
    drivetrain_module = DrivetrainModule(11, 10, 9, 8, gas_pedal)
    steering_module = SteeringModule(15, 14, 13, 12, steering_wheel)
    dashboard = DashboardModule(frequency, gas_pedal, brake_pedal, steering_wheel, steering_module, drivetrain_module, braking_module, display_mode)

    modules = [
        frequency,
        gas_pedal,
        brake_pedal,
        steering_wheel,
        braking_module,
        drivetrain_module,
        steering_module,
        dashboard
    ]

    while True:
        for module in modules:
            module.update()


if __name__ == '__main__':
    main()
