import os
import pygame
from player import Player
from util import *
import sys

pygame.init()
screen = pygame.display.set_mode((255, 255))
pygame.display.set_caption("No poison chocolate")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 20
HEIGHT = 20
MARGIN = 5

grid_size = sys.argv[1:]

me = Player(who='me')
computer = Player(who='heuristic algorithm')

grid = np.zeros(grid_size, dtype='uint8').tolist()

clock = pygame.time.Clock()
done = False
valid_move = True
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            if grid[row][column] == 0:
                if row == grid_size[0] and column == grid_size[1]:
                    print "You're poisoned!  I win!"
                    os._exit(0)

                grid = me.move(grid, (row, column))
                grid = computer.move(grid)
                print("I choose %d,%d (you're done for!)" % (grid[1][0], grid[1][1]))

                if grid == None:
                    'Something bad happened sir!'
                    break
                grid = grid[1]

            else:
                valid_move = False

    if not valid_move:
        continue

    screen.fill(BLACK)
    for row in range(grid_size[0]):
        for column in range(grid_size[1]):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            if row == grid_size[0] - 1 and column == grid_size[1] - 1:
                color = RED

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
