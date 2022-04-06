def minimal_cover(ls, val, printer = False):
    ls = sorted(ls)
    min_cov = []
    j = -1
    for i in ls:
        if i < val:
            min_cov.append(i)
            j += 1
        else:
            print("NO minimal cover may be found")
            print(f"{i} value bigger than knapsack size {val}")
            break

        if (val - sum(min_cov)) < 0:
            break

    if printer:
        print("The minimal cover is:")
        for i in range(0, len(min_cov)):
            print(f"{min_cov[i]}*d{i+1}", end = " + ")
        print(f"0 <= {val}")

        for i in range(0, len(min_cov)):
            print(f"1*d{i+1}", end = " + ")
        print(f"0 <= {j}", end = "\n\n")



    return j, min_cov


def padberg(ls, val, printer = False):
    ls = sorted(ls)

    if printer:
        print("The given knapsack inequality:")
        for i in range(len(ls)):
            print(f"{ls[i]}*d{i+1}", end = " + ")
        print(f"0 <= {val}", end = "\n\n")
        step = 0

    j, min_cov = minimal_cover(ls, val, printer)
    nr = len(min_cov) - 1
    coef = [1 for i in range(len(min_cov))]
    for i in range(j + 1, len(ls)):
        bound = val - ls[i]
        optimal = 0
        for k in min_cov:
            if bound - k >= 0:
                optimal += 1
                bound = bound - k
            else:
                break
        coef.append(nr - optimal)

        if printer:
            step += 1
            print(f"Padberg step {step}:")
            for (j, i) in zip(coef, range(1, len(coef) + 1)):
                print(f"{j}*d{i}", end = " + ")
            print(f"0 <= {nr}")
            for (j, i) in zip(ls, range(1, len(ls[:i]) + 1)):
                print(f"{j}*d{i}", end = " + ")
            print(f"0 <= {val}", end = "\n\n")

    if printer:
        print("Thus the LCI becomes:")
        for (j, i) in zip(coef, range(1, len(coef) + 1)):
            print(f"{j}*d{i}", end = " + ")
        print(f"0 <= {nr}")
        for (j, i) in zip(ls, range(1, len(ls) + 1)):
            print(f"{j}*d{i}", end = " + ")
        print(f"0 <= {val}")

    return ls, coef
