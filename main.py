from geometricFunctions import naca4_airfoil_xy
from numericFunctions import define_panels
from linearSystem import computeLambdasVortex, computeTangentVelocityVortex
from coeficients import computeCp
from velocityCalculations import vInf
from posProcessing import Solution, plot_family, plot_painels_numerados



def main():

    m, p, t, N = 0, 0, 12, 200
    nPanels = 40
    v_inf = vInf(0)

    x, y = naca4_airfoil_xy(m, p , t, N)
    panels = define_panels(x, y, nPanels)
    panels.reverse()
    uk = computeLambdasVortex(panels, v_inf) # unknowns, aqui calcula as variáveis desconhecidas do sistema linear
    vt = computeTangentVelocityVortex(uk, panels, v_inf)
    cp = computeCp(vt, v_inf)
    s = Solution(panels, x, y, cp)
    ss = {0: s}
    plot_family(f"NACA {m}{p}{t}", ss, ["C0"])
    plot_painels_numerados(panels, "Ordenamento de vetores")


    return



if __name__ == "__main__":
    main()