from math import pi

from .compound_serpenoid import compound_serpenoid


def helix_auto(phase, n_modules, tightness, pole_side, time_frequency):
    """Calculate joint angles for automatic helical rolling.

    This is a helical gait that intelligently combines pitch and diameter.
    This helix gait is used for climbing the outside of a pole, and
    the single "tightness" parameter therefore changes the pitch and diameter
    of the helix in a piecewise-linear fashion; as the helix tightens, the
    rate of change of each changes at several distinct set points.
    """
    if tightness <= 0.3:
        spatial_frequency = 0
    elif tightness <= 0.4:
        spatial_frequency = (tightness - 0.3) / 10.0
    elif tightness <= 0.6:
        spatial_frequency = 0.01 + (tightness - 0.4) / 20.0
    else:
        spatial_frequency = 0.2
    if pole_side:
        spatial_frequency *= -1

    return compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=[pi / 2 * tightness] * 2,
        spatial_frequencies=[spatial_frequency] * 2,
        time_frequencies=[time_frequency] * 2,
        phase_shift=0.25
    )
