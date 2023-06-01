from .module import Module
from time import ticks_us, ticks_diff


class FrequencyModule(Module):

    def __init__(self):
        self.counter = 0
        self.previous = ticks_us()
        self.frequency = 0

    def update(self):
        self.counter += 1
        current = ticks_us()
        if ticks_diff(current, self.previous) > 1000000:
            self.previous = current
            self.frequency = self.counter
            self.counter = 0
