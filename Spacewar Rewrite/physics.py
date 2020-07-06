import numpy as np
import math
from time import time


grav_const = 6.67408e-11

def to_polar(point):
    u"""Converts a point from cartesian to polar coordinates

    Args:
        point (array): Point in form of cartesian (x, y) to convert

    Returns:
        numpy array: Same point in polar coordinates in form of (r, θ), where θ is in degrees
    """
    return np.array((math.sqrt(point[1]**2+point[0]**2), math.degrees(math.atan2(point[0], point[1]))))

def to_cartesian(point):
    u"""Converts a point from polar to cartesian coordinates

    Args:
        point (array): Point in form of polar (r, θ), where θ is in degrees

    Returns:
        numpy array: Same point in cartesian coordinates in form of (x, y)
    """
    return np.array((np.cos(math.radians(point[1]))*point[0], np.sin(math.radians(point[1]))*point[0]))

def accduetograv(M, R, grav_const=grav_const):
    """Calculates acceleration due to gravity of an object

    Args:
        M (float): Mass of the object
        R (float): Distance from object
        grav_const (float, optional): Gravitational constant. Defaults to 6.67408e-11.

    Returns:
        float: Acceleration due to gravity
    """
    return grav_const*(M / R**2)

def gravforce(*args, **kwargs):
    if len(args) == 2:
        return args[0]*args[1]
    elif len(args) == 3:
        return args[0]*accduetograv(*args[1:], **kwargs)
    else:
        raise TypeError("gravforce expected 2 or 3 arguments, got " + len(args))

class PhysicalObject():
    def __init__(self, mass=1):
        self.acc = np.array((0, 0), dtype="float")
        self.vel = np.array((0, 0), dtype="float")
        self.pos = np.array((0, 0), dtype="float")
        self.dt = time()
        self.created = time()
        self._polar = None
        self._polar_done = np.array((0, 0))

    @property
    def alive(self):
        return time() - self.created

    @property
    def polar(self, relative_to=(0, 0)):
        if np.array_equal(self._polar_done, self.pos) and relative_to == (0, 0):
            return self._polar
        else:
            self._polar_done = np.array(self.pos)
            self._polar = to_polar(self.pos-relative_to)
            return self._polar
    
    @property
    def cartesian(self, relative_to=(0, 0)):
        return self.pos-relative_to

    def update(self):
        self.dt = time() - self.dt
        self.vel += self.acc * self.dt
        self.pos += self.vel * self.dt
        self.dt = time()
