import numpy as np


def select(grid, place):
    new_grid = np.array(grid)
    new_grid[:place[0] + 1, :place[1] + 1] = 1
    return new_grid.tolist()
