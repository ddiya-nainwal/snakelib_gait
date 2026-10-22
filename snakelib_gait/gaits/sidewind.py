from .compound_serpenoid import compound_serpenoid


def sidewind(phase, n_modules, amplitude_h, amplitude_v,
             spatial_frequency, time_frequency):
    """Calculate joint angles for sidewinding.

    Sidewinding is a fast, efficient gait that moves the robot sideways.
    It effectively wraps the robot around a "squished cylinder" and segments
    of this helical wrap produce "treads" which do not slide when contacting
    the ground, but instead the contact rolls along parallel lines, and the
    snake's motion is 45 degrees with respect to these lines. This is very
    similar to how biological snakes sidewind.

    Args:
        phase:
            Abstract time value that lets us set where we are in the gait cycle.
        n_modules:
            Integer representing number of modules or a list of positions along
            the backbone. For a typical gait it might be [0, 1, 2, 3, ..].
        amplitude_h:
            Amplitude in the horizontal direction.
        amplitude_v:
            Amplitude in the horizontal direction. In general this should be
            less than amplitude_h for stability
        spatial_frequency:
            Inverse of wavelength or 1 / (the number of modules in one cycle).
        time_frequency:
            How many cycles each wave goes through with respect to phase.
    """
    return compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=[amplitude_h, amplitude_v],
        spatial_frequencies=[spatial_frequency] * 2,
        time_frequencies=[time_frequency] * 2,
        phase_shift=3.0 / 8.0
    )
