import math
from spaceFunctions import escalarProduct, rij
from numericClasses import Panel
from geometricClasses import Point, Velocity

# ============== VELOCITY CALCULATIONS ====================

def vInf(alpha, magnitude=1) -> Velocity:

    u = math.cos(math.radians(alpha))*magnitude
    v = math.sin(math.radians(alpha))*magnitude
    return Velocity(u, v)


def deltaULinha(rotated_control_point_i: Point, panelj: Panel):
    A = 1/(4*math.pi)
    B = rotated_control_point_i.x + 0.5*panelj.s
    C = rotated_control_point_i.y
    D = rotated_control_point_i.x - 0.5*panelj.s
    E = math.log((B**2+C**2)/(D**2+C**2))
    return A*E

def deltaVLinha(rotated_control_point_i: Point, panelj: Panel):
    A = 1/(2*math.pi)
    B = math.atan2(rotated_control_point_i.y,rotated_control_point_i.x + 0.5*panelj.s)
    C = math.atan2(rotated_control_point_i.y, rotated_control_point_i.x - 0.5*panelj.s)
    if B < 0:
        B = B + 2*math.pi
    if C < 0:
        C = C + 2*math.pi
    return A*(B-C)

def deltaULinha_vor(rotated_control_point_i: Point, panelj: Panel):
    A = 1/(2*math.pi)
    B = math.atan2(rotated_control_point_i.y,(rotated_control_point_i.x - 0.5*panelj.s))
    C = math.atan2(rotated_control_point_i.y,(rotated_control_point_i.x + 0.5*panelj.s))
    if B < 0:
        B = B + 2*math.pi
    if C < 0:
        C = C + 2*math.pi
    return A*(B-C)

def deltaVLinha_vor(rotated_control_point_i: Point, panelj: Panel):
    A = 1/(4*math.pi)
    B = rotated_control_point_i.x - 0.5*panelj.s
    C = rotated_control_point_i.y
    D = rotated_control_point_i.x + 0.5*panelj.s
    E = math.log((B**2+C**2)/(D**2+C**2))
    return A*E


def computeRotatedVelocityComponent(paneli: Panel, panelj: Panel):
    r = rij(paneli.control_point, panelj.control_point)
    rotated_control_point = Point(escalarProduct(r, panelj.tangent_vector), escalarProduct(r, panelj.normal_vector))
    u = deltaULinha(rotated_control_point, panelj)
    v = deltaVLinha(rotated_control_point, panelj)
    V = Velocity(u, v)
    return V

def computeRotatedVelocityComponentVortex(paneli: Panel, panelj: Panel):
    r = rij(paneli.control_point, panelj.control_point)
    rotated_control_point = Point(escalarProduct(r, panelj.tangent_vector), escalarProduct(r, panelj.normal_vector))
    u = deltaVLinha(rotated_control_point, panelj)
    v = -deltaULinha(rotated_control_point, panelj)
    V = Velocity(u, v)
    return V

def computeVelocityComponent(paneli: Panel, panelj: Panel):
    V_linha = computeRotatedVelocityComponent(paneli, panelj)
    t = panelj.tangent_vector
    n = panelj.normal_vector   # (-t.y, t.x)

    u = V_linha.u * t.x - V_linha.v * n.x
    v = V_linha.u * t.y - V_linha.v * n.y
    return Velocity(u, v)

def computeVelocityComponent2(paneli: Panel, panelj: Panel):
    V = computeRotatedVelocityComponentVortex(paneli, panelj)
    t = panelj.tangent_vector
    n = panelj.normal_vector

    u = V.u*t.x - V.v*n.x
    v = V.u*t.y - V.v*n.y

    return Velocity(u, v)