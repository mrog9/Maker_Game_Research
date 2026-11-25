import pandas as pd

# eventually i need to see if a card "shape" is the same even after a transformation.
# so for each card i went through all possible rotations and then i translated the cells
# to make sure it was as close to the bottom left of the board as possible (in the positive region)

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

#  cell transform

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

# transform a list of cells

def find_transform(r, tx, ty, cell_list):

    trans_cell_list = []

    for c in cell_list:

        trans_cell_list.append(R(r, c, tx, ty))

    return trans_cell_list

#  convert cell list to a string

def create_cell_str(cell_list):

    cell_str = ""

    for (x,y) in cell_list:

        cell_str += INT_TO_CHAR[x] + INT_TO_CHAR[y] + " "

    return cell_str

# sanity check to make sure cells were in positive region

def check_cells(card_num,r, col, cell_list):

    for (x, y) in cell_list:

        assert x >= 0, f"x for card {card_num} rotation {r} col {col} was negative"
        assert y >= 0, f"y for card {card_num} rotation {r} col {col} was negative"

#  translating intersection of A_i, A, and T together to make sure its on positive region of board

def translate(ia, a, t):

    cell_list = ia + a + t

    tx = min(x for (x,_) in cell_list)
    ty = min(y for (_,y) in cell_list)

    if tx < 0:
    
        tx = abs(tx)
    
    else:

        tx = -abs(tx)
    
    
    if ty < 0:
    
        ty = abs(ty)
    
    else:
    
        ty = -abs(ty)

    ia_translated = find_transform(0, tx, ty, ia)
    a_translated = find_transform(0, tx, ty, a)
    t_translated = find_transform(0, tx, ty, t)

    return ia_translated, a_translated, t_translated

#  finding all transforms of a particular card

def find_card_transforms(ind, ia_cell_str, a_cell_str, t_cell_str):

    transform_list = []

    ia_cell_list = []
    a_cell_list = []
    t_cell_list = []
    

    for cell_str in ia_cell_str.split():

        cell = (CHAR_TO_INT[cell_str[0]], CHAR_TO_INT[cell_str[1]])

        (x,y) = cell
        assert x>=0, f"card {ind} has negative x for inter_A"
        assert y>=0, f"card {ind} has negative y for inter_A"

        ia_cell_list.append(cell)

    for cell_str in a_cell_str.split():
    
        cell = (CHAR_TO_INT[cell_str[0]], CHAR_TO_INT[cell_str[1]])

        (x,y) = cell
        assert x>=0, f"card {ind} has negative x for A"
        assert y>=0, f"card {ind} has negative y for A"
    
        a_cell_list.append(cell)

    for cell_str in t_cell_str.split():
    
        cell = (CHAR_TO_INT[cell_str[0]], CHAR_TO_INT[cell_str[1]])

        (x,y) = cell
        assert x>=0, f"card {ind} has negative x for A"
        assert y>=0, f"card {ind} has negative y for A"
    
        t_cell_list.append(cell)

    
    cell_list = ia_cell_list + a_cell_list + t_cell_list

    for r in range(8):

        ia_trans = find_transform(r, 0, 0, ia_cell_list)
        a_trans = find_transform(r, 0, 0, a_cell_list)
        t_trans = find_transform(r, 0, 0, t_cell_list)

        ia_trans, a_trans, t_trans = translate(ia_trans, a_trans, t_trans)

        check_cells(ind,r,"inter_A",  ia_trans)
        check_cells(ind,r, "A",  a_trans)
        check_cells(ind,r, "T",  t_trans)

        transform_list = transform_list + [create_cell_str(ia_trans), create_cell_str(a_trans), create_cell_str(t_trans)]

    return transform_list

# finding all transforms for all cards in df

def generate_card_transforms():

    df = pd.read_csv("generator/version9/pruned_cards_by_interA.csv")

    a = df['A'].to_list()
    t = df['T'].to_list()
    ia = df['inter_A'].to_list()
    data = []

    for i in range(len(df)):

        data.append(find_card_transforms(i, ia[i], a[i], t[i]))

    # column suffix = rotation code r, so A_0 is the identity
    cols_inter_A = ["A_inter_0", "A_inter_1", "A_inter_2", "A_inter_3", "A_inter_4", "A_inter_5", "A_inter_6", "A_inter_7"]
    cols_A = ["A_0", "A_1", "A_2", "A_3", "A_4", "A_5", "A_6", "A_7"]
    cols_T = ["T_0", "T_1", "T_2", "T_3", "T_4", "T_5", "T_6", "T_7" ]
    cols = []

    for i in range(8):

        cols = cols + [cols_inter_A[i], cols_A[i], cols_T[i]]

    new_df = pd.DataFrame(data=data, columns=cols)

    df = pd.concat([df, new_df], axis=1)

    df.to_csv("generator/version9/card_A_T_transforms.csv")



