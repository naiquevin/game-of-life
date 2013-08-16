## Conway's game of life implementation in Python
## It runs in the terminal.
##
## http://en.wikipedia.org/wiki/Conway's_Game_of_Life
##
## How to run?
## ===========
##
##  $ python game_of_life.py
##

from __future__ import division
import sys
import time
import os
from functools import reduce
from collections import namedtuple
import random


ALIVE = 1
DEAD = 0

ALIVE_CHAR = '#'
DEAD_CHAR = ' '

## Interesting initial configurations
BLINKER = ((5, 5), [11, 12, 13])
TOAD = ((6, 6), [14, 15, 16, 19, 20, 21])
BEACON = ((6, 6), [7, 8, 13, 22, 27, 28])


## VT100 control codes
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


## representation of a grid
Grid = namedtuple('Grid', ['name', 'cells', 'rows', 'cols'])


## For parsing cell patterns from .cells files

def load_grid(filename):
    """Reads a .cells file and loads a Grid namedtuple"""
    name = os.path.splitext(os.path.basename(filename))[0]
    with open(os.path.abspath(filename)) as f:
        lines = [[ALIVE if c == 'O' else DEAD for c in line if c not in ('', '\n')]
                 for line in f
                 if not line.startswith('!') and line != '']
        rows = len(lines)
        cols = len(lines[0])
        cells = reduce(lambda x, y: x + y, lines, [])
        padded_cells, (new_rows, new_cols) = pad_cells(cells, size=(rows, cols), padding=1)
        return Grid(name=name,
                    cells=padded_cells,
                    rows=new_rows,
                    cols=new_cols)


def make_grid(name, size, live_cells):
    """Produces a grid from size and a list of "alive" cells

    :param name       : String
    :param size       : tuple eg. (#rows, #cols)
    :param live_cells : list of integers representing indexes at which
                        the cells are alive
    :rtype            : Grid namedtuple

    """
    rows, cols = size
    cells = [ALIVE if i in live_cells else DEAD
             for i in range(rows * cols)]
    return Grid(name=name,
                cells=cells,
                rows=rows,
                cols=cols)


def pad_cells(cells, size, padding=1):
    rows, cols = size
    # convert list to matrix
    matrix = list_to_matrix(cells, size)
    # pad with extra rows and cols
    matrix = [[DEAD]*padding + row + [DEAD]*padding
              for row in matrix]
    matrix = [[DEAD]*len(matrix[0])] + matrix + [[DEAD]*len(matrix[0])]
    # convert to flat list again
    return (matrix_to_list(matrix), (rows+2*padding, cols+2*padding))


def test_pad_cells():
    c1 = range(16)
    c1_p, (nr, nc) = pad_cells(c1, size=(4, 4))
    assert nr == 6
    assert nc == 6
    assert len(c1_p) == 36
    assert c1_p == [0,  0,  0,  0,  0, 0,
                    0,  0,  1,  2,  3, 0,
                    0,  4,  5,  6,  7, 0,
                    0,  8,  9, 10, 11, 0,
                    0, 12, 13, 14, 15, 0,
                    0,  0,  0,  0,  0, 0]


def list_to_matrix(items, size):
    rows, cols = size
    return [items[i:i+cols] for i in range(0, len(items), cols)]


def test_list_to_matrix():
    c1 = range(4*4)
    assert list_to_matrix(c1, (4, 4)) == [[ 0,  1,  2,  3],
                                          [ 4,  5,  6,  7],
                                          [ 8,  9, 10, 11],
                                          [12, 13, 14, 15]]


def matrix_to_list(matrix):
    return reduce(lambda x,y: x+y, matrix, [])

def test_matrix_to_list():
    m1 = [[ 0,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11],
          [12, 13, 14, 15]]
    assert matrix_to_list(m1) == range(4*4)


def update_cells(grid, cells):
    """Produces a new grid from the original one with the cells updated

    :param grid  : Grid namedtuple
    :param cells : list
    :rtype       : Grid namedtuple

    """
    return Grid(name=grid.name,
                cells=cells,
                rows=grid.rows,
                cols=grid.cols)


def test_make_cells():
    g1 = make_grid('test1', size=(2, 2), live_cells=[0, 3])
    assert g1.cells == [1, 0, 0, 1]
    assert g1.rows == 2
    assert g1.cols == 2
    assert g1.name == 'test1'


def tick(grid):
    """The callback function to be passed to the game loop

    :param grid : Grid namedtuple
    :rtype      : Grid namedtuple

    """
    cell_destiny = destiny(grid)
    size = grid.rows * grid.cols
    new_cells = [cell_destiny(i) for i in range(size)]
    return update_cells(grid, new_cells)


def destiny(grid):
    """A function that takes a Grid namedtuple and returns a curried
    function that decides what will happen to a the cell as per the
    rules of Conway's game of life.

    The curried function takes index (int) and the current state of
    the cell

    """
    def inner(i):
        pos = id_to_pos(i, grid)
        live_ngh = len(live_neighbours(pos, grid))
        if grid.cells[i] == ALIVE:
            return ALIVE if live_ngh in (2, 3) else DEAD
        if grid.cells[i] == DEAD:
            return ALIVE if live_ngh == 3 else DEAD
    return inner


def test_destiny():
    cells = [
        0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 1, 0,
        0, 1, 1, 1, 0, 0,
        0, 0, 0, 0, 0, 0,
    ]
    new_cells = [
        0, 0, 0, 1, 0, 0,
        0, 1, 0, 0, 1, 0,
        0, 1, 0, 0, 1, 0,
        0, 0, 1, 0, 0, 0,
    ]
    grid = Grid(name='toad',
                cells=cells,
                rows=4,
                cols=6)
    dest = destiny(grid)
    for i in range(grid.rows*grid.cols):
        assert dest(i) == new_cells[i]


def print_grid(grid, init=False):
    """Prints the grid in the terminal and makes sure it's overwritten

    :param grid: Grid namedtuple

    """
    if not init:
        for i in range(grid.rows):
            print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    gs = [ALIVE_CHAR if c == ALIVE else DEAD_CHAR
          for c in grid.cells]
    output = []
    for i, c in enumerate(gs):
        if i != 0 and i % grid.cols == 0:
            output.append('\n')
        output.append(c)
    output.append('\n')
    sys.stdout.write('\r' + ''.join(output))
    sys.stdout.flush()


def loop(state, fn, interval=1, init=False):
    """Runs infinitely calling the function at the interval and updating
    state as per the function calls return value

    :param state    : State of the game (Grid namedtuple in this case)
    :param fn       : Callback function
    :param interval : refresh rate in seconds

    """
    print_grid(state, init)
    new_state = fn(state)
    time.sleep(interval)
    return loop(new_state, fn, interval)


def id_to_pos(cell_index, grid):
    """Produces position in a grid from index of a flat list

    :param cell_index : int
    :param grid       : Grid namedtuple
    :rtype            : tuple(int, int) of row and column

    """
    row = cell_index//grid.cols
    column = cell_index % grid.cols
    return (row, column)


def test_id_to_pos():
    grid = Grid(name='test3', rows=5, cols=5, cells=None)
    assert id_to_pos(0, grid) == (0, 0)
    assert id_to_pos(24, grid) == (4, 4)
    assert id_to_pos(10, grid) == (2, 0)
    toad = Grid(name='toad',
                cells=[
                    0, 0, 0, 0, 0, 0,
                    0, 0, 1, 1, 1, 0,
                    0, 1, 1, 1, 0, 0,
                    0, 0, 0, 0, 0, 0,
                ],
                rows=4,
                cols=6)
    assert id_to_pos(7, toad) == (1, 1)


def pos_to_id(pos, grid):
    """Produces id of flat cells list from row,col position

    :param pos  : tuple(int, int)
    :param grid : Grid namedtuple
    :rtype      : int

    """
    row, col = pos
    return row * grid.cols + col


def cell_status(grid):
    """Function that takes a grid and returns a curried function that
    computes the current status of a position in the grid

    """
    def inner(pos):
        return grid.cells[pos_to_id(pos, grid)]
    return inner


def test_cell_status():
    grid = make_grid('test2', size=(5, 5), live_cells=[0, 3, 12, 18, 21])
    status = cell_status(grid)
    assert status((0, 0)) == 1
    assert status((0, 3)) == 1
    assert status((2, 0)) == 0
    assert status((3, 4)) == 0


def neighbours(grid):
    """A function that takes a grid and returns a curried function to
    compute neighbours of a position in the grid which are returned as
    a list of position tuples

    """
    def inner(pos):
        prv = lambda x: x-1 if x > 0 else None
        nxt_row = lambda x: x+1 if x < (grid.rows-1) else None
        nxt_col = lambda x: x+1 if x < (grid.cols-1) else None
        valid_cell = lambda x: all(map(lambda y: y is not None, x))
        row, col = pos
        return filter(lambda x: valid_cell(x),
                      [(prv(row), prv(col)),
                       (prv(row), col),
                       (prv(row), nxt_col(col)),
                       (row, prv(col)),
                       (row, nxt_col(col)),
                       (nxt_row(row), prv(col)),
                       (nxt_row(row), col),
                       (nxt_row(row), nxt_col(col))])
    return inner


def test_neighbors():
    grid = make_grid('test2', size=(5, 5), live_cells=[0, 3, 12, 18, 21])
    get_neighbours = neighbours(grid)
    p1 = id_to_pos(0, grid)
    assert get_neighbours(p1) == [(0, 1), (1, 0), (1, 1)]
    p2 = id_to_pos(18, grid)
    assert get_neighbours(p2) == [(2, 2), (2, 3), (2, 4),
                                  (3, 2),         (3, 4),
                                  (4, 2), (4, 3), (4, 4)]
    p3 = id_to_pos(24, grid)
    assert get_neighbours(p3) == [(3, 3), (3, 4), (4, 3)]


def live_neighbours(pos, grid):
    """Produces alive neighbours of a cell in the grid at position 'pos'

    :param pos  : pos tuple
    :param grid : Grid namedtuple
    :rtype      : list of pos tuples

    """
    status = cell_status(grid)
    get_neighbours = neighbours(grid)
    return [c for c in get_neighbours(pos) if status(c) == ALIVE]


def main(grid):
    try:
        loop(grid, tick, interval=0.2, init=True)
    except KeyboardInterrupt:
        print '\rbye!'
        exit(0)


if __name__ == '__main__':
    try:
        cellsfile = sys.argv[1]
        grid = load_grid(cellsfile)
    except IndexError:
        files = os.listdir('cells')
        cellsfile = os.path.join('cells', files[random.randint(0, len(files))])
        grid = load_grid(cellsfile)
        raw_input('Randomly selected to play pattern %r\nPress enter to start' % (grid.name,))
    main(grid)
