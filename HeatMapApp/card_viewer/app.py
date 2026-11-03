import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import Union
import math

def get_cells(ind : int) -> Union[set, list]:

    df = pd.read_csv("HeatMapApp/certificate/card_cells.csv")

    construct = df.iloc[ind-6]['card_cells']

    cells_list = construct.split(" ")
    cells_set = set(cells_list)

    return cells_set, cells_list


def get_board(cell_set : set, cell_list : list) -> list[list]:

    cell_val_dict = {
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
        "G" : 16,
        "H" : 17
    }

    board = [[0 for _ in range(17)] for _ in range(17)]

    for cell in cell_set:

        if cell:

            (x, y) = (cell_val_dict[cell[0]], cell_val_dict[cell[1]])
                

            board[16-y][x] = (cell_list.count(cell))/len(cell_list)

    return board

def create_board_heatmap(card_num):

    cell_set, cells_list = get_cells(int(card_num))

    board = get_board(cell_set, cells_list)

    fig, ax = plt.subplots(figsize=(17, 17))

    rows = len(board)
    cols = len(board[0])

    max_val = max(max(row) for row in board)

    board = [[c/max_val for c in row] for row in board]

    for r in range(rows):
        for c in range(cols):

            color = (board[r][c],1.0 - board[r][c], 1.0 - board[r][c])

            rect = Rectangle(
                (c, rows-r-1),  # x,y
                1,              # width
                1,              # height
                facecolor=color,
                edgecolor="gray"
            )

            ax.add_patch(rect)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")

    st.pyplot(fig)

def create_board_shape(card_num):

    cell_set, cells_list = get_cells(int(card_num))

    board = get_board(cell_set, cells_list)

    fig, ax = plt.subplots(figsize=(17, 17))

    rows = len(board)
    cols = len(board[0])

    max_val = max(max(row) for row in board)

    board = [[c/max_val for c in row] for row in board]

    for r in range(rows):
        for c in range(cols):

            if board[r][c] > 0.0:

                color="black"

            else:

                color="white"

            rect = Rectangle(
                (c, rows-r-1),  # x,y
                1,              # width
                1,              # height
                facecolor=color,
                edgecolor="gray"
            )

            ax.add_patch(rect)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")

    st.pyplot(fig)


card_num = st.number_input(
                label="ENTER CARD NUMBER",
                min_value=6,
                max_value=727)


st.session_state.card_num = card_num

if st.button("SHOW CARD HEATMAP"):

    create_board_heatmap(st.session_state.card_num)

if st.button("SHOW CARD SHAPE"):

    create_board_shape(st.session_state.card_num)

        