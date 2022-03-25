import numpy as np

def north_west(sup, dem):
    supply = sup[:]
    demand = dem[:]
    m = len(supply) - 1
    n = len(demand) - 1

    res = [["-" for _ in range(n + 1)] for __ in range(m + 1)]

    i, j = 0, 0
    # i = række "supply"
    # j = kolonne "demand"
    while (not(i == m + 1 and j == n) and not(i == m and j == n + 1)):
        x = min(supply[i], demand[j])
        supply[i] -= x
        demand[j] -= x
        res[i][j] = x
        if demand[j] > 0:
            i += 1
        else:
            j += 1

    return res



def kant_finder(data, type = True):
    ls = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if type:
                if data[i][j] != "-":
                    ls.append((i, j))
            else:
                if data[i][j] == "-":
                    ls.append((i, j))
    return ls



def cykel(data, start, pos, rat = -1):
    """"
    if rat = 1 then row wise else -1 then column wise
    """
    ls = ["start"]
    nx_rat = -1 * rat

    i, j = pos

    jav = data[:]

    for k in range(len(w := data[i])):
        kand = w[k]
        if (kand != "-" and kand != "m" and k != j):

            if rat == 1:
                ls.append((k, i))
            else:
                ls.append((i, k))

            if ls[-1] != start:
                cykel(data.T, start, (int(k), int(i)), nx_rat)

    ss1 = sum(1 for ku in data[i] if ku != "-")
    ss2 = sum(1 for ku in data[:, j] if ku != "-")

    ss = min(ss1, ss2)

    if ss < 2:
        jav[i][j] = "-"

    return jav


def negatives(ls, cost, pos):
    def cykel_finder(ls, pos):
        obs = [pos]
        ls.remove(pos)
        rat = 0
        nex = pos
        for _ in range(len(ls)):
            x = nex[rat]
            nex = [par for par in ls if par[rat] == x][0]
            ls.remove(nex)
            obs.append(nex)
            rat = 1 if rat == 0 else 0
        return obs
    ss = 0
    ls = cykel_finder(ls, pos)

    print("Edges:", end = " ")
    j = 0
    for pp in ls:
        if j % 2:
            ss -= cost[pp[0]][pp[1]]
            print(f"-{pp}", end = "")
        else:
            ss += cost[pp[0]][pp[1]]
            print(f"+{pp}", end = "")
        j += 1
    print()

    print("Value:", end = " ")
    j = 0
    for pp in ls:
        if j % 2:
            print(f"-{cost[pp[0]][pp[1]]}", end = "")
        else:
            print(f"+{cost[pp[0]][pp[1]]}", end = "")
        j += 1
    print(f"={ss}")
    return ls, ss



def cheap_scape(data, cost):
    optimal = data.copy()
    while True:
        possible_m = kant_finder(optimal, type = False)
        for pos in possible_m:
            vej = optimal.copy()
            vej[pos[0]][pos[1]] = "m"
            cc = cykel(vej, pos, pos)
            print()
            print(cc)
            kant = kant_finder(cc)
            ls, er_kanten_bedre = negatives(kant, cost, pos)
            if er_kanten_bedre < 0:
                print()
                print("Better edge found. Rerunning the stepping-stone:")
                max_val = min([int(optimal[sec[0]][sec[1]]) for sec in ls[1::2]])

                checker = True

                for sec in ls[1::2]:
                    optimal[sec[0]][sec[1]] = int(optimal[sec[0]][sec[1]]) - max_val
                    if (int(optimal[sec[0]][sec[1]]) == 0 and checker):
                        optimal[sec[0]][sec[1]] = '-'
                        checker = False

                optimal[ls[0][0]][ls[0][1]] = max_val
                for sec in ls[2::2]:
                    optimal[sec[0]][sec[1]] = int(optimal[sec[0]][sec[1]]) + max_val

                print("New solution:")
                print(optimal)
                break
        else:
            break

    print()
    print("Optimal solution found:")
    print(optimal)

    return optimal

def north_west_and_step(supply, demand, costs):
    res = north_west(supply, demand)
    print("Northwest rule find:", "\n")
    for i in range(len(res)):
        for j in res[i]:
            print(j, end = " ")
        print("|", supply[i])
    print("-"*(len(res[0]*2) + 4))
    for i in demand:
        print(i, end = " ")
    print()

    res = np.array(res)
    costs = np.array(costs)

    op = cheap_scape(res, costs)

    print()
    print("cost of this is:")
    print(np.sum(np.array(op) * np.arry(costs)))

    return ""
