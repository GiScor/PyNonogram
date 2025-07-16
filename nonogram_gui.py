import numpy as np
from itertools import groupby
import random

import sys

import pygame
from pygame.locals import *

from nonogram import Nonogram

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Arial', 18)

puzzle = Nonogram(dim=10)

color_screen = 255, 255, 255
color_cell = 0, 0, 0
color_line = 50, 50, 50
size = width, height = 1280, 720

cell_size = 25

grid_size = len(puzzle.solved_nonogram)

x = 150
y = 150

screen = pygame.display.set_mode(size)

def quit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


def draw_cell(nonogram, width, height, x, y):
    counter = 0
    x_init = x
    y_init = y
    for row_index, row_value in enumerate(nonogram):
        for cell_index, cell_value in enumerate(row_value):
            pygame.draw.rect(screen, color_cell, pygame.Rect(x, y, width, height))
            x += width + 3
            counter += 1
            if counter == len(nonogram):
                y += height + 3
                x = x_init
                counter = 0
    x = x_init
    y = y_init

def draw_hline(nonogram, x1, y1, x2, y2):
    x1 -= 2
    x2 = x1 + grid_size * (cell_size + 3)
    y1 -= 2
    y2 -= 2
    for i in nonogram:
        pygame.draw.line(screen, color_line, [x1, y1], [x2, y2], 1)
        y1 += cell_size + 3
        y2 += cell_size + 3
    pygame.draw.line(screen, color_line, [x1, y1], [x2, y2], 1)
    
def draw_vline(nonogram, x1, y1, x2, y2):
    y1 -= 2
    y2 = y1 + grid_size * (cell_size + 3)
    x1 -= 2
    x2 -= 2
    for i in nonogram:
        pygame.draw.line(screen, color_line, [x1, y1], [x2, y2], 1)
        x1 += cell_size + 3
        x2 += cell_size + 3
    pygame.draw.line(screen, color_line, [x1, y1], [x2, y2], 1)
    
def draw_row_clues(row_clues, x_init, y_init):
            x = x_init 
            y = y_init
            rc_counter = 0
            clue_text = font.render(f"{row_clues}", 1, color_cell, color_screen)
            clue_rect = clue_text.get_rect()
            for row_index, row_value in enumerate(row_clues):
                screen.blit(clue_text, (x_init, y_init))
                y+=1



while True:
    screen.fill(color_screen)
    
    draw_cell(puzzle.solved_nonogram, cell_size, cell_size, x, y)
    draw_hline(puzzle.solved_nonogram, x, y, x, y)
    draw_vline(puzzle.solved_nonogram, x, y, x, y)
    draw_row_clues(puzzle.row_clues, x, y)
    pygame.display.update()
    quit()