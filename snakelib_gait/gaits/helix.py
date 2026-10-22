from .compound_serpenoid import compound_serpenoid


def helix(phase, n_modules, amplitude, spatial_frequency, time_frequency):
    """Calculate joint angles for manual helical rolling.

    This gait forms a helix by using a particular temporal offset
    between the waves on the lateral and dorsal axes. Direct control is given
    of the amplitude and spatial frequency of these waves.
    """
    return compound_serpenoid(
        phase, n_modules,
        offsets=[0, 0],
        amplitudes=[amplitude] * 2,
        spatial_frequencies=[spatial_frequency] * 2,
        time_frequencies=[time_frequency] * 2,
        phase_shift=0.25
    )
