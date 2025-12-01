from geometricClasses import Point, Vector, Velocity

def rij(control_point1: Point, control_point2: Point):
    x = control_point1.x - control_point2.x
    y = control_point1.y - control_point2.y
    r = Vector(x, y)
    return r

def escalarProduct(vector1: Vector, vector2: Vector):
    answ = (vector1.x*vector2.x)+(vector1.y*vector2.y)
    return answ

def escalarProduct2(vector1: Vector, velocity: Velocity):
    answ = (vector1.x*velocity.u)+(vector1.y*velocity.v)
    return answ
