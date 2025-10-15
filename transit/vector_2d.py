import math
import numpy as np


def rotate(v, angle):
    """Rotate a vector around the origin.
    v: array of 2d vector
    angle: angle in radians (clockwise)

    return numpy array of 2d vector
    """
    n0 = math.cos(angle) * v[0] - math.sin(angle) * v[1]
    n1 = math.sin(angle) * v[0] + math.cos(angle) * v[1]

    return np.array([n0, n1])


def length(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def add_arrowhead_points(p0, p1, size=1):
    """
    Add an arrowhead to the end of p1.
    :param p0: The point of the start of the line
    :param p1: The point of the end of the line
    :param size: The size of the arrowhead (default: 1)
    :return: an array of points that draw a polyline with an arrowhead at the end of the line.
    """
    l = length(p0 - p1)
    n1 = rotate(p0 - p1, math.pi / 6) * size / l + p1
    n2 = rotate(p0 - p1, -math.pi / 6) * size / l + p1

    return [p0, p1, n1, p1, n2]
