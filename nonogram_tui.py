#!/home/piece/Documents/pynonogram/.venv/bin/python

import numpy as np
from itertools import groupby
import random

import sys

import curses
from curses import *

from nonogram import Nonogram




def main(stdsrc):
    curses.curs_set(0)  
    stdsrc.nodelay(True)
    stdsrc.timeout(500)
    stdsrc.keypad(True)
    curses.noecho()
    curses.cbreak()


    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, 8)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    cell_chars = {"empty": " ",
                   "filled": "O",
                   "cross": "X",
                   "note_full": "@", 
                   "note_cross": "/"
    }

    dim = 5

    if len(sys.argv) > 1:
        dim = int(sys.argv[1])
    else:
        dim = 5

    puzzle = Nonogram(dim=dim)

    row_clues = puzzle.row_clues
    col_clues = puzzle.col_clues

    dimension = len(puzzle.solved_nonogram)    

    cursor_row = 0
    cursor_col = 0
    
    running = True
    while running:
        stdsrc.erase()
        x = dimension * 3
        y = dimension
    
        def draw_grid(user_puzzle, x_init, y_init, solved, color):
            p_x = x
            p_y = y
            counter = 0
            tcolor = color
            for row_index, row_value in enumerate(user_puzzle):
                for col_index, cell_value in enumerate(row_value):
                    screen_x = x + (col_index + 1) * 3
                    screen_y = y + row_index

                    char_to_draw = cell_chars["empty"]
                    if cell_value == 1:
                        char_to_draw = cell_chars["filled"]
                        tcolor = 5

                    elif cell_value == 0:
                        char_to_draw = cell_chars["empty"]
                        tcolor = color

                    elif cell_value == 2:
                        char_to_draw = cell_chars["cross"]
                        tcolor = 6

                    elif cell_value == 3:
                        char_to_draw = cell_chars["note_cross"]
                        tcolor = 7

                    elif cell_value == 4:
                        char_to_draw = cell_chars["note_full"]
                        tcolor = 7

                    p_x += 3
                    counter += 1
                    stdsrc.addstr(p_y, p_x, f"[{char_to_draw}]", curses.color_pair(tcolor))
                    if counter == dimension:
                        p_y += 1
                        p_x = x
                        counter = 0

                    
                    if solved == False:
                        if row_index == cursor_row and col_index == cursor_col:
                            stdsrc.addstr(screen_y, screen_x, f"[{char_to_draw}]", curses.color_pair(2))
                            """
                        elif row_index == cursor_row or col_index == cursor_col:
                            stdsrc.addstr(screen_y, screen_x, f"[{char_to_draw}]", curses.color_pair(3))
                        """
                        else:
                            stdsrc.addstr(screen_y, screen_x, f"[{char_to_draw}]", curses.color_pair(tcolor))
                    elif solved == True:
                        stdsrc.addstr(screen_y, screen_x, f"[{char_to_draw}]", curses.color_pair(tcolor))

            p_y = y

        draw_grid(puzzle.user_nonogram, x, y, False, 1)


        def draw_row_clues(row_clues, x_init, y_init):
            x = x_init
            y = y_init
            rc_counter = 0
            for row_index, row_value in enumerate(row_clues):
                stdsrc.addstr(y, 
                              x - len(row_value) * 3,
                              f"{row_value}")
                y+=1

        draw_row_clues(puzzle.row_clues, x, y)


        def draw_col_clues(col_clues, x_init, y_init):
            cc_x = x_init + 1
            cc_y = y_init - 1
            for index, value in enumerate(col_clues):
                cc_x += 3
                for index, cue in enumerate(value):
                    stdsrc.addstr(cc_y - len(value),
                                cc_x,
                                f"{cue}")
                    cc_y+=1
                cc_y=y_init - 1

        draw_col_clues(col_clues, x, y)


        if puzzle.check_solved() == True:
            stdsrc.addstr(x, y, "SOLVED! Press 'q' to quit.", curses.color_pair(4))
            draw_grid(puzzle.solved_nonogram, x, y, True, 6)
            curses.beep()


        stdsrc.refresh()

        key = stdsrc.getch()
        if key == ord('q'):
            running = False

        elif key == ord('f'):
            if not puzzle.check_solved(): 
                current_cell_state = puzzle.get_cell_state(cursor_row, cursor_col)
                if current_cell_state == 0 or current_cell_state == 4:
                    puzzle.set_cell_state(cursor_row, cursor_col, 1)
                else:
                    puzzle.set_cell_state(cursor_row, cursor_col, 0)
        
        elif key == ord('d'):
            if not puzzle.check_solved(): 
                current_cell_state = puzzle.get_cell_state(cursor_row, cursor_col)
                if current_cell_state == 0 or current_cell_state == 3:
                    puzzle.set_cell_state(cursor_row, cursor_col, 2)
                else:
                    puzzle.set_cell_state(cursor_row, cursor_col, 0)
                    
        elif key == ord('e'):
            if not puzzle.check_solved(): 
                current_cell_state = puzzle.get_cell_state(cursor_row, cursor_col)
                if current_cell_state == 0:
                    puzzle.set_cell_state(cursor_row, cursor_col, 3)
                elif current_cell_state == 4 or current_cell_state == 3:
                    puzzle.set_cell_state(cursor_row, cursor_col, 0)
        
        elif key == ord('r'):
            if not puzzle.check_solved(): 
                current_cell_state = puzzle.get_cell_state(cursor_row, cursor_col)
                if current_cell_state == 0:
                    puzzle.set_cell_state(cursor_row, cursor_col, 4)
                elif current_cell_state == 3 or current_cell_state == 4:
                    puzzle.set_cell_state(cursor_row, cursor_col, 0)

        elif key == curses.KEY_UP:
            cursor_row = max(-1, cursor_row - 1)
        elif key == curses.KEY_DOWN:
            cursor_row = min(dimension, cursor_row + 1)
        elif key == curses.KEY_LEFT:
            cursor_col = max(-1, cursor_col - 1)
        elif key == curses.KEY_RIGHT:
            cursor_col = min(dimension, cursor_col + 1)

        
        if cursor_row == -1:
            cursor_row = dimension
        elif cursor_row == dimension:
            cursor_row = -1

        if cursor_col == -1:
            cursor_col = dimension
        elif cursor_col == dimension:
            cursor_col = -1

wrapper(main)
