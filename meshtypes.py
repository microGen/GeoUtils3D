"""Solid geometry (mesh) types derived from general 3D math geometry primitives.

Copyright (c) 2020 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

from numpy import array
from numpy import ndarray

import utility
from mathtypes import Point as __Point
#from mathtypes import Line as __Line
from mathtypes import Plane as __Plane


class Vertex(__Point):
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


class Face(__Plane):
    """Face primitive in 3D space"""
    # can be defined with points and edges
    # edges have to share vertices with next/previous edges
    # edges connect counter-clockwise
    # use edges to find neighboring face
    _dimension = 3
    _argtypes_vert = [ndarray, Vertex]

    def __init__(self, element_0, element_1, element_2 = None):
        if element_2 is not None:
            # Vertex initialization mode
            utility.argcheck_type(self._argtypes_vert, element_0)
            utility.argcheck_type(self._argtypes_vert, element_1)
            utility.argcheck_type(self._argtypes_vert, element_2)
        else:
            if type(element_0) == Edge and type(element_1) == Edge:
                # Two Edge initialization mode
                pass
            else:
                # Vertex and Edge initialization mode. End vertices of edge must be distinct from passed vertex.
                args = [element_0, element_1]
                arg_edge = next(filter(lambda a: type(a) == Edge, args))
                arg_vert = next(filter(lambda a: type(a) != Edge, args))
                utility.argcheck_type(self._argtypes_vert, arg_vert)
