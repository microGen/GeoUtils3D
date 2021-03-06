"""Types for 3D geometry operations.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray
from numpy import cross
import utility

class Point:
    """Point primitive in 3D space"""
    _dimension = 3
    _argtypes_multi = [ndarray]
    _argtypes_single = [int, float]

    def __init__(self, *coords):
        """Creates a point in 3D space.
        ARGS:
            coords: ndarray of 3 elements
                    or 3 float arguments
        """
        if len(coords) == 1 and utility.argcheck_type(self._argtypes_multi, coords[0]):
            if len(coords[0]) == 3:
                self.__coords = coords[0]
            else:
                raise ValueError("Point only works in 3D space.")
        elif len(coords) == 3:
            for c in coords:
                utility.argcheck_type(self._argtypes_single, c)
            self.__coords = array(coords)
        else:
            raise TypeError("Point constructor takes either one ndarray or 3 floats as arguments.")

        self.__x = self.__coords[0]
        self.__y = self.__coords[1]
        self.__z = self.__coords[2]

    @property
    def x(self) -> float:
        return self.__x

    @x.setter
    def x(self, x_coord):
        utility.argcheck_type(self._argtypes_single, x_coord)
        self.__coords[0] = x_coord
        self.__x = x_coord

    @property
    def y(self) -> float:
        return self.__y

    @y.setter
    def y(self, y_coord):
        utility.argcheck_type(self._argtypes_single, y_coord)
        self.__coords[1] = y_coord
        self.__y = y_coord

    @property
    def z(self) -> float:
        return self.__z

    @z.setter
    def z(self, z_coord):
        utility.argcheck_type(self._argtypes_single, z_coord)
        self.__coords[2] = z_coord
        self.__z = z_coord

    @property
    def coords(self) -> ndarray:
        return self.__coords

    @coords.setter
    def coords(self, new_coords: ndarray):
        utility.argcheck_type(self._argtypes_multi, new_coords)
        utility.argcheck_dim(self._dimension, new_coords)
        self.__coords = new_coords


class Line:
    """Line primitive in 3D space"""
    _dimension = 3
    _argtypes_point = [ndarray, Point]
    _argtypes_vector = [ndarray]

    def __init__(self, constraint_0, constraint_1, mode: str):
        """Creates line
        ARGS:
            constraint_0:
                Point object or ndarray representing a vector to (first) base point
            constraint_1:
                Point object or ndarray representing a vector to second base point
                or ndarray representing vector parallel to line
            mode (str): 'point' for defining line with two points or 'vector' for point and vector form
        """
        mode = utility.modecheck_type(mode)
        utility.argcheck_type(self._argtypes_point, constraint_0)
        utility.argcheck_dim(self._dimension, constraint_0, constraint_1)

        self.__point_a = utility.vec(constraint_0)
        if mode == 'point':
            utility.argcheck_type(self._argtypes_point, constraint_1)
            self.__point_b = utility.vec(constraint_1)
            self.__vector = self.__point_b - self.__point_a
        elif mode == 'vector':
            utility.argcheck_type(self._argtypes_vector, constraint_1)
            self.__vector = utility.vec(constraint_1)
            self.__point_b = self.__point_a + self.__vector
        else:
            e_str = f"Line parameter \'mode\' takes either \'point\' or \'vector\' as argument. Unknown argument {mode}"
            raise ValueError(e_str)

    @property
    def point_a(self) -> ndarray:
        return self.__point_a

    @point_a.setter
    def point_a(self, new_const):
        utility.argcheck_type( self._argtypes_point, new_const)
        utility.argcheck_dim(self._dimension, new_const)
        self.__point_a = utility.vec(new_const)
        self.__vector = self.__point_b - self.__point_a

    @property
    def point_b(self) -> ndarray:
        return self.__point_b

    @point_b.setter
    def point_b(self, new_const):
        utility.argcheck_type( self._argtypes_point, new_const)
        utility.argcheck_dim(self._dimension, new_const)
        self.__point_b = utility.vec(new_const)
        self.__vector = self.__point_b - self.__point_a

    @property
    def vector(self) -> ndarray:
        return self.__vector

    @vector.setter
    def vector(self, new_vector: ndarray):
        utility.argcheck_type(self._argtypes_vector, new_vector)
        utility.argcheck_dim(self._dimension, new_vector)
        self.__vector = new_vector
        self.__point_b = self.__point_a + self.__vector

    def point(self, scale: float) -> ndarray:
        """Returns a point on the line.
        ARGS:
            scale (float): scales the direction vector of the line extending from base point
        RETURNS:
            point_on_line (ndarray): Point on line, determined by scaling line direction vector
        """
        utility.argcheck_type([int, float], scale)
        point_on_line = self.point_a + scale * self.vector
        return point_on_line


class Plane:
    "Plane primitive in 3D space"
    _dimension = 3
    _const_type = Point
    _argtypes_point = [ndarray, Point]
    _argtypes_vector = [ndarray]

    def __init__(self, constraint_0, constraint_1, constraint_2, mode: str):
        """Creates a plane. 3 forms of representation are possible:
        - three points
        - point and two vectors defining plane
        - point, vector parallel to plane and vector normal to plane
        ARGS:
            constraint_0:
                Point object or ndarray representing vector to base point
            constraint_1:
                Point object or ndarray representing vector to second base point
                or ndarray representing vector parallel to plane
            constraint_2:
                Point object or ndarray representing vector to third base point
                or ndarray representing second vector parallel to plane (non-parallel to constraint_1)
                or ndarray representing vector normal to plane
            mode (str): "point", "vector", "normal" for plane representation
        """
        utility.argcheck_dim(self._dimension, constraint_0, constraint_1, constraint_2)
        utility.argcheck_type(self._argtypes_point, constraint_0)
        mode = utility.modecheck_type(mode)


        self.__point_a = utility.vec(constraint_0)
        if mode == 'point':
            utility.argcheck_type(self._argtypes_point, constraint_1)
            utility.argcheck_type(self._argtypes_point, constraint_2)

            self.__point_b = utility.vec(constraint_1)
            self.__point_c = utility.vec(constraint_2)
            self.__vector_u = self.__point_b - self.__point_a
            self.__vector_v = self.__point_c - self.__point_a
        else:
            utility.argcheck_type(self._argtypes_vector, constraint_1)
            utility.argcheck_type(self._argtypes_vector, constraint_2)

            self.__vector_u = utility.vec(constraint_1)
            self.__point_b = self.__point_a + self.__vector_u
            if mode == 'vector':
                self.__vector_v = utility.vec(constraint_2)
            elif mode == 'normal':
                # generate second plane defining vector to calculate points on plane
                self.__vector_v = cross(self.__point_c, self.__vector_u)
            else:
                e_str = f"Plane parameter \'mode\' takes either \'point\', \'vector\' or \'normal\' as argument. " \
                        f"Unknown argument {mode}"
                raise ValueError(e_str)
            self.__point_c = self.__point_a + self.__vector_v
        self.__normal = cross(self.__vector_u, self.__vector_v)

    def __recalc_normal(self):
        """Recalculates the normal after point update."""
        self.__vector_u = self.__point_b - self.__point_a
        self.__vector_v = self.__point_c - self.__point_a
        self.__normal = cross(self.__vector_u, self.__vector_v)

    @property
    def point_a(self) -> ndarray:
        return self.__point_a

    @point_a.setter
    def point_a(self, new_const):
        utility.argcheck_type(self._argtypes_point, new_const)
        utility.argcheck_dim(self._dimension, new_const)
        self.__point_a = utility.vec(new_const)
        self.__recalc_normal()

    @property
    def point_b(self) -> ndarray:
        return self.__point_b

    @point_b.setter
    def point_b(self, new_const):
        utility.argcheck_type(self._argtypes_point, new_const)
        utility.argcheck_dim(self._dimension, new_const)
        self.__point_b = utility.vec(new_const)
        self.__recalc_normal()

    @property
    def point_c(self) -> ndarray:
        return self.__point_c

    @point_c.setter
    def point_c(self, new_const):
        utility.argcheck_type(self._argtypes_point, new_const)
        utility.argcheck_dim(self._dimension, new_const)
        self.__point_c = utility.vec(new_const)
        self.__recalc_normal()

    @property
    def normal(self) -> ndarray:
        return self.__normal

    def point(self, scale_a: float, scale_b: float) -> ndarray:
        """Calculates a point on the plane
        ARGS:
           scale_a (float): scales vector a
           scale_b (float): scales vector b
        RETURNS:
            point_on_plane (ndarray): Point on plane, determined by scaling defining vectors
        """
        utility.argcheck_type([int, float], scale_a)
        utility.argcheck_type([int, float], scale_b)
        point_on_plane = self.point_a + scale_a * self.__vector_v + scale_b * self.__vector_v
        return point_on_plane
