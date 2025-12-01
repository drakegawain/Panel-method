import math

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass


class Velocity:

    def __init__(self, u, v):

        self.u = u
        self.v = v
        self.magnitude = math.sqrt((self.u**2)+(self.v**2))
        pass

