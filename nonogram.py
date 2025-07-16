#!/home/piece/Documents/pynonogram/.venv/bin/python

import numpy as np
from itertools import groupby
import random


def get_clues(cells):
    current_lenght = 0
    lenghts = []

    for i in range(len(cells)):
        if cells[i] == 1:
            current_lenght += 1
        else:
            if current_lenght > 0:
                lenghts.append(current_lenght)
            current_lenght = 0
    if current_lenght > 0:
        lenghts.append(current_lenght)

    return(lenghts)


class Nonogram:
    def __init__(self, dim):
        self.dim = dim
        self.solved_nonogram = self._nonogram_gen()
        self.user_nonogram = self._empty_nonogram()
        self.user_final_nonogram = self._convert_to_check()
        self.row_clues = self._gen_row_clues()
        self.col_clues = self._gen_col_clues()



    def _nonogram_gen(self):
        rows = random.randint(self.dim, self.dim)
        cols = rows
        nonogram = np.random.randint(0, 2, size=(rows, cols))
        return nonogram


    def _empty_nonogram(self):
        dim = len(self.solved_nonogram)
        nonogram = np.zeros(shape=(dim,dim), dtype=int)
        return nonogram


    def _gen_row_clues(self):
        row_clues = []
        for cells in self.solved_nonogram:
            row_clues.append(get_clues(cells))
        return row_clues

    def _gen_col_clues(self):
        col_clues = []
        for cells in self.solved_nonogram.T:
            col_clues.append(get_clues(cells))
        return col_clues

    def _convert_to_check(self):
        row = []
        nonogram = []
        counter=0
        for row_index, row_value in enumerate(self.user_nonogram):
            for col_index, cell_value in enumerate(row_value):
                counter+=1
                if cell_value != 2:
                    row.append(int(cell_value))
                elif cell_value == 2:
                    row.append(0)
                
                if counter == self.dim:
                    nonogram.append(row)
                    counter=0
                    row=[]
        return np.array(nonogram)

    def check_solved(self):
        self.user_final_nonogram = self._convert_to_check()
        if np.array_equal(self.user_final_nonogram, self.solved_nonogram):
#        if self.user_final_nonogram.all == self.solved_nonogram.all:
            solved = True
        else:
            solved = False
        return solved
    
    def get_cell_state(self, row, col):
        if 0 <= row < self.dim and 0 <= col < self.dim:
            return self.user_nonogram[row, col]
        return None # Or raise an error

    def set_cell_state(self, row, col, state):
        if 0 <= row < self.dim and 0 <= col < self.dim and state in [0, 1, 2, 3, 4, 5]:
            self.user_nonogram[row, col] = state
            self.check_solved() # Check if solved after every change
            return True
        return False


"""my_nonogram = Nonogram(dim=5)

print(my_nonogram.solved_nonogram, "\n")
print(my_nonogram.user_nonogram, "\n")
print("rows:", my_nonogram.row_clues, "\n")
print("columns:", my_nonogram.col_clues, "\n")
print(my_nonogram.check_solved())
"""