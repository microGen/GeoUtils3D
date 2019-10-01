"""Utility functions for 3D geometry operations.
Uses numpy arrays for 3D representations.
Point / Vertex: numpy.array([x, y, z])
Line / Edge:    numpy.array([Point, Point])
Plane / Face:   numpy.array([Point, Point, Point])"""

import numpy as np

def calculate_normal(face):
    """Calculates normal of a face defined by 3 points in 3D space."""
    return np.cross(face[1]-face[0], face[2]-face[0])

def dist_point_point(point_0, point_1):
    """Calculates the distance between two points in 3D space."""
    if type(point_0) != np.ndarray:
        point_0 = np.asarray(point_0)
    if type(point_1) != np.ndarray:
        point_1 = np.asarray(point_1)

    vector = point_1 - point_0
    return np.linalg.norm(vector)

def dist_point_line(point, line):
    """Calculates the distance between a point and a line defined by 2 points in 3D space"""
    if type(point) != np.ndarray:
        point = np.asarray(point)
    if type(line) != np.ndarray:
        line = np.asarray(line)

    line_vector = line[1] - line[0]
    num = np.linalg.norm(np.cross(line_vector, (point - line[0])))
    return num / np.linalg.norm(line_vector)

def dist_point_plane(point, plane):
    """Calculates the distance of a point to a plane defined by 3 points in 3D space."""
    if type(point) != np.ndarray:
        point = np.asarray(point)
    if type(plane) != np.ndarray:
        plane = np.asarray(plane)

    normal = calculate_normal(plane)
    num = np.linalg.norm(np.dot(normal, (np.subtract(point, plane[0]))))
    return num / np.linalg.norm(normal)

def intersection_line_plane(line, plane):
    """Calculates the intersection point between a line defined by 2 points
    and a plane defined by 3 points in 3D space."""
    line_vector = line[1] - line[0]
    normal = calculate_normal(plane)
    num = np.dot(normal, (plane[0] - line[0]))
    den = np.dot(normal, line_vector)
    intersection_point = line[0] + np.dot(num/den, line_vector)
    return intersection_point

def map_xyz_to_uv(origin, u_axis, normal, point):
    """Map coordinates of a point in 3D space to local UV coordinates.
    origin: origin of local coordinate system
    u_axis: vector defining local U axis
    normal: normal pointing out of UV plane
    coords: coordinates to be translated"""
    if type(origin) != np.ndarray:
        origin = np.asarray(origin)
    if type(u_axis) != np.ndarray:
        u_axis = np.asarray(u_axis)
    if type(normal) != np.ndarray:
        normal = np.asarray(normal)
    if type(point) != np.ndarray:
        point = np.asarray(point)

    point = point - origin
    v_axis = np.cross(u_axis, -normal)
    #normalize coordinate system
    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)
    uv_system = np.stack((u_axis, v_axis))
    uv_coords = np.dot(uv_system, point)
    return uv_coords

def point_in_triangle(face_uv, point_uv):
    """Calculates whether point is within bounds of given triangular face in 2D space."""

    #check whether point is on the same side of an edge as the third vertex of the triangle
    alignment = lambda p0, p1, line: np.dot(np.cross(line[1] - line[0], p0 - line[0]),\
                                      np.cross(line[1] - line[0], p1 - line[0])) >= 0
    #create edges from vertices
    edges = []
    for i in range(3):
        edges.append(np.array([face_uv[i%3], face_uv[(i+1)%3]]))
    return alignment(point_uv, face_uv[0], edges[1]) and alignment(point_uv, face_uv[1], edges[2]) and\
        alignment(point_uv, face_uv[2], edges[0])
