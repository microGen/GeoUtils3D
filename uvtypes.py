"""Types for UV projected geometry operations. Strictly in 2D.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray
import utility
from mathtypes import Line as __Line


class UVPoint:
    """Point primitive in UV space"""
    _dimension = 2

    def __init__(self, *coords):
        """Creates a point in UV space.
        ARGS:
            coords: ndarray of 2 elements
                    or 2 float arguments
        """
        if len(coords) == 1 and type(coords[0]) == ndarray:
            if len(coords[0]) == 2:
                self.__coords = coords[0]
            else:
                raise ValueError("UVPoint only works in 2D UV space.")
        elif len(coords) == 2:
            self.__coords = array(coords)
        else:
            raise TypeError("UVPoint constructor takes either one ndarray or 2 floats as arguments.")

        self.__u = self.__coords[0]
        self.__v = self.__coords[1]

    @property
    def u(self) -> float:
        return self.__u

    @u.setter
    def u(self, u_coord):
        self.__coords[0] = u_coord
        self.__u = u_coord

    @property
    def v(self) -> float:
        return self.__v

    @v.setter
    def v(self, v_coord):
        self.__coords[1] = v_coord
        self.__v = v_coord

    @property
    def coords(self) -> ndarray:
        return self.__coords

    @coords.setter
    def coords(self, new_coords: ndarray):
        utility.argcheck_dim(self._dimension, new_coords)
        self.__coords = new_coords

class UVLine(__Line):
    """Line primitive in UV space"""
    _dimension = 2
    _argtypes_point = [ndarray, UVPoint]
    _argtypes_vector = [ndarray]
