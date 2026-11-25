import pandas as pd

# would set one card to its identity transform and then from the next card to the end of df I would 
# check to see if the original card matched any of the other cards in a certain transformation.
# i did this for A, T, and intersection of A. if there was a match between all these categories, then
#  i would store the index of the second card so that i can keep the orignial and remove the second one

def remove_duplicates():

    df = pd.read_csv("generator/version9/card_A_T_transforms.csv")

    # index 0 is the identity, so each card is compared in its own frame
    # against all 8 transforms of the later cards
    cols_ia = ["A_inter_0", "A_inter_1", "A_inter_2", "A_inter_3", "A_inter_4", "A_inter_5", "A_inter_6", "A_inter_7"]
    cols_a = ["A_0", "A_1", "A_2", "A_3", "A_4", "A_5", "A_6", "A_7"]
    cols_t = ["T_0", "T_1", "T_2", "T_3", "T_4", "T_5", "T_6", "T_7"]

    # remove_inds_A = set()
    # remove_inds_T = set()
    # remove_inds_A_inter = set()

    remove_inds = []

    a_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_a}
    t_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_t}
    ia_sets = {c: [frozenset(x.split()) for x in df[c]] for c in cols_ia}

    a0_sets = a_sets[cols_a[0]]
    t0_sets = t_sets[cols_t[0]]
    ia0_sets = ia_sets[cols_ia[0]]

    print(f"there is {len(df)} number of entries in dataframe")

    for i in range(len(df)):

        a_item = a0_sets[i]
        t_item = t0_sets[i]
        ia_item = ia0_sets[i]

        for j in range(len(cols_a)):

            a_comp = a_sets[cols_a[j]]
            t_comp = t_sets[cols_t[j]]
            ia_comp = ia_sets[cols_ia[j]]
            flag=False

            for k in range(i+1, len(df)):

                if a_item == a_comp[k] and t_item == t_comp[k] and ia_item == ia_comp[k]:

                    remove_inds.append(k)

        if i%1000 == 0:

            print(i)

    # remove_inds = remove_inds_A & remove_inds_T & remove_inds_A_inter
    # remove_inds = remove_inds_T & remove_inds_A

    df = df.drop(remove_inds).reset_index(drop=True)

    df.to_csv("generator/version9/unique_cards.csv")