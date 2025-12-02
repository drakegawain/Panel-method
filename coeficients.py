from geometricClasses import Velocity
from geometricFunctions import divideCp
from numericClasses import Panel
import math

def computeCp(Vt: list, Vinf: Velocity):
    return [(1-(x/Vinf.magnitude)**2) for x in Vt]

def computeCl(panels: Panel, cp: list, alpha):

    xu, yu, xl, yl, cpU, cpL = divideCp(panels, cp)


    x = 0

    sumCpUx = 0
    sumCpUy = 0
    sumCpLx = 0
    sumCpLy = 0

    xu.reverse()
    yu.reverse()
    cpU.reverse()

    print(xl)

    for i in range(len(xu)):
        deltaX = xu[i]-x
        sumCpUx += cpU[i]*deltaX
        x = xu[i]

    x = 0

    for i in range(len(xl)):
        deltaX = xl[i]-x
        sumCpLx += cpL[i]*deltaX
        x = xl[i]

    y = 0

    for i in range(len(yu)):
        deltay = yu[i]-y
        sumCpUy += cpU[i]*deltay
        y = yu[i]

    y = 0

    for i in range(len(yl)):
        deltay = yl[i]-y
        sumCpLy += cpL[i]*deltay
        y = yl[i]

    cn = sumCpLx - sumCpUx
    ca = sumCpUy - sumCpLy

    return cn*math.cos(math.radians(alpha)) - ca*math.sin(math.radians(alpha))