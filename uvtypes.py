"""Types for UV projected geometry operations. Strictly in 2D.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray
import utility
import mathtypes
import meshtypes


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


class UVLine(mathtypes.Line):
    """Line primitive in UV space"""
    _dimension = 2
    _argtypes_point = [ndarray, UVPoint]
    _argtypes_vector = [ndarray]


class UVTriangle:
    """Triangle primitive in UV space"""
    _dimension = 2
    _argtypes_point = [ndarray, UVPoint]
    _argtypes_edge = [UVLine]
    _argtypes_vector = [ndarray]

    def __init__(self, point_0: UVPoint, point_1: UVPoint, point_2: UVPoint):
        utility.argcheck_dim(self._dimension, point_0, point_1, point_2)
        utility.argcheck_type(self._argtypes_point, point_0)
        utility.argcheck_type(self._argtypes_point, point_1)
        utility.argcheck_type(self._argtypes_point, point_2)

        self.__point_a = utility.vec(point_0)
        self.__point_b = utility.vec(point_1)
        self.__point_c = utility.vec(point_2)
        self.__edge_a = UVLine(self.__point_a, self.__point_b)
        self.__edge_b = UVLine(self.__point_b, self.__point_c)
        self.__edge_c = UVLine(self.__point_c, self.__point_a)

    def __recalc_edges(self):
        self.__edge_a = UVLine(self.__point_a, self.__point_b)
        self.__edge_b = UVLine(self.__point_b, self.__point_c)
        self.__edge_c = UVLine(self.__point_c, self.__point_a)

    @property
    def point_a(self):
        return UVPoint(self.__point_a)

    @point_a.setter
    def point_a(self, new_point):
        utility.argcheck_dim(self._dimension, new_point)
        utility.argcheck_type(self._argtypes_point, new_point)
        self.__point_a = vec(new_point)
        self.__recalc_edges()

    @property
    def point_b(self):
        return UVPoint(self.__point_b)

    @point_b.setter
    def point_b(self, new_point):
        utility.argcheck_dim(self._dimension, new_point)
        utility.argcheck_type(self._argtypes_point, new_point)
        self.__point_b = vec(new_point)
        self.__recalc_edges()

    @property
    def point_c(self):
        return UVPoint(self.__point_c)

    @point_c.setter
    def point_c(self, new_point):
        utility.argcheck_dim(self._dimension, new_point)
        utility.argcheck_type(self._argtypes_point, new_point)
        self.__point_c = vec(new_point)
        self.__recalc_edges()

    @property
    def edge_a(self):
        return self.__edge_a

    @property
    def edge_b(self):
        return self.__edge_b

    @property
    def edge_c(self):
        return self.__edge_c