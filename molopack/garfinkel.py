import numpy as np
import pulp as PLP
from copy import deepcopy

#funktion til at opstille modellen.

def the_sound_of_silence(cost_matrix):
    """
        Denne funktion returnerer den bedste mulige løsning af subture problemet.

        res = de ture som en kan tage
        PLP.value(Model.objective) = den objective værdi ved den optimale løsning
    """

    n = len(cost_matrix)

    # Minimeringsproblem
    Model = PLP.LpProblem("Simon_and_Garfinkel", PLP.LpMinimize)

    # Heltallige beslutningsvariable x(i,j)
    x = PLP.LpVariable.dicts("x", (range(n), range(n)), 0, 1, PLP.LpContinuous) # x(0,0) .. x(n,n)

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
    Model.solve()

    # Print af løsningens status
    # print("Status:", PLP.LpStatus[Model.status])

    # Print af hver variabel med navn og løsningsværdi

    kanter = []
    for v in Model.variables():
        if v.varValue > 0:
            #print(v.name, "=", v.varValue)
            kanter.append(tuple(map(int, v.name.split("_")[1:3])))
    subture = []
    #tur = [kanter[0]]
    for pot_tur in kanter:
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

    res = []
    for subtur in subture:
        res1 = []
        for kant in subtur:
            a, b = kant
            if res1 == []:
                res1.append(a)
            res1.append(b)
        res.append(res1)

    #print(f"subture: {res} (nul indexeret)")

    # Print af den optimale objektfunktionsværdi
    #print("Obj. = ", PLP.value(Model.objective))
    return res, PLP.value(Model.objective)

#garfinkels metode
def simon_n_garfinkel(matrix, m=999):
    n = len(matrix)

    start_gren = (the_sound_of_silence(matrix), [0]) # Finder optimal setting med subture

    print_gren = [[1 + i for i in indre_liste] for indre_liste in start_gren[0][0]]

    print(f"P(0): subture={print_gren}, obj={start_gren[0][1]}")

    matrix_liste = [(start_gren, matrix)]
    bedste_rute = ([0]*n, 999)
    max_P = 0
    while True:
        #BBS
        ((subture, obj), P), matrix = matrix_liste.pop(matrix_liste.index(min(matrix_liste, key=lambda x: x[0][0][1])))

        #BFS
        #((subture, obj), P), matrix = matrix_liste.pop(0)

        #hvis der er 2 ellere flere subture
        if len(subture) != 1:
            korteste_subtur = subture.pop(np.argmin([len(subtur) for subtur in subture]))
            rest_kanter = [i for sublist in subture for i in sublist]
            coord_lister = []

            for i in range(1, len(korteste_subtur)):
                andre_ture = korteste_subtur[0:i][:-1]

                #vi finder alle de kanter de "andre" ture ikke må gå til
                kanter = [(i, j) for i in andre_ture for j in rest_kanter]
                main_kant = korteste_subtur[0:i][-1]
                coord_liste = [*kanter]

                # vi finder de kanter "main" kanten ikke må gå til
                coord_liste += [(main_kant, i) for i in range(n) if i not in rest_kanter]

                coord_lister.append(coord_liste)


            tæller = 0
            for coord_liste in coord_lister:
                test = deepcopy(matrix)
                for coord in coord_liste:
                    test[coord[0]][coord[1]] = m
                #print(test)
                tæller += 1
                gren = (the_sound_of_silence(test), P + [max_P + tæller])
                print_gren = [[1 + i for i in indre_liste] for indre_liste in gren[0][0]]
                print(f"P{tuple(P + [max_P + tæller])}: subture={print_gren}, obj={gren[0][1]}")
                matrix_liste.append((gren, test))

            max_P = max_P + tæller
        if len(subture[0]) == n+1 and obj < bedste_rute[1]:
            bedste_rute = (subture[0], obj)

        if bedste_rute[1] < min([l[0][0][1] for l in matrix_liste]):
            print_gren = [1 + i for i in bedste_rute[0]]
            return (print_gren, bedste_rute[1])
