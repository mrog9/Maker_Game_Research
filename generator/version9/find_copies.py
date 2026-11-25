import pandas as pd

#  this was used to set me up for my second pruning method. for this script i am tracking each card in unique_cards.csv
#  and its "parent" which shares the same T and an overlapping intersection of A_i. I then stored this overlap as possible pivots

def find_copies():

    df = pd.read_csv("generator/version9/unique_cards.csv")

    # index 0 is the identity, so the pivots found here are in card i's own
    # frame, the same frame as its A, T and inter_A columns
    cols_ia = ["A_inter_0", "A_inter_1", "A_inter_2", "A_inter_3", "A_inter_4", "A_inter_5", "A_inter_6", "A_inter_7"]
    cols_a = ["A_0", "A_1", "A_2", "A_3", "A_4", "A_5", "A_6", "A_7"]
    cols_t = ["T_0", "T_1", "T_2", "T_3", "T_4", "T_5", "T_6", "T_7"]

    unique_strategies = []

    a_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_a}
    t_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_t}
    ia_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_ia}

    a0_sets = a_sets[cols_a[0]]
    t0_sets = t_sets[cols_t[0]]
    ia0_sets = ia_sets[cols_ia[0]]

    for i in range(len(df)):

        a0_item = a0_sets[i]
        t0_item = t0_sets[i]
        ia0_item = ia0_sets[i]
        copy_list = []

        for j in range(len(cols_a)):

            a_comp = a_sets[cols_a[j]]
            t_comp = t_sets[cols_t[j]]
            ia_comp =ia_sets[cols_ia[j]]

            for k in range(i+1, len(df)):

                if t0_item == t_comp[k] and len(ia0_item & ia_comp[k])>0:

                    copy_list.append({str(k): ia0_item & ia_comp[k]})


        if len(copy_list) > 0:

            unique_strategies.append({str(i): copy_list})

    data = []

    for us in unique_strategies:

        for k1, v1 in us.items():

            for d in v1:

                for k2, v2 in d.items():

                    p_str = ""

                    for p in v2:

                        p_str += p + " "

                    row =[k2, k1, p_str]
                    data.append(row)

    new_df = pd.DataFrame(data=data, columns=["card", "parent_copy", "pivots"])

    new_df.to_csv("generator/version9/copies.csv")

