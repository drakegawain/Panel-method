import matplotlib.pyplot as plt
import numpy as np

class Solution:
        def __init__(self, panel_list, x, y, Cp):
            self.panel_list = panel_list
            self.x = x
            self.y = y
            self.Cp = Cp
        pass


def plot_family(airfoil_name, solutions, colors):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(9, 7))

    # --- Geometria ---
    any_solution = next(iter(solutions.values()))
    ax1.plot(any_solution.x, any_solution.y, "-k")
    ax1.set_aspect("equal", "box")
    ax1.set_ylabel("y/c")
    ax1.set_title(f"{airfoil_name} – Geometria e distribuição de $C_p$")

    # --- Cp(x) separado em extradorso e intradorso ---
    for (alpha, sol), color in zip(solutions.items(), colors):
        panels = sol.panel_list
        Cp     = np.array(sol.Cp)

        x_cp = np.array([p.control_point.x for p in panels])
        y_cp = np.array([p.control_point.y for p in panels])

        # máscara para extradorso (y >= 0) e intradorso (y < 0)
        mask_up   = y_cp >= 0.0
        mask_down = y_cp < 0.0

        # ordenar por x dentro de cada superfície
        idx_up   = np.argsort(x_cp[mask_up])
        idx_down = np.argsort(x_cp[mask_down])

        x_up = x_cp[mask_up][idx_up]
        Cp_up = Cp[mask_up][idx_up]

        x_down = x_cp[mask_down][idx_down]
        Cp_down = Cp[mask_down][idx_down]

        # plota extradorso e intradorso separados
        ax2.plot(x_up,   Cp_up,   color=color, linestyle="-",  label=f"extradorso α={alpha}°")
        ax2.plot(x_down, Cp_down, color=color, linestyle="--", label=f"intrad. α={alpha}°")

    ax2.invert_yaxis()
    ax2.set_xlabel("x/c")
    ax2.set_ylabel("$C_p$")
    ax2.grid(True)
    ax2.legend()
    plt.tight_layout()
    plt.show()

def plot_painels_numerados(panel_list, title="Painéis do aerofólio"):
    fig, ax = plt.subplots(figsize=(8, 2.5))

    for i, p in enumerate(panel_list):
        # coordenadas do painel
        xs = [p.begin.x, p.end.x]
        ys = [p.begin.y, p.end.y]
        ax.plot(xs, ys, "-k")

        # ponto de controle
        xc = p.control_point.x
        yc = p.control_point.y

        # número do painel
        ax.text(xc, yc, f"{i}", color="red", fontsize=9,
                ha="center", va="center")

        # ---------- vetor tangente (azul) ----------
        t = p.tangent_vector
        t_len = (t.x**2 + t.y**2)**0.5
        if t_len == 0:
            continue
        tx = t.x / t_len
        ty = t.y / t_len

        scale_t = 0.06  # comprimento da setinha tangente
        ax.arrow(xc, yc, scale_t*tx, scale_t*ty,
                 head_width=0.008, head_length=0.015,
                 fc='blue', ec='blue')

        # ---------- vetor normal (verde) ----------
        n = p.normal_vector
        n_len = (n.x**2 + n.y**2)**0.5
        nx = n.x / n_len
        ny = n.y / n_len

        scale_n = 0.06  # comprimento da setinha normal
        ax.arrow(xc, yc, scale_n*nx, scale_n*ny,
                 head_width=0.008, head_length=0.015,
                 fc='green', ec='green')

    ax.set_aspect("equal", "box")
    ax.set_xlabel("x/c")
    ax.set_ylabel("y/c")
    ax.set_title(title)
    ax.grid(True)
    plt.tight_layout()
    plt.show()