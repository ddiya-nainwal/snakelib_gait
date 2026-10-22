import numpy as np

from .shape import Shape


def serpenoid(
        phase, n, offset, amplitude,
        spatial_frequency, time_frequency, phase_shift):
    """Generate a single-backbone sinusoidal curve.

    Args:
        phase:
            Abstract time value that lets us set where we are in the gait cycle
        n:
            Abstract spatial position along the backbone. For a typical gait it
            might be [0, 2, 4, ..] or [1, 3, 5, ...]. This and the parameters
            that follow can be a single float or an array of shape (N,).
        offset:
            The offset about which the sine wave is centered.
        amplitude:
            Amplitude of the sin wave.
        spatial_frequency:
            Inverse of wavelength or 1 / (the number of modules in one cycle).
            By using frequency instead of wavelenth, waves which are purely
            temporal in nature can be represented with a frequency of zero
            rather than an infinit wavelength.
        time_frequency:
            How many cycles this wave goes through with respect to phase.
        phase_shift:
            Offset between the two backbone curves in phase

    Returns:
        Output joint angles
    """
    return offset + amplitude * np.sin(
        np.pi * 2 * (spatial_frequency * n - time_frequency * phase + phase_shift))


def compound_serpenoid(
        phase, n_modules, offsets, amplitudes,
        spatial_frequencies, time_frequencies,
        phase_shift):
    """Generate a dual-backbone sinusoidal curve.

    Args:
        phase:
            Abstract time value that lets us set where we are in the gait cycle.
        n_modules:
            Integer representing number of modules or a list of positions along
            the backbone. For a typical gait it might be [0, 1, 2, 3, ..].
        offsets:
            The offsets about which each sine wave is centered. This can be a an
            array of shape (2,) or (n_modules, 2).
        amplitudes:
            Amplitudes of each sin wave. This can be a an array of shape (2,)
            or (n_modules, 2).
        spatial_frequencies:
            Inverse of wavelengths or 1 / (the number of modules in one cycle).
            By using frequency instead of wavelenth, waves which are purely
            temporal in nature can be represented with a frequency of zero
            rather than an infinite wavelength. This is an array of shape (2,).
        time_frequencies:
            How many cycles each wave goes through with respect to phase. This
            is an array of shape (2,).
        phase_shift:
            Phase offset added to the second backbone curve.

    Returns:
        Shape object representing the joint angles
    """
    if isinstance(n_modules, int):
        n = np.arange(n_modules, dtype=float)
    else:
        n = np.asarray(n_modules)
    backbones = []
    for i in range(2):
        backbones.append(serpenoid(
            phase,
            n,
            offsets[i],
            amplitudes[i],
            spatial_frequencies[i],
            time_frequencies[i],
            phase_shift if i else 0
        ))
    return Shape.from_angles(backbones[0], backbones[1])
