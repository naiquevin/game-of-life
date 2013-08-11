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
from math import sqrt


ALIVE = 1
DEAD = 0

ALIVE_CHAR = '#'
DEAD_CHAR = ' '

SIZE = 25 # should be a perfect square
INIT_ALIVE = int(SIZE * 0.85)

## Interesting initial configurations
BLINKER = (25, [11, 12, 13])
TOAD = (36, [14, 15, 16, 19, 20, 21])
BEACON = (36, [7, 8, 13, 22, 27, 28])


## VT100 control codes
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def grid(live_cells=None):
    live_cells = [] if live_cells is None else live_cells
    cells = [ALIVE if i in live_cells else DEAD
             for i in range(SIZE)]
    return cells

def test_grid():
    g1 = grid(size=4, live_cells=[0, 3])
    assert g1 == [1, 0, 0, 1]


def game(g):
    cells = zip(range(SIZE), g)
    cell_destiny = destiny(g)
    new_grid = [cell_destiny(i, s) for i, s in cells]
    return new_grid


def destiny(g):
    def inner(i, s):
        pos = cell_pos(i)
        live_ngh = len(live_neighbours(pos, g))
        if s == ALIVE:
            return ALIVE if live_ngh in (2, 3) else DEAD
        if s == DEAD:
            return ALIVE if live_ngh == 3 else DEAD
    return inner


def print_grid(g):
    n_rows = int(sqrt(SIZE))
    for i in range(n_rows):
        print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
    gs = [ALIVE_CHAR if c == ALIVE else DEAD_CHAR
          for c in g]
    output = []
    for i, c in enumerate(gs):
        if i != 0 and i % n_rows == 0:
            output.append('\n')
        output.append(c)
    output.append('\n')
    sys.stdout.write('\r' + ''.join(output))
    sys.stdout.flush()


def loop(state, fn, interval=1):
    print_grid(state)
    new_state = fn(state)
    time.sleep(interval)
    return loop(new_state, fn, interval)


def cell_pos(cell_index):
    n_rows = int(sqrt(SIZE))
    row = cell_index//n_rows
    column = cell_index % n_rows
    return (row, column)

def test_cell_pos():
    assert cell_pos(0) == (0, 0)
    assert cell_pos(24) == (4, 4)
    assert cell_pos(10) == (2, 0)


def cell_status(g):
    def inner(pos):
        row, col = pos
        return g[row * int(sqrt(SIZE)) + col]
    return inner


def test_cell_status():
    g1 = grid(size=25, live_cells=[0, 3, 12, 18, 21])
    status = cell_status(g1)
    assert status((0, 0)) == 1
    assert status((0, 3)) == 1
    assert status((2, 0)) == 0
    assert status((3, 4)) == 0


def neighbours(pos):
    prv = lambda x: x-1 if x > 0 else None
    nxt = lambda x: x+1 if x < 4 else None
    valid_cell = lambda x: all(map(lambda y: y is not None, x))
    row, col = pos
    return filter(lambda x: valid_cell(x),
                  [(prv(row), prv(col)),
                   (prv(row), col),
                   (prv(row), nxt(col)),
                   (row     , prv(col)),
                   (row     , nxt(col)),
                   (nxt(row), prv(col)),
                   (nxt(row), col),
                   (nxt(row), nxt(col))])

def test_neighbors():
    p1 = cell_pos(0)
    assert neighbours(p1) == [(0, 1), (1, 0), (1, 1)]
    p2 = cell_pos(18)
    assert neighbours(p2) == [(2, 2), (2, 3), (2, 4),
                              (3, 2),         (3, 4),
                              (4, 2), (4, 3), (4, 4)]
    p3 = cell_pos(24)
    assert neighbours(p3) == [(3, 3), (3, 4), (4, 3)]


def live_neighbours(pos, g):
    status = cell_status(g)
    return [c for c in neighbours(pos) if status(c) == ALIVE]


def main(g):
    try:
        loop(g, game)
    except KeyboardInterrupt:
        print '\rbye!'
        exit(0)


if __name__ == '__main__':
    SIZE, live_cells = TOAD
    main(grid(live_cells=live_cells))

