import numpy as np
from geometricClasses import Velocity
from numericClasses import Panel
from velocityCalculations import computeVelocityComponent, computeVelocityComponent2
from spaceFunctions import escalarProduct2



def computeLambdasVortex(panel_list: list[Panel], Vinf):

    N = len(panel_list)

    # sistema global
    A = np.zeros((N+1, N+1), dtype=float)
    b = np.zeros(N+1, dtype=float)

    # 1) N equações de não-penetração
    for i in range(N):

        ni = panel_list[i].normal_vector
        ti = panel_list[i].tangent_vector

        sum_vor_normal = 0.0

        for j in range(N):

            # --- fonte unitária no painel j ---
            Vji_fon  = computeVelocityComponent(panel_list[i], panel_list[j])
            Vnji_fon = escalarProduct2(ni, Vji_fon)

            # guarda a influência "bruta" da fonte
            

            # na matriz global A, a diagonal vira 0.5
            if i == j:
                A[i, j] = 0.5
            else:
                A[i, j] = Vnji_fon

            # --- vórtice unitário no painel j ---
            Vji_vor  = computeVelocityComponent2(panel_list[i], panel_list[j])
            Vnji_vor = escalarProduct2(ni, Vji_vor)

            # coeficiente de γ é a soma sobre j
            sum_vor_normal += Vnji_vor

        # coeficiente de γ na equação i
        A[i, N] = sum_vor_normal

        # lado direito: -Vinf·n_i
        b[i] = -escalarProduct2(ni, Vinf)

    # 2) Condição de Kutta nos dois painéis de TE (0 e N-1)
    pk1 = panel_list[0]
    pk2 = panel_list[N-1]

    tk1 = pk1.tangent_vector
    tk2 = pk2.tangent_vector
    #tk1 = Vector(-tk1.x, -tk1.y)
    #tk2 = Vector(-tk2.x, -tk2.y)

    # lado direito: - (Vinf·t0 + Vinf·tN-1)
    b[N] =  -(escalarProduct2(tk1, Vinf) + escalarProduct2(tk2, Vinf))

    # coeficientes na equação de Kutta

    
    for j in range(N):
        vj = panel_list[j]

    # influência da fonte
        V0_j = computeVelocityComponent(pk1, vj)
        VN_j = computeVelocityComponent(pk2, vj)

        A[N, j] = escalarProduct2(tk1, V0_j) + escalarProduct2(tk2, VN_j)

# Influência do vórtice global (mesmo para todos os painéis)
    sum_gamma = 0.0
    for j in range(N):
        V0_v = computeVelocityComponent2(pk1, panel_list[j])
        VN_v = computeVelocityComponent2(pk2, panel_list[j])
        sum_gamma += escalarProduct2(tk1, V0_v)
        sum_gamma += escalarProduct2(tk2, VN_v)

    A[N, N] = sum_gamma

# Termo independente (velocidade livre)
    b[N] = - (
    escalarProduct2(tk1, Vinf) +
    escalarProduct2(tk2, Vinf)
)

    # 3) Resolve o sistema
    strengths = np.linalg.solve(A, b)
    print("Solução unknowns = [λ₁, λ₂, ..., Γ]:")
    print(strengths)

    return strengths


def computeTangentVelocityVortex(unknowns, panel_list: list[Panel], Vinf: Velocity):

    N = len(panel_list)
    lambdas = unknowns[:N]
    gamma = unknowns[N]

    Vt = np.zeros(N, dtype=float)

    for i in range(N):

        ti = panel_list[i].tangent_vector
        #ti = Vector(-ti.x, -ti.y)
        Vinf_ti = escalarProduct2(ti, Vinf)
        sum_vor = 0
        sum_fon = 0

        for j in range(N):

            Vij_fon = computeVelocityComponent(panel_list[i], panel_list[j])
            Vtij_fon = escalarProduct2(ti, Vij_fon)

            sum_fon += Vtij_fon*lambdas[j]

            Vij_vor = computeVelocityComponent2(panel_list[i], panel_list[j])
            Vtij_vor = escalarProduct2(ti, Vij_vor)
            sum_vor += Vtij_vor
        
        Vt[i] = sum_fon + sum_vor*gamma + Vinf_ti
        print(f"Painel {i}: Vt = {Vt[i]:.4f}, Vinf_ti = {Vinf_ti:.4f}, soma fontes = {sum_fon:.4f}, soma vortice = {sum_vor*gamma:.4f}")


    return Vt