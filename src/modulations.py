import numpy as np


def bpsk(_system):
    _number_of_constellaition_points = 2
    _possible_symbols = np.arange(0, _number_of_constellaition_points)
    _constellation = _system.properties.amplitude * np.cos(
        _possible_symbols / _number_of_constellaition_points * 2 * np.pi
    )
    _random_syms = np.random.randint(
        low=0,
        high=_number_of_constellaition_points,
        size=int(_system.properties.get_number_of_Symbols()),
    )
    _modulated = _constellation[_random_syms]
    return _modulated, _constellation


def qpsk(_system):
    _number_of_constellaition_points = 4
    # Generate random symbols (two bits per symbol)
    _random_symbols = np.random.randint(
        0, _number_of_constellaition_points, int(_system.number_of_Symbols / 2)
    )
    # Normalize amplitude for QPSK
    _amplitude = _system.properties.amplitude / np.sqrt(2)

    # QPSK mapping (00, 01, 11, 10 to unique phase shifts)
    _constellations = _amplitude * (
        np.cos(np.pi / 4 * (1 + 2 * _random_symbols))
        + 1j * np.sin(np.pi / 4 * (1 + 2 * _random_symbols))
    )

    return _constellations, _random_symbols
