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
        self.__vertex_a = utility.vec(new_vert)
        self.__vector = self.__vertex_b - self.__vertex_a

    @property
    def vertex_b(self):
        return Vertex(self.__vertex_b)

    @vertex_b.setter
    def vertex_b(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_b = utility.vec(new_vert)
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
    _argtypes_edge = [Edge]

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
            self.__vertex_a = utility.vec(element_0)
            self.__vertex_b = utility.vec(element_1)
            self.__vertex_c = utility.vec(element_2)
        else:
            if type(element_0) == self._argtypes_edge[0] and type(element_1) == self._argtypes_edge[0]:
                # Two Edge initialization mode
                v0a = utility.vec(element_0.vertex_a)
                v0b = utility.vec(element_0.vertex_b)
                v1a = utility.vec(element_1.vertex_a)
                v1b = utility.vec(element_1.vertex_b)
                if reduce(tol_comp, c_in_tol(v0a - v1a, sigma)) or reduce(tol_comp, c_in_tol(v0a - v1b, sigma)):
                    self.__vertex_a = v0b
                elif reduce(tol_comp, c_in_tol(v0b - v1a, sigma)) or reduce(tol_comp, c_in_tol(v0b - v1b, sigma)):
                    self.__vertex_a = v0a
                else:
                    raise ValueError("Passed Edge objects do not share at least 1 Vertex.")
                self.__vertex_b = v1a
                self.__vertex_c = v1b
            else:
                # Vertex and Edge initialization mode
                args = [element_0, element_1]
                self.__vertex_a = utility.vec(next(filter(lambda a: type(a) != Edge, args)))
                utility.argcheck_type(self._argtypes_vert, self.__vertex_a)
                arg_edge = next(filter(lambda a: type(a) == Edge, args))
                self.__vertex_b = utility.vec(arg_edge.vertex_a)
                self.__vertex_c = utility.vec(arg_edge.vertex_b)
        utility.argcheck_dim(self._dimension, self.__vertex_a, self.__vertex_b, self.__vertex_c)

        self.__edge_a = Edge(self.__vertex_a, self.__vertex_b)
        self.__edge_b = Edge(self.__vertex_b, self.__vertex_c)
        self.__edge_c = Edge(self.__vertex_c, self.__vertex_a)

        self.__vector_u = self.__vertex_b - self.__vertex_a
        self.__vector_v = self.__vertex_c - self.__vertex_a
        self.__normal = cross(self.__vector_u, self.__vector_v)

    def __recalc_edges(self):
        """(Re)Calculates the edges in Face."""
        self.__edge_a = Edge(self.__vertex_a, self.__vertex_b)
        self.__edge_b = Edge(self.__vertex_b, self.__vertex_c)
        self.__edge_c = Edge(self.__vertex_c, self.__vertex_a)

    def __recalc_vertices(self, edge_id):
        """(Re)Calculates vertices in Face."""
        if edge_id == 'a':
            self.__vertex_a = self.__edge_a.vertex_a
            self.__vertex_b = self.__edge_a.vertex_b
            self.__vertex_c = self.__edge_c.vertex_a
        elif edge_id == 'b':
            self.__vertex_a = self.__edge_a.vertex_a
            self.__vertex_b = self.__edge_b.vertex_a
            self.__vertex_c = self.__edge_b.vertex_b
        elif edge_id == 'c':
            self.__vertex_a = self.__edge_c.vertex_b
            self.__vertex_b = self.__edge_b.vertex_a
            self.__vertex_c = self.__edge_c.vertex_a
        else:
            raise ValueError(f"No edge {edge_id} in Face")

    def __recalc_normal(self):
        """(Re)Calculates normal of Face"""
        self.__vector_u = self.__vertex_b - self.__vertex_a
        self.__vector_v = self.__vertex_c - self.__vertex_a
        self.__normal = cross(self.__vector_u, self.__vector_v)

    def flip(self):
        """Flips Face along normal."""
        self.__vertex_b, self.__vertex_c = self.__vertex_c, self.__vertex_b
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def vertex_a(self):
        return Vertex(self.__vertex_a)

    @vertex_a.setter
    def vertex_a(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_a = utility.vec(new_vert)
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def vertex_b(self):
        return Vertex(self.__vertex_b)

    @vertex_b.setter
    def vertex_b(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_b = utility.vec(new_vert)
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def vertex_c(self):
        return Vertex(self.__vertex_c)

    @vertex_c.setter
    def vertex_c(self, new_vert):
        utility.argcheck_type(self._argtypes_vert, new_vert)
        utility.argcheck_dim(self._dimension, new_vert)
        self.__vertex_c = utility.vec(new_vert)
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def edge_a(self):
        return self.__edge_a

    @edge_a.setter
    def edge_a(self, new_edge):
        utility.argcheck_type(self._argtypes_edge, new_edge)
        self.__edge_a = new_edge
        self.__recalc_vertices()
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def edge_b(self):
        return self.__edge_b

    @edge_b.setter
    def edge_b(self, new_edge):
        utility.argcheck_type(self._argtypes_edge, new_edge)
        self.__edge_b = new_edge
        self.__recalc_vertices()
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def edge_c(self):
        return self.__edge_c

    @edge_c.setter
    def edge_c(self, new_edge):
        utility.argcheck_type(self._argtypes_edge, new_edge)
        self.__edge_c = new_edge
        self.__recalc_vertices()
        self.__recalc_edges()
        self.__recalc_normal()

    @property
    def normal(self):
        return self.__normal

    @property
    def centerpoint(self):
        pass