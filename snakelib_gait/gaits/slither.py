import numpy as np

from .compound_serpenoid import compound_serpenoid


def slither(phase, n_modules, head_horizontal_amplitude,
            head_vertical_amplitude, tail_amplitude, time_frequency):
              
    n = n_modules if isinstance(n_modules, int) else len(n_modules)

    s = np.linspace(0.0, 1.0, n)

    #each module gets its own amplitude start + (end - start) x s
    horizontal = head_horizontal_amplitude + (tail_amplitude - head_horizontal_amplitude) * s
    vertical = head_vertical_amplitude + (tail_amplitude - head_vertical_amplitude) * s

    amplitudes = np.stack([horizontal, vertical]) * np.pi / 2

    return compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=amplitudes,
        spatial_frequencies=[1 / 8, 1 / 14],
        time_frequencies=[2 * time_frequency, time_frequency],
        phase_shift=0
    )
