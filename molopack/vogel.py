import numpy as np

def vogel(S, T, costs):

    def nan_gen(it, obj):
        ls = np.array([])
        j = 0
        for i in range(len(it)):
            if it[i]:
                ls = np.append(ls, obj[j])
                j += 1
            else:
                ls = np.append(ls, np.nan)
        return ls

    s = [True for _ in range(len(S))]
    t = [True for _ in range(len(T))]

    sup = np.array(S)
    tar = np.array(T)
    cost = np.array(costs)
    out = np.array([[0 for _ in range(sum(t))] for __ in range(sum(s))])


    while((sum(s) >= 2) and (sum(t) >= 2)):
        cst = cost[s][..., t]
        sorted = np.sort(cst, axis = 1)
        diff_r = sorted[..., 1] - sorted[..., 0]
        sorted = np.sort(cst, axis = 0)
        diff_c = sorted[1] - sorted[0]

        d_r = nan_gen(s, diff_r)
        d_c = nan_gen(t, diff_c)

        diff = [d_r, d_c]

        m = map(np.nanmax, diff)

        if next(m) >= next(m): # if a diff on supply is larger than on demand
            idx_r = np.nanargmax(d_r)
            idx_c = np.nanargmin(nan_gen(t, cost[idx_r, t]))
            send = min([sup[idx_r], tar[idx_c]])
            out[idx_r, idx_c] = send

            sup[idx_r] = sup[idx_r] - send
            tar[idx_c] = tar[idx_c] - send
        else:
            idx_c = np.nanargmax(d_c)
            idx_r = np.nanargmin(nan_gen(s, cost[s, idx_c]))
            send = min([sup[idx_r], tar[idx_c]])
            out[idx_r, idx_c] = send

            sup[idx_r] = sup[idx_r] - send
            tar[idx_c] = tar[idx_c] - send


        for i in range(len(sup)):
            if sup[i] == 0:
                s[i] = False

        for i in range(len(tar)):
            if tar[i] == 0:
                t[i] = False


    flag = False
    if sum(sup != 0) != 1:
        flag = True
        sup, tar = tar, sup
        cost = cost.T
        out = out.T
        t, s = s, t

    idx_r = np.where(sup != 0)

    for i in range(sum(tar != 0)):
        idx_c = np.nanargmin(nan_gen(t, cost[idx_r, t][0]))
        send = min([sup[idx_r], tar[idx_c]])
        out[idx_r, idx_c] = send

        sup[idx_r] = sup[idx_r] - send
        tar[idx_c] = tar[idx_c] - send

        for i in range(len(tar)):
            if tar[i] == 0:
                t[i] = False

    if flag:
        out = out.T
        cost = cost.T

    print("Vogels approximation:")
    print(out)

    print()
    print("Cost of this is:")
    print(np.sum(np.array(out) * np.array(cost)))

    return out
