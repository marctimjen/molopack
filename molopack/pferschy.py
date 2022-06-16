import numpy as np
import pulp as PLP

def pferschy(cost_matrix):

    n = len(cost_matrix)

    # Minimeringsproblem
    Model = PLP.LpProblem("Simon_and_Garfinkel", PLP.LpMinimize)

    # Heltallige beslutningsvariable x(i,j)
    x = PLP.LpVariable.dicts("x", (range(n), range(n)), 0, 1, PLP.LpInteger) # x(0,0) .. x(n,n)

    # Objektfunktion
    Model += PLP.lpSum([cost_matrix[i][j] * x[i][j] for i in range(n)
                        for j in range(n)]), "Objektfunktion"

    # Outflow:
    for i in range(n):
        Model += PLP.lpSum([x[i][j] for j in range(n)]) == 1, f"Outflow({i})"

    # Inflow:
    for j in range(n):
        Model += PLP.lpSum([x[i][j] for i in range(n)]) == 1, f"Inflow({j})"


    # Løsning af modellen vha. PuLP's valg af Solver

    # Print af løsningens status
    #print("Status:", PLP.LpStatus[Model.status])

    # Print af hver variabel med navn og løsningsværdi

    første = True
    while første or len(res) != 1: # Stopper når der kun er en tur rundt.
        første = False

        Model.solve()
        res = []

        kanter = []
        for v in Model.variables():
            if v.varValue > 0:
                #print(v.name, "=", v.varValue)
                kanter.append(tuple(map(int, v.name.split("_")[1:3])))

        subture = []
        #tur = [kanter[0]]
        for pot_tur in kanter: # Finder de subturene, som eksisterer i grafen.
            # efter dette bliver subture fx lig:
            # [[(0, 6), (6, 7), (7, 5), (5, 4), (4, 0)], [(1, 3), (3, 2), (2, 1)]]
            if not any(pot_tur in subtur for subtur in subture):
                tmp_subtur = [pot_tur]
                kant = kanter[tmp_subtur[-1][1]]
                g_lng = len(tmp_subtur)
                while True:
                    if kant != tmp_subtur[-1] and kant != tmp_subtur[0]:
                        tmp_subtur.append(kant)
                        kant = kanter[tmp_subtur[-1][1]]

                    if len(tmp_subtur) == g_lng:
                        break
                    g_lng = len(tmp_subtur)
                subture.append(tmp_subtur)

        for subtur in subture:
            # Finder de punkter der besøges i subturene.
            # fx. [[0, 6, 7, 5, 4], [1, 3, 2]]
            res1 = []
            for kant in subtur:
                a, b = kant
                if res1 == []:
                    res1.append(a)
                if b != res1[0]:
                    res1.append(b)
            res.append(res1)

        print([[1 + i for i in indre_liste] for indre_liste in res], PLP.value(Model.objective))

        for S in res: # Gå gennem hver subtur
            Model += PLP.lpSum([x[i][j] for i in S for j in S]) <= len(S) - 1
            # tilføjer en SEC pr subtur. Her tvinger vi antallet af kanter til at være
            # antal punkter -1. Dette vil ødelægge denne subtur.

    #print(f"subture: {res} (nul indexeret)")

    # Print af den optimale objektfunktionsværdi
    #print("Obj. = ", PLP.value(Model.objective))
    return [[1 + i for i in indre_liste] for indre_liste in res], PLP.value(Model.objective)
