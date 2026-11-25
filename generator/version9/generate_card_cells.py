import pandas as pd

# im finding the cells of each card by rotating and translating according to the certificate. however i also translate after this to make sure 
# all cells are moved to the "board"

BASE_CARDS = {

    0 : [(1,0), (2,0), (3,0), (3,1), (4,1)],
    1 : [(0,0), (2,0), (3,0), (3,1), (4,1)],
    2 : [(0,0), (1,0), (3,0), (3,1), (4,1)],
    3 : [(0,0), (1,0), (2,0), (3,1), (4,1)],
    4 : [(0,0), (1,0), (2,0), (3,0), (4,1)],
    5 : [(0,0), (1,0), (2,0), (3,0), (3,1)],
    6 : [(0,0), (1,0), (2,0), (3,0), (3,1), (4,1)]

}

CHAR_TO_INT = {

    "0" : 0,
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "A" : 10,
    "B" : 11,
    "C" : 12,
    "D" : 13,
    "E" : 14,
    "F" : 15,
    "G" : 16

}

INT_TO_CHAR = {

    0 : "0",
    1 : "1",
    2 : "2",
    3 : "3",
    4 : "4",
    5 : "5",
    6 : "6",
    7 : "7",
    8 : "8",
    9 : "9",
    10 : "A",
    11 : "B",
    12 : "C",
    13 : "D",
    14 : "E",
    15 : "F",
    16 : "G"

}

# transform a given cell

def R(ind, cell, tx, ty):

    (x,y) = cell
    new_cell = None

    if ind == 0:

        new_cell = (x + tx, y + ty)

    elif ind == 1:

        new_cell = (y + tx, x + ty)

    elif ind == 2:
    
        new_cell = (-x + tx, y + ty)

    elif ind == 3:
    
        new_cell = (y + tx, -x + ty)

    elif ind == 4:
    
        new_cell = (x + tx, -y + ty)

    elif ind == 5:
    
        new_cell = (-y + tx, x + ty)

    elif ind == 6:

        new_cell = (-x + tx, -y + ty)

    elif ind == 7:
    
        new_cell = (-y + tx, -x + ty)

    return new_cell

# transform a given basis

def transform(ind, tx, ty, card):

    trans_card = []

    for cell in card:

        trans_card.append(R(ind, cell, tx, ty))

    return trans_card

# getting all the cards from h2_combos.csv file

def get_construct_list():

    df = pd.read_csv("generator/version9/h2_combos.csv")

    construct_list = df['construction'].to_list()

    return construct_list

# i had a problem with some cells having negative components so this method was
# used to do sanity checks

def check_cells(card_num , cell_list):

    for (x, y) in cell_list:

        assert x >= 0, f"x for {card_num} was negative"
        assert y >= 0, f"y for {card_num} was negative"

# used to translate all the cells in A_i and T_i, intersection of A_i, 
# A and T together to make sure the general shape is maintained and that
# the cells did not have negative components

def translate_cells(card_num, a1, a2, t1, t2, ia, a, t):

    cell_list = a + t

    x_t = min(x for (x,_) in cell_list)
    y_t = min(y for (_,y) in cell_list)


    if x_t < 0:

        x_t = abs(x_t)

    else:

        x_t = -abs(x_t)


    if y_t < 0:
    
        y_t = abs(y_t)
    
    else:
    
        y_t = -abs(y_t)

    a1_trans = transform(0, x_t, y_t, a1)
    a2_trans = transform(0, x_t, y_t, a2)
    t1_trans = transform(0, x_t, y_t, t1)
    t2_trans = transform(0, x_t, y_t, t2)
    ia_trans = transform(0, x_t, y_t, ia)
    a_trans = transform(0, x_t, y_t, a)
    t_trans = transform(0, x_t, y_t, t)

    check_cells(card_num, a1_trans)
    check_cells(card_num, a2_trans)
    check_cells(card_num, t1_trans)
    check_cells(card_num, t2_trans)
    check_cells(card_num, ia_trans)
    check_cells(card_num, a_trans)
    check_cells(card_num, t_trans)

    return [a1_trans, a2_trans, t1_trans, t2_trans, ia_trans, a_trans, t_trans]

# transform each cell list to a string

def create_cell_str(cell_list):

    cell_str = ""

    for (x,y) in cell_list:

        cell_str += INT_TO_CHAR[x] + INT_TO_CHAR[y] + " "

    return cell_str

# use a given card from h2_combos.csv and transform it and return a string of cells

def find_card_cells(card_str):

    card_list = card_str.split()

    assert len(card_list) == 3

    card_num = int(card_list[0])

    assert len(card_list[1]) == 5

    base1 = BASE_CARDS[int(card_list[1][0])]

    assert len(card_list[2]) == 5

    base2 = BASE_CARDS[int(card_list[2][0])]

    snaky = BASE_CARDS[6]

    r1 = int(card_list[1][2])
    r2 = int(card_list[2][2])

    x1 = CHAR_TO_INT[card_list[1][3]]
    x2 = CHAR_TO_INT[card_list[2][3]]

    y1 = CHAR_TO_INT[card_list[1][4]]
    y2 = CHAR_TO_INT[card_list[2][4]]

    a1_trans = transform(r1, x1, y1, base1)
    a2_trans = transform(r2, x2, y2, base2)
    t1_trans = transform(r1, x1, y1, snaky)
    t2_trans = transform(r2, x2, y2, snaky)

    inter_a_trans = [c for c in set(a1_trans) & set(a2_trans)]
    a_trans = [c for c in set(a1_trans + a2_trans)]
    t_trans = [c for c in set(t1_trans + t2_trans)]

    trans_list = translate_cells(card_num, a1_trans, a2_trans, t1_trans, t2_trans, inter_a_trans, a_trans, t_trans)

    row = [str(card_num)]

    for i in range(7):

        row.append(create_cell_str(trans_list[i]))

    return row

#  main method of this script to find the cells of A_i, T_i, intersection of A
#  A, and T for each card in h2_combos.csv. transferred data to a dataframe
#  and then saved df to a csv file

def get_data():

    construct_list = get_construct_list()

    data = []

    for c in construct_list:

        data.append(find_card_cells(c))

    cell_df = pd.DataFrame(data=data, columns=["card", "A1", "A2", "T1", "T2", "inter_A", "A", "T"])

    cell_df.to_csv("generator/version9/generated_A_T_cells.csv")