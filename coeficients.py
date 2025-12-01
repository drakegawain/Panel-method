from geometricClasses import Velocity

def computeCp(Vt: list, Vinf: Velocity):
    return [(1-(x/Vinf.magnitude)**2) for x in Vt]