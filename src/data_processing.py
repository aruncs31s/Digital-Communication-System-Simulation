"""
Author : Arun CS 

Date : 2024-11-03

Notes : I know it looks complicated but it is good to keep this way to prevent modularity , also objects are passed around instead of variables it is best to keep this way
"""

import numpy as np


class Properties:
    def __init__(self, frequency, number_of_Symbols, amplitude):
        self.frequency = frequency
        self.number_of_Symbols = number_of_Symbols
        self.amplitude = amplitude

    def get_frequency(self):
        return self.frequency

    def get_amplitude(self):
        return 1

    def get_time_period(self):
        return 1 / self.frequency

    def get_number_of_Symbols(self):
        return self.number_of_Symbols


class Communication_System:
    def __init__(self, properties, modulation_scheme):
        self.properties = properties
        self.frequency = properties.frequency
        self.number_of_Symbols = properties.number_of_Symbols
        self.modulation_scheme = modulation_scheme
        if self.modulation_scheme == "bpsk":
            self._number_of_constellaition_points = 2
        if self.modulation_scheme == "qpsk":
            self._number_of_constellaition_points = 4

    def get_modulation_scheme(self):
        return self.modulation_scheme

    def get_ber(self):
        if self.modulation_scheme == "bpsk":
            return 0.5 * (1 - 1 / np.sqrt(self._number_of_constellaition_points))

    def get_x_axis(self):
        x_axis = np.linspace(0, 2 * np.pi, self.number_of_Symbols)
        return x_axis
