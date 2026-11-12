from .compound_serpenoid import compound_serpenoid


def roll(phase, n_modules, amplitude, time_frequency):
    """Calculate joint angles for rolling in an arc. This
    causes the snake to translate laterally across the ground.
    """
    return compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=[amplitude] * 2,
        spatial_frequencies=[0, 0],
        time_frequencies=[time_frequency] * 2,
        phase_shift=-0.25
    )
