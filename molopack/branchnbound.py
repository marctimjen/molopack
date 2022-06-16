import numpy as np
import pandas as pd

#gør at matricerne bliver printet nice, men laver permanent om på dine numpy indstillinger, så husk at ændre det tilbage
# pd.set_option('precision', 0)
np.set_printoptions(suppress=True)
np.set_printoptions(suppress=False)

# Lånt fra Jens visual basic kode
def beregn_reduceret_matrix(OG_matrix, branch_list=[]):
    n = len(OG_matrix)

    # 1-indeksering og kopiere den originale matrice
    reduced_matrix = np.hstack((np.repeat(999, n + 1)[:, np.newaxis],
                                np.vstack((np.repeat(999, n), OG_matrix))))

    # det er det de kalder mig
    big_m = OG_matrix[1][1]

    prev_city = {}
    next_city = {}

    for branch in branch_list:
        from_city = branch[0]
        to_city = branch[1]

        if to_city > 0:  # hvis vi SKAL gå til kanten
            # kanten (from_city, to_city) skal benyttes i løsningen
            prev_city[to_city] = from_city
            next_city[from_city] = to_city

            # eliminer alle andre kanter til to_city
            for i in range(1, n + 1):
                if i != from_city:
                    reduced_matrix[i][to_city] = big_m

            # eliminer alle andre kanter til from_city
            for j in range(1, n + 1):
                if j != to_city:
                    reduced_matrix[from_city][j] = big_m

        else:  # hvis vi IKKE MÅ gå til kanten
            reduced_matrix[from_city][-to_city] = big_m

    # forbyd kanten fra sidste til første by i hver krævet sti
    for start_city in range(1, n + 1):
        if prev_city.get(start_city, 0) == 0 and next_city.get(start_city, 0) > 0:
            end_city = next_city.get(start_city)
            while next_city.get(end_city, 0) > 0:
                end_city = next_city.get(end_city)
            reduced_matrix[end_city][start_city] = big_m

    # gennemfør herefter reduktionen
    total_reduction = 0
    for i in range(1, n + 1):
        this_reduction = min(reduced_matrix[i])
        for j in range(1, n + 1):
            reduced_matrix[i][j] = reduced_matrix[i][j] - this_reduction
        total_reduction += this_reduction

    for j in range(1, n + 1):
        this_reduction = min(reduced_matrix[:, j])
        for i in range(1, n + 1):
            reduced_matrix[i][j] = reduced_matrix[i][j] - this_reduction
        total_reduction += this_reduction

    #fjerner 1-indeksering
    reduced_matrix = np.delete(np.delete(reduced_matrix, 0, 0), 0, 1)
    return reduced_matrix, total_reduction

def straf_matrix(reduced_matrix):
    # det hele forklarer lidt sig selv
    n = len(reduced_matrix)
    svar_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if reduced_matrix[i][j] == 0:
                min_row = min(reduced_matrix[i][np.arange(len(reduced_matrix)) != j])
                min_column = min(reduced_matrix[:, j][np.arange(len(reduced_matrix)) != i])
                svar_matrix[i][j] = min_row + min_column

    return svar_matrix

def print_table(reduceret_matrix):

    def color_red(val):  # vi maler byen rød
        color = 'red' if val > 500 else ''  # dog kun hvis den er større end 500
        return 'background-color: %s' % color

    n = len(reduceret_matrix[0])

    # 1-indeksere vores udskrift
    pd_df = pd.DataFrame(reduceret_matrix[0],
                         columns=list(range(1,n + 1)),
                         index = list(range(1, n + 1)))

    print(f"Total reduktion: {reduceret_matrix[1]}")
    return pd_df.style.applymap(color_red) # vi applyer Birthe Kjær til matricen

def print_straf_table(straf_matrix):  # Total original kode

    matrix, (t, f) = straf_matrix
    print("Straf Matrix:")

    def style_specific_cell(x):  # vi gør punkt (t,f) grønt
        color = 'background-color: green'
        df1 = pd.DataFrame('', index=x.index, columns=x.columns)
        df1.iloc[t, f] = color
        return df1

    n = len(matrix)

    # 1-indeksere vores udskrift
    pd_df = pd.DataFrame(matrix,
                         columns=list(range(1,n + 1)),
                         index = list(range(1, n + 1)))

    return pd_df.style.apply(style_specific_cell, axis=None)  # smid den på matricen

def branch_and_bound(matrix, must_end_at=None):


    branch_costs = []  # liste til alle de branches vi støder på
    costs = []         # liste med costs, den sidste vil altid være den bedste
    reds = []          # liste med de reducerede matricer, den sidste vil altid være den bedste

    def solve(matrix, branch_list=[]):

        # danner den reducerede matrice og straf matricen
        red_matrix, cost = beregn_reduceret_matrix(matrix, branch_list)
        straf = straf_matrix(red_matrix)

        # vi gemmer resultaterne
        reds.append(red_matrix)
        costs.append(cost)

        # output nogle resultater
        print(f"{branch_list=}")
        display(print_table((red_matrix, cost)))


        if must_end_at:
            # vi sørger for at vi ikke ser på den søjle vi skal slutte i
            tmp_straf = straf[:, [i for i in range(len(straf)) if i != (must_end_at - 1)]]

            kant = np.where(tmp_straf == tmp_straf[tmp_straf < 800].max())
            f = kant[0][0] + 1 # fra kant
            t = kant[1][0] + 1 # til kant

            # hvis vi ligger efter den søjle vi skal slutte i, bliver vi nødt til at ligge 1 til søjle indekset
            if t >= must_end_at:
                t += 1

        else:
            kant = np.where(straf == straf[straf < 800].max())
            f = kant[0][0] + 1  # fra kant
            t = kant[1][0] + 1  # til kant

        # vi gemmer den "venstre" branch, i tilfælde af at den optimale løsning ikke bare direkte til højre
        # vi ved allerede nu at cost af denne gren bliver (straf[f - 1][t - 1] + cost)
        branch_costs.append(((straf[f - 1][t - 1] + cost), branch_list + [(f, -1 * t)]))

        # vi undgår at vise den allersidste straf matrice
        if straf[f - 1][t - 1] != 0:
            display(print_straf_table((straf, (f-1, t-1))))

        # Vi stopper hvis vi finder en fuld løsning og der ikke er findes en lavere cost
        if np.all(straf[straf < 800] == 0) and cost <= min(branch_costs, key=lambda x: x[0])[0]:
            return

        else:
            # hvis vores cost er den laveste fortsætter vi "blindt" til højre i træet
            if cost <= min(branch_costs, key=lambda x: x[0])[0]:
                solve(matrix, branch_list + [(f, t)])  # Now do it again

            else:  # vores cost var shit, så vi går tilbage til tidligere branch muligheder og kigger dem igennem
                # vi skal lige huske at gemme det branch vi står, i tilfælde at de andre ruter også er trash
                branch_costs.append((cost, branch_list))

                # vi vælger den bedste branch tilgængelig
                h_branch = branch_costs.pop(branch_costs.index(min(branch_costs, key=lambda x: x[0])))
                solve(matrix, h_branch[1])

    solve(matrix)

    res = np.argwhere(reds[-1] == 0)  # vi finder alle indekserne på alle 0 i vores løsning

    return list(map(lambda x: (x[0]+1, x[1]+1), res)), costs[-1]
