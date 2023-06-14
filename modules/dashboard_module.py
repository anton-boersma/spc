from .module import Module
from components.display import Display
from modules.frequency_module import FrequencyModule
from modules.steering_module import SteeringModule
from modules.drivetrain_module import DrivetrainModule


class DashboardModule(Module):

    def __init__(self, frequency: FrequencyModule, gas_pedal, brake_pedal, steering_wheel, steering_module: SteeringModule, drivetrain_module: DrivetrainModule, display_mode: int):
        self.display = Display(line_height=10)
        self.frequency = frequency
        self.gas_pedal = gas_pedal
        self.brake_pedal = brake_pedal
        self.steering_wheel = steering_wheel
        self.steering_module = steering_module
        self.drivetrain_module = drivetrain_module
        self.display_mode = display_mode

    def update(self):
        self.display.clear()
        if self.display_mode == 1:
            self.display.text(f"Frequency:{self.frequency.frequency} Hz\nGas pedaal:{self.gas_pedal.value}\nRem pedaal:{self.brake_pedal.value}\nStuurwiel: {self.steering_wheel.value}\n\n")
        elif self.display_mode == 2:
            self.display.text(f"Frequency:{self.frequency.frequency} Hz\nLV hoek:{self.steering_module.lv_steering_angle() - 90}\nRV hoek:{self.steering_module.rv_steering_angle() - 90}\nLA hoek:{self.steering_module.la_steering_angle() - 90}\nRA hoek:{self.steering_module.ra_steering_angle() - 90}\n")
        elif self.display_mode == 3:
            self.display.text(f"Frequency:{self.frequency.frequency} Hz\nFront power:{round(self.drivetrain_module.front_power/180*100)}%\nRear power:{round(self.drivetrain_module.rear_power/180*100)}%")

        self.display.show()
