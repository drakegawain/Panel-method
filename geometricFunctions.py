import numpy as np
import math

def yt_4digit(x, t):

    t=t/100

    x1 = math.sqrt(x)
    x2 = x
    x3 = x*x
    x4 = x*x*x
    x5 = x*x*x*x

    p1 = 0.2969
    p2 = -0.12600
    p3 = -0.35160
    p4 = 0.28430
    p5 = -0.1036

    t1 = t/0.20

    return t1*(p1*x1+p2*x2+p3*x3+p4*x4+p5*x5)


def yc(m, p, t, x):

    m = m/100
    p = p/10
    t = t/100

    if x <= p:
        p2 = p*p
        return (2*p*x-x*x)*(m/p2)
    
    if x > p:
        p2 = (1-p)**2
        A = 1-2*p
        B = 2*p*x
        C = -x**2
        return (A+B+C)*(m/p2)
    
    return "gonei"


def dycdx(m, p, t, x):

    m = m/100
    p = p/10
    t = t/100

    if x <= p:
        p2 = p**2
        A = 2*m/p2
        return (p-x)*A
    
    if x > p:
        p2 = (1-p)**2
        A=2*m/p2    
        return A*(p-x)

    return

def theta(m, p, t, x):
    return math.atan(dycdx(m,p,t,x))

def naca4_airfoil_xy(m, p, t, N=100):
    """
    Gera coordenadas de um aerofólio NACA 4 dígitos no formato Selig:
    TE (x≈1) -> LE (x≈0) pela superfície superior,
    depois LE -> TE pela superfície inferior.
    
    m, p, t: parâmetros NACA (ex: 2, 4, 12 para NACA 2412)
    N: número de pontos em cada meia-superfície (upper/lower).
    """

    # distribuição cosenoidal (melhor resolução perto do bordo de ataque)
    beta = np.linspace(0.0, np.pi, N)
    x = 0.5 * (1 - np.cos(beta))   # vai de 0 (LE) até 1 (TE)

    xu, yu, xl, yl = [], [], [], []

    for xi in x:
        XU, YU, XL, YL = naca(m, p, t, xi)
        xu.append(XU); yu.append(YU)
        xl.append(XL); yl.append(YL)

    xu = np.array(xu); yu = np.array(yu)
    xl = np.array(xl); yl = np.array(yl)

    # Formato Selig:
    # - upper: TE -> LE  (por isso [::-1])
    # - lower: LE -> TE  (já está assim)
    # - evitamos duplicar o ponto de LE (x≈0) removendo xl[0], yl[0]
    x_upper = xu[::-1]
    y_upper = yu[::-1]

    x_lower = xl[1:]
    y_lower = yl[1:]

    x_all = np.concatenate([x_upper, x_lower])
    y_all = np.concatenate([y_upper, y_lower])

    return x_all, y_all

def naca(m, p, t, x):

    if (m == 0) and (p == 0):
        yt = yt_4digit(x, t)
        xu = x
        yu = yt
        xl=x
        yl=-yt

    else:
        xu = x - yt_4digit(x, t)*math.sin(theta(m,p,t,x))
        yu = yc(m, p, t, x) + yt_4digit(x, t)*math.cos(theta(m,p,t,x))

        xl = x + yt_4digit(x, t)*math.sin(theta(m, p, t, x))
        yl = yc(m, p , t, x) - yt_4digit(x, t)*math.cos(theta(m, p, t, x))

    return xu, yu, xl, yl