#!/usr/bin/python

import re
import sys
import pygame

pygame.init()

DEFAULT_WIDTH = 4
DEFAULT_HEIGHT = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH = 70
HEIGHT = 70
MARGIN = 10


class Grid(object):
    def __init__(self, rows):
        self.rows = rows

    def __eq__(self, other):
        return self.rows == other.rows

    def display(self, screen):
        screen.fill(BLACK)
        for y in range(self.height()):
            for x in range(self.width()):
                color = WHITE
                if self.is_cell_open(x, y):
                    color = GREEN
                if x == 0 and y == 0:
                    color = RED
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * y + MARGIN,
                                  (MARGIN + HEIGHT) * x + MARGIN,
                                  WIDTH,
                                  HEIGHT])

    def width(self):
        return len(self.rows[0])

    def height(self):
        return len(self.rows)

    def cell_at(self, x, y):
        return self.rows[y][x]

    def is_cell_open(self, x, y):
        return self.rows[y][x] == 'o'

    @staticmethod
    def of_size(width, height):
        rows = []
        for row in range(height):
            cols = ['o' for i in range(width)]
            if row == 0:
                cols[0] = '*'
            rows.append(cols)
        return Grid(rows)


def move(board, x, y):
    if [x, y] == [0, 0]:
        return board
    if (x >= board.width()) or (y >= board.height()):
        return board
    if not board.is_cell_open(x, y):
        return board
    new_rows = []
    for r in range(board.height()):
        new_row = ['o' for i in range(board.width())]
        for c in range(len(new_row)):
            new_row[c] = board.cell_at(c, r)
            if r >= y and c >= x:
                new_row[c] = '.'
        new_rows.append(new_row)
    return Grid(new_rows)


def heuristicMove(board, depth=0):
    rx = 0
    cx = 0
    for r in range(board.height()):
        for c in range(board.width()):
            if board.is_cell_open(c, r) and (r + c > 0):
                rx = r
                cx = c
                new_board = move(board, c, r)
                if heuristicMove(new_board, depth + 1)[0]:
                    continue
                if depth == 0:
                    board = move(board, c, r)
                    print("I choose %d,%d" % (c, r))
                return [True, board]
    if depth == 0:
        board = move(board, cx, rx)
        print("I choose %d,%d" % (cx, rx))
        if rx == 0 and cx == 0:
            print "I have lost. :-("
            return None
        # else:
        #     print "I am losing.  :-/"
    return [False, board]


def main(argv):
    clock = pygame.time.Clock()
    [width, height] = [DEFAULT_WIDTH, DEFAULT_HEIGHT]
    if len(argv) > 0:
        width = int(argv[0])
    if len(argv) > 1:
        height = int(argv[1])
    grid = Grid.of_size(width, height)
    print(width, WIDTH, height, HEIGHT, MARGIN)
    screen = pygame.display.set_mode((height * HEIGHT + height * MARGIN + MARGIN, width * WIDTH + width * MARGIN + MARGIN))
    pygame.display.set_caption("No poison chocolate")

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                y = pos[0] // (WIDTH + MARGIN)
                x = pos[1] // (HEIGHT + MARGIN)
                if x >= grid.width() or y >= grid.height():
                    continue
                if [x, y] == [0, 0]:
                    print "You're poisoned!  I win!"
                    return
                # time.sleep(1)
                grid = move(grid, x, y)
                calc_move = heuristicMove(grid)
                if calc_move is None:
                    break
                grid = calc_move[1]

        # grid.display()
        # [x, y] = get_user_move(grid)
        grid.display(screen)
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main(sys.argv[1:])
