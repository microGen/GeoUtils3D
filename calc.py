"""Utility functions for 3D geometry operations.

Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)
"""

import numpy as np
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])
PointUV = namedtuple('PointUV', ['u', 'v'])
Line = namedtuple('Line', ['Point_0', 'Point_1'])
LineUV = namedtuple('LineUV', ['PointUV_0', 'PointUV_1'])
Plane = namedtuple('Face', ['Point_0', 'Point_1', 'Point_2'])
PlaneUV = namedtuple('PlaneUV', ['PointUV_0', 'PointUV_1', 'PointUV_2'])

def calculate_normal(plane: Plane) -> np.ndarray:
    """Calculates normal of a face defined by 3 points in 3D space.
    ARGS:
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        normal_vector (np.ndarray): vector normal to plane in 3D space
    """
    pl0, pl1, pl2 = [np.array(pli) for pli in plane]
    normal_vector = np.cross(pl1-pl0, pl2-pl0)
    return normal_vector

def dist_point_point(point_0: Point, point_1: Point) -> float:
    """Calculates the distance between two points in 3D space.
    ARGS:
        point_0, point_1 (Point): Points in 3D space
    RETURNS:
        dist (float): scalar distance between both points
    """
    p0 = np.array(point_0)
    p1 = np.array(point_1)
    vector = p1 - p0
    dist = np.linalg.norm(vector)
    return dist

def dist_point_line(point: Point, line: Line) -> float:
    """Calculates the distance between a point and a line in 3D space.
    ARGS:
        point (Point): Point in 3D space
        line (Line): Line in 3D space defined by 2 points
    RETURNS:
        dist(float): scalar minimum distance between point and line
    """
    p = np.array(point)
    l0, l1 = [np.array(li) for li in line]
    l_vector = l1 - l0
    num = np.linalg.norm(np.cross(l_vector, (p-l0)))
    dist = num / np.linalg.norm(l_vector)
    return dist

def dist_point_plane(point: Point, plane: Plane) -> float:
    """Calculates the distance of a point to a plane in 3D space.
    ARGS:
        point (Point): Point in 3D space
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        dist(float): scalar minimum distance between point and line
    """
    p = np.array(point)
    pl0, pl1, pl2 = [np.array(pli) for pli in plane]
    normal = np.array(calculate_normal(plane))
    num = np.linalg.norm(np.dot(normal, (np.subtract(p, pl0))))
    dist = num / np.linalg.norm(normal)
    return dist

def intersection_line_plane(line: Line, plane: Plane) -> Point:
    """Calculates the intersection point between a line and a plane in 3D space.
    ARGS:
        line (Line): Line in 3D space defined by 2 points
        plane (Plane): Plane in 3D space defined by 3 points
    RETURNS:
        intersection_point (Point): intersection of both lines
    """
    line_vector = np.array(line[1]) - np.array(line[0])
    normal = calculate_normal(plane)
    num = np.dot(normal, (np.array(plane[0]) - np.array(line[0])))
    den = np.dot(normal, line_vector)
    intersection_point = Point(*(np.array(line[0]) + np.dot(num/den, line_vector)))
    return intersection_point

def map_xyz_to_uv(origin: Point, u_axis: np.ndarray, normal: np.ndarray, point: Point) -> PointUV:
    """Map coordinates of a point in 3D space to local UV coordinates.
    ARGS:
        origin (Point): origin of local coordinate system
        u_axis (np.ndarray): vector defining local U axis
        normal (np.ndarray): normal pointing out of UV plane
            i.e. the plane in 3D space on which the UV coordinate system resides
        point (Point): Point to be translated to UV projection
    RETURNS:
        uv_coords (PointUV): UV coordinates of point
    """
    origin = np.array(origin)
    p = np.array(point)

    p = p - origin
    v_axis = np.cross(u_axis, -normal)
    #normalize coordinate system
    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)
    uv_system = np.stack((u_axis, v_axis))
    uv_coords = PointUV(*np.dot(uv_system, p))
    return uv_coords

def point_in_triangle(face_uv: PlaneUV, point_uv: PointUV) -> bool:
    """Calculates whether point is within bounds of given triangular face in 2D space.
    ARGS:
        face_uv (PlaneUV): triangle in UV space defined by 3 points
        point_uv (PlaneUV): point in UV space
    RETURNS:
        in_bounds (bool): True if point is in triangle, False if not
    """
    #check whether point is on the same side of an edge as the third vertex of the triangle
    alignment = lambda p0, p1, line: np.dot(np.cross(line[1] - line[0], p0 - line[0]),\
                                      np.cross(line[1] - line[0], p1 - line[0])) >= 0
    p_uv = np.array(point_uv)
    #create edges from vertices
    edges = []
    for i in range(3):
        edges.append(np.array([face_uv[i%3], face_uv[(i+1)%3]]))
    in_bounds = alignment(p_uv, face_uv[0], edges[1]) and alignment(p_uv, face_uv[1], edges[2]) and\
        alignment(p_uv, face_uv[2], edges[0])
    return in_bounds

def project_vector(vector_0: np.array, vector_1: np.array) -> np.array:
    """Projects vector_0 onto vector_1 and returns the resulting vector.
    ARGS:
        vector_0, vector_1 (np.array): vectors in 3D space
    RETURNS:
        projection (np.array): projected vector in 3D space
    """
    num = np.dot(vector_1, vector_0)
    den = np.dot(vector_1, vector_1)
    projection = num / den * vector_1
    return projection