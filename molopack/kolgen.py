import os

def kolonne_generering(wides, demand, C, ms, kg, max_iterationer=10, start_kol=False):
    sol_dicts = []
    obj = 2
    iteration = 0
    while iteration < max_iterationer:
        print(f"{iteration=}")
        #Master
        n_rolls = [ C//x for x in wides]
        print(f"{n_rolls=}")
        master_string = "Minimize\n"                                            # Minimize
        g_liste = [f"g{x}" for x in range(1,len(demand)+1+iteration)]
        g_string = " + ".join(g_liste) + "\nSubject To\n"                       # g1 + g2 + g3 + g4
                                                                                # Subject To
        left_ineq = [f"{n} {g}" for n,g in zip(n_rolls, g_liste)]

        for i in range(iteration):                                              # + 2 g5
            dic = sol_dicts[i]
            for j in range(0,len(left_ineq)):
                if val := dic.get(str(j+1)):
                        left_ineq[j] += f" + {val} {g_liste[len(left_ineq)+i]}"

        right_ineq = [f" >= {d}\n" for d in demand]
        ineq_string = "".join([l + r for l, r in zip(left_ineq, right_ineq)])   # 2 g1 >= 20
                                                                                # 4 g2 >= 31
                                                                                # 5 g3 >= 27
                                                                                # 6 g4 >= 23
        master_string += g_string + ineq_string + "End"                         # End
        master_name = f"CS-MasterLP-{iteration+1}.lp"
        print()
        print(master_name)
        print(master_string)

        f = open(master_name, "x")
        f.write(master_string)
        f.close()

        #Kør Master
        master = ms(master_name)

        linje = 1
        dual_vals = []
        while (val := master[::-1][linje].split()[1]) != "Name":
            dual_vals.append(val)
            linje += 1
        dual_vals .reverse()

        #KolGen

        ax_liste = [f"a{x+1}" for x in range(len(dual_vals))]
        kol_gen_string = "Maximize\n"                                           # Maximize

        dual_liste = [f"{dual} {a}" for dual, a in zip(dual_vals, ax_liste)]
        ax_string = " + ".join(dual_liste) + "\nSubject To\n"                   # 0.5000 a1 + 0.2500 a2 + 0.2000 a3 + 0.1667 a4
                                                                                # Subject To
        ineq_liste = [f"{w} {a}" for w, a in zip(wides, ax_liste)]
        kol_ineq_string = " + ".join(ineq_liste) + f" <= {C}\n"                 # 7 a1 + 5 a2 + 4 a3 + 3 a4 <= 20
        general_string = "General\n" + "\n".join(ax_liste) + "\nEnd"            # General
                                                                                # a1
                                                                                # a2
                                                                                # a3
                                                                                # a4
                                                                                # End
        kol_gen_string += ax_string + kol_ineq_string + general_string

        kol_gen_name = f"CS-KolGen-{iteration+1}.lp"
        print()
        print(kol_gen_name)
        print(kol_gen_string)

        f = open(kol_gen_name, "x")
        f.write(kol_gen_string)
        f.close()

        #kør KolGen
        kol_gen = kg(kol_gen_name)

        for string in kol_gen :
            if "Objective =" in string:
                print("obj:", obj :=float(string.split()[-1]), "\n")
        if obj <= 1:
            break

        linje = 2
        sol_vars = {}
        while (sol_var := kol_gen[::-1][linje].split())[0][0] == 'a':
            sol_vars[sol_var[0][1:]] = sol_var[1].split(".")[0]
            linje  += 1
        sol_dicts.append(sol_vars)
        iteration += 1
    i = 0
    print("Løsning:")
    while (var := master[::-1][i].split())[0:2] != ['CPLEX>', 'Variable'] or i == 20:
        if var[0][0] == "g":
            print(": ".join(var))
        i += 1
