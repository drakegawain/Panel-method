from geometricClasses import Point, Vector
import math

class Panel:

    def __init__(self, begin: Point, end: Point):
        self.begin = begin
        self.end = end
        self.s = self.size()
        self.control_point = self.controlPoint()

        self.tangent_vector = self.tangentVector()
        self.normal_vector = self.normalVector()

    def tangentVector(self):
    # sempre do begin → end
        dx = self.end.x - self.begin.x
        dy = self.end.y - self.begin.y
        return Vector(dx/self.s, dy/self.s)

    def normalVector(self):
    # normal "cruzada" à direita da tangente
        t = self.tangent_vector
        return Vector(-t.y, t.x)

    def size(self):
        x = self.end.x - self.begin.x
        y = self.end.y - self.begin.y
        return math.sqrt((x**2)+(y**2))
    
    def controlPoint(self):
        x = (self.end.x + self.begin.x)/2
        y = (self.end.y + self.begin.y)/2
        cp = Point(x, y)
        return cp