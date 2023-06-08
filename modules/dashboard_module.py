from .module import Module
from components.display import Display
from modules.frequency_module import FrequencyModule


class DashboardModule(Module):

    def __init__(self, frequency: FrequencyModule, gas_pedal, brake_pedal, steering_wheel, display_mode: int):
        self.display = Display(line_height=10)
        self.frequency = frequency
        self.gas_pedal = gas_pedal
        self.brake_pedal = brake_pedal
        self.steering_wheel = steering_wheel
        self.display_mode = display_mode

    def update(self):
        self.display.clear()
        if self.display_mode == 1:
            self.display.text(f"Frequency:{self.frequency.frequency} Hz\nGas pedaal:{self.gas_pedal.value}\nRem pedaal:{self.brake_pedal.value}\nStuurwiel: {self.steering_wheel.value}\n\n")
        self.display.show()
