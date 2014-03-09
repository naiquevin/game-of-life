from game_of_life import (pad_cells, list_to_matrix, matrix_to_list,
                          make_grid, Grid, destiny, id_to_pos,
                          cell_status, neighbours)


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


def test_list_to_matrix():
    c1 = range(4*4)
    assert list_to_matrix(c1, (4, 4)) == [[ 0,  1,  2,  3],
                                          [ 4,  5,  6,  7],
                                          [ 8,  9, 10, 11],
                                          [12, 13, 14, 15]]


def test_matrix_to_list():
    m1 = [[ 0,  1,  2,  3],
          [ 4,  5,  6,  7],
          [ 8,  9, 10, 11],
          [12, 13, 14, 15]]
    assert matrix_to_list(m1) == range(4*4)


def test_make_cells():
    g1 = make_grid('test1', size=(2, 2), live_cells=[0, 3])
    assert g1.cells == [1, 0, 0, 1]
    assert g1.rows == 2
    assert g1.cols == 2
    assert g1.name == 'test1'


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


def test_cell_status():
    grid = make_grid('test2', size=(5, 5), live_cells=[0, 3, 12, 18, 21])
    status = cell_status(grid)
    assert status((0, 0)) == 1
    assert status((0, 3)) == 1
    assert status((2, 0)) == 0
    assert status((3, 4)) == 0


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
