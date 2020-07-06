import numpy as np
from time import time

class PhysicalObject():
    def __init__(self):
        self.acc = np.array((0, 0), dtype="float")
        self.vel = np.array((0, 0), dtype="float")
        self.pos = np.array((0, 0), dtype="float")
        self.dt = time()
        self.created = time()

    @property
    def alive(self):
        return time() - self.created

    def update(self):
        self.dt = time() - self.dt
        self.vel += self.acc * self.dt
        self.pos += self.vel * self.dt
        self.dt = time()

