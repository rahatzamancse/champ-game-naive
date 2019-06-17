from util import *


class Player:
    def __init__(self, who):
        self.who = who

    def move(self, grid, place=None):
        def get_opt(grid, who):
            if sum([sum(i) for i in grid]) == len(grid) * len(grid[0]):
                if who == 'me':
                    return 1
                else:
                    return 0

            summation = 0
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col] != 1:
                        new_grid = select(grid, (row, col))
                        summation += get_opt(new_grid, 'me' if who == 'opp' else 'opp')
            return summation

        if self.who == 'heuristic algorithm':
            max_row = None
            max_col = None
            max_sum = -1
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col] == 0:
                        new_grid = select(grid, (row, col))
                        summation = get_opt(grid, 'me')
                        if summation > max_sum:
                            print(row, col, max_row, max_col, summation, max_sum)
                            summation = max_sum
                            max_row = row
                            max_col = col
            return select(grid, (max_row, max_col))

        elif self.who == 'me':
            return select(grid, place)
