from geometricClasses import Point
from numericClasses import Panel
import numpy as np


def selectPanelPoints(xu, yu, xl, yl, total_points_wanted):
    points = []

    # inferior: TE -> LE
    for i in range(len(xl)-1, -1, -1):
        points.append(Point(xl[i], yl[i]))

    # superior: LE -> TE, mas pulando LE (já usado) e TE (para não duplicar)
    for i in range(1, len(xu)-1):
        points.append(Point(xu[i], yu[i]))

    if points[0].x == points[-1].x and points[0].y == points[-1].y:
        points.pop()

    # agora faz o downsampling
    total_points = len(points)
    if total_points_wanted >= total_points:
        return points

    step = (total_points - 1) / (total_points_wanted - 1)
    selected = []
    idx = 0.0
    for _ in range(total_points_wanted):
        selected.append(points[int(round(idx))])
        idx += step
    return selected

def define_panels(x, y, N=40):
    """
    Discretizes the geometry into panels using 'cosine' method.
    
    Parameters
    ----------
    x: 1D array of floats
        x-coordinate of the points defining the geometry.
    y: 1D array of floats
        y-coordinate of the points defining the geometry.
    N: integer, optional
        Number of panels;
        default: 40.
    
    Returns
    -------
    panels: 1D np array of Panel objects.
        The list of panels.
    """
    
    R = (x.max() - x.min()) / 2.0  # circle radius
    x_center = (x.max() + x.min()) / 2.0  # x-coordinate of circle center
    
    theta = np.linspace(0.0, 2.0 * np.pi, N + 1)  # array of angles
    x_circle = x_center + R * np.cos(theta)  # x-coordinates of circle
    
    x_ends = np.copy(x_circle)  # x-coordinate of panels end-points
    y_ends = np.empty_like(x_ends)  # y-coordinate of panels end-points
    
    # extend coordinates to consider closed surface
    x, y = np.append(x, x[0]), np.append(y, y[0])
    
    # compute y-coordinate of end-points by projection
    I = 0
    for i in range(N):
        while I < len(x) - 1:
            if (x[I] <= x_ends[i] <= x[I + 1]) or (x[I + 1] <= x_ends[i] <= x[I]):
                break
            else:
                I += 1
        a = (y[I + 1] - y[I]) / (x[I + 1] - x[I])
        b = y[I + 1] - a * x[I + 1]
        y_ends[i] = a * x_ends[i] + b
    y_ends[N] = y_ends[0]
    
    # create panels
    panels = np.empty(N, dtype=object)
    points = []
    panels = []
    for i in range(N):
        panels.append(Panel(Point(x_ends[i+1], y_ends[i+1]), Point(x_ends[i], y_ends[i])))
        #points.append(Point(x_ends[i+1], y_ends[i+1]))
        #panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i + 1], y_ends[i + 1])
    
    return panels

def panelList(points: list[Point]) -> list[Panel]:

    panels = []

    for i in range(len(points) - 1):
        panels.append(Panel(points[i], points[i+1]))
    panels.append(Panel(points[-1], points[0]))
    panels.reverse()

    return panels

