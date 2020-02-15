"""Solid geometry (mesh) types derived from general 3D math geometry primitives.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray
from numpy import cross
from functools import reduce

import utility
import mathtypes
import calc


class Vertex(mathtypes.Point):
    """Vertex primitive in 3D space"""
    _dimension = 3


class Edge:
    """Edge primitive in 3D space"""
    _dimension = 3
    _argtypes_vert = [ndarray, Vertex]

    def __init__(self, vert_0, vert_1):
        """Creates Edge
        ARGS:
            vert_0: Vertex object or ndarray representing vector to vertex
            vert_1: Vertex object or ndarray representing vector to vertex
        """
        utility.argcheck_type(self._argtypes_vert, vert_0)
        utility.argcheck_type(self._argtypes_vert, vert_1)
        utility.argcheck_dim(self._dimension, vert_0, vert_1)
        self.__vertex_a = utility.vec(vert_0)
        self.__vertex_b = utility.vec(vert_1)
        self.__vector = self.__vertex_b - self.__vertex_a

    @property
    def vertex_a(self):
        return Vertex(self.__vertex_a)

    @vertex_a.setter
    def vertex_a(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_a = new_vert
        self.__vector = self.__vertex_b - self.__vertex_a

    @property
    def vertex_b(self):
        return Vertex(self.__vertex_b)

    @vertex_b.setter
    def vertex_b(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_b = new_vert
        self.__vector = self.__vertex_b - self.__vertex_a

    @property
    def vector(self):
        return self.__vector

    def point(self, proportion: float):
        """Calculates a point on the edge.
        ARGS:
            proportion (float): Scalar between 0 and 1, representing the proportion of segment between first Vertex and
            point to total Edge length.
        RETURNS:
            point_on_edge (ndarray): Point on edge
        """
        utility.argcheck_type([int, float], proportion)
        utility.argcheck_minmax(0, 1, proportion)
        point_on_edge = self.__vertex_a + self.vector * proportion
        return point_on_edge


class Face:
    """Face primitive in 3D space"""
    # can be defined with points and edges
    # edges have to share vertices with next/previous edges
    # edges connect counter-clockwise
    # use edges to find neighboring face
    _dimension = 3
    _argtypes_vert = [ndarray, Vertex]

    def __init__(self, element_0, element_1, element_2 = None):
        sigma = 1e-8
        c_in_tol = lambda coord, tolerance: abs(coord) <= tolerance
        tol_comp = lambda c0, c1: c0 and c1

        # Accounting for all initialization modes
        if element_2 is not None:
            # Vertex initialization mode
            utility.argcheck_type(self._argtypes_vert, element_0)
            utility.argcheck_type(self._argtypes_vert, element_1)
            utility.argcheck_type(self._argtypes_vert, element_2)
            self.__vertex_a = element_0
            self.__vertex_b = element_1
            self.__vertex_c = element_2
        else:
            if type(element_0) == Edge and type(element_1) == Edge:
                # Two Edge initialization mode
                v0a = element_0.vertex_a
                v0b = element_0.vertex_b
                v1a = element_1.vertex_a
                v1b = element_1.vertex_b
                if reduce(tol_comp, c_in_tol(v0a.coords - v1a.coords, sigma)) or reduce(tol_comp, c_in_tol(v0a.coords - v1b.coords, sigma)):
                    self.__vertex_a = v0b
                elif reduce(tol_comp, c_in_tol(v0b.coords - v1a.coords, sigma)) or reduce(tol_comp, c_in_tol(v0b.coords - v1b.coords, sigma)):
                    self.__vertex_a = v0a
                else:
                    raise ValueError("Passed Edge objects do not share at least 1 Vertex.")
                self.__vertex_b = v1a
                self.__vertex_c = v1b
            else:
                # Vertex and Edge initialization mode
                args = [element_0, element_1]
                self.__vertex_a = next(filter(lambda a: type(a) != Edge, args))
                utility.argcheck_type(self._argtypes_vert, self.__vertex_a)
                arg_edge = next(filter(lambda a: type(a) == Edge, args))
                self.__vertex_b = arg_edge.vertex_a
                self.__vertex_c = arg_edge.vertex_b
        utility.argcheck_dim(self._dimension, self.__vertex_a, self.__vertex_b, self.__vertex_c)
        self.__element_order()

    def __element_order(self):
        """(Re)Calculates the element order in Face. Order is mathematically positive (ccw)."""
        u_vector = self.__vertex_b.coords - self.__vertex_a.coords
        v_plane = self.__vertex_c.coords - self.__vertex_a.coords
        n_vector = cross(u_vector, v_plane)
        uva = calc.map_xyz_to_uv(self.__vertex_a, u_vector, n_vector, self.__vertex_a)
        uvb = calc.map_xyz_to_uv(self.__vertex_a, u_vector, n_vector, self.__vertex_b)
        uvc = calc.map_xyz_to_uv(self.__vertex_a, u_vector, n_vector, self.__vertex_c)
        ab_vector = uvb.coords - uva.coords
        ac_vector = uvc.coords - uva.coords
        # if Edge AB is left of Edge AC: switch Vectors B and C
        if cross(ab_vector, ac_vector) < 0:
            self.__vertex_b, self.__vertex_c = self.__vertex_c, self.__vertex_b
