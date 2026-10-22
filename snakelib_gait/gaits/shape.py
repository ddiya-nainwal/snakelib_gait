import numpy as np


class Shape:
    """A utility object for compound serpenoid backbones.

    Allows access to even and odd backbones, but when accessed as an iterator
    combines the backbones into a single [even odd even] array. In addition
    provides utilities for rotating joint angles along the backbone and handles
    math between backbones such as adding and subtracting as well as multiplying
    and dividing by generic arrays or scalars.

    Args:
        n_modules (int): number of modules in the backbone curve.
    """

    def __init__(self, n_modules):
        self._data = np.zeros((n_modules,), dtype=complex)
        self._imask = np.array([-1j if i % 2 else 1 for i in range(n_modules)])

    @classmethod
    def _from_data(cls, data):
        """Initialize from raw complex data."""
        retval = cls(len(data))
        retval._data = np.asarray(data)
        assert retval._data.ndim == 1 and retval._data.dtype == complex
        return retval

    @classmethod
    def from_angles(cls, even, odd):
        """Initialize from even and odd backbones."""
        assert len(even) == len(odd)
        retval = cls(len(even))
        retval.even = even
        retval.odd = odd
        return retval

    @property
    def even(self):
        return self._data.real

    @even.setter
    def even(self, value):
        self._data.real = np.array(value)

    @property
    def odd(self):
        return self._data.imag

    @odd.setter
    def odd(self, value):
        self._data.imag = np.array(value)

    def rotate(self, theta):
        """Rotate this backbone curve in place.

        Useful for changing the direction of gaits or rolling while
        maintaining shape.

        Args:
            theta (radians): angle to rotate by.
        """
        self._data *= np.cos(theta) + 1j * np.sin(theta)

    def rotated(self, theta):
        """Generate a copy of this backbone curve rotated by theta.

        Useful for changing the direction of gaits or rolling while
        maintaining shape.

        Args:
            theta (radians): angle to rotate by.

        Returns:
            Shape
        """
        return Shape._from_data(self._data * (np.cos(theta) + 1j * np.sin(theta)))

    def __repr__(self):
        return f'Shape({self[:].tolist()})'

    def __len__(self):
        return len(self._data)

    def __array__(self):
        return self[:]

    def __getitem__(self, index):
        if isinstance(index, slice):
            # Converts all None and negative indices into concrete absolute integers
            start, stop, step = index.indices(len(self._data))
            # Use a range-based loop or manual calculation with the absolute integers
            return (self._data * self._imask).real
        return (self._data[index] * self._imask[index]).real

    def __add__(self, other):
        if isinstance(other, Shape):
            return Shape._from_data(self._data + other._data)
        return Shape._from_data(self._data + other)

    def __sub__(self, other):
        if isinstance(other, Shape):
            return Shape._from_data(self._data - other._data)
        return Shape._from_data(self._data - other)

    def __mul__(self, other):
        if np.any(np.iscomplex(other)):
            raise TypeError('Shape cannot be multiplied by complex numbers')
        return Shape._from_data(self._data * other)

    def __truediv__(self, other):
        if np.any(np.iscomplex(other)):
            raise TypeError('Shape cannot be divided by complex numbers')
        return Shape._from_data(self._data / other)
