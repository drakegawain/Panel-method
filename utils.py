from numericFunctions import define_panels
from geometricFunctions import naca4_airfoil_xy, divideCp
from posProcessing import Solution
from velocityCalculations import vInf
from linearSystem import computeLambdasVortex, computeTangentVelocityVortex
from coeficients import computeCp

def computeSolution(m, p, t, nPoints, nPanels, alpha):

    v_inf = vInf(alpha)
    x, y = naca4_airfoil_xy(m, p, t, nPoints)
    panels = define_panels(x, y, nPanels)
    #panels.reverse() nao sei pq antes funcionava e agora nao precisa mais disso
    uk = computeLambdasVortex(panels, v_inf)
    vt = computeTangentVelocityVortex(uk, panels, v_inf)
    cp = computeCp(vt, v_inf)

    return Solution(panels, x, y, cp)