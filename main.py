from geometricFunctions import naca4_airfoil_xy, upperAndLower, divideCp
from numericFunctions import define_panels
from linearSystem import computeLambdasVortex, computeTangentVelocityVortex
from coeficients import computeCp, computeCl
from velocityCalculations import vInf, takeOffVelocity
from posProcessing import Solution, plot_family, plot_painels_numerados
from utils import computeSolution
import matplotlib.pyplot as plt

def main():

    m, p, t, N = 0, 0, 12, 200
    nPanels = 40

    alfa = [-15, -10, -5, 0, 5, 10, 15]

    s = []

    for a in alfa:
        s.append(computeSolution(m, p, t, N, nPanels, a))

    
    ss = {-15:s[0], -10:s[1], -5:s[2], 0: s[3], 5:s[4], 10:s[5], 15:s[6]}
    #plot_family(f"NACA {m}{p}{t}", ss, ["C0", "C1", "C2", "C3", "C4", "C5", "C6"])

    cl = []

    for i, sol in enumerate(s):
        panels = sol.panel_list
        cp = sol.Cp
        a = alfa[i]
        cl.append(computeCl(panels, cp, a))

    #panels = s.panel_list
    #cp = s.Cp
    #plot_painels_numerados(panels, "Ordenamento de vetores")

    xu, yu, xl, yl, cpU, cpL = divideCp(s[4].panel_list, s[4].Cp)

    #print(xl)

    fig, ax = plt.subplots()
    ax.plot(xu, yu, label="Superior")
    
    ax.plot(xl, yl, label="Inferior")
    ax.legend()
    ax.set_aspect("equal")
    plt.show()

    fig, ax = plt.subplots()
    #ax.plot(alfa, cl)
    ax.plot(xu, cpU, label="Superior")
    
    ax.plot(xl, cpL, label="Inferior")
    
    ax.invert_yaxis()
    ax.legend()
    #ax.set_aspect("equal")
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(alfa, cl)
    plt.show()

    # beleza, integração do coeficiente de sustentação funcionando

    

    return



if __name__ == "__main__":

    #================== CESNA 150 DATA ======================
    S = 15                      # AREA IN M^2
    W = 4380                    # WEIGHT IN NEWTONS
    rho = 1.2                   # DENSITY IN KILOGRAMS PER CUBIC METER
    m, p, t = 2, 4, 12          # NACA 2412 AS ANDERSON
    alpha = 5                   # ATTACK ANGLE
    N = 200                     # NUMBER OF POINTS OF GEOMETRIC DISCRETIZATION OF AIRFOILS
    NP = 40                     # NUMBER OF PANES
    
    #================= VORTEX PANE METHOD ====================
    s = computeSolution(m, p, t, N, NP, alpha)
    cp = s.Cp
    panels = s.panel_list

    #======================== Cl =============================
    cl = computeCl(panels, cp, alpha)

    #===================== TAKEOFF VELOCITY ==================
    vtoff = takeOffVelocity(W, cl, rho, S)

    print(f"TAKE OFF VELOCITY IS: {vtoff} m/s")
    print(f"TAKE OFF VELOCITY IS: {vtoff*3.6} KM/H")

