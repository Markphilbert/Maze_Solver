from cell import Cell

import random
import time


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_after_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_after_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        visited = []
        self._solve_r([0,0])
        return visited

    def _solve_r(self, current_vertex, end = False):
        self._animate()
        current = self._cells[current_vertex[0]][current_vertex[1]]
        current.visited = True
        if current == self._cells[self._num_cols - 1][self._num_rows - 1]:
            end = True
            return end
        next_index_list = []
        if current_vertex[0] > 0 and not self._cells[current_vertex[0] - 1][current_vertex[1]].visited and not current.has_left_wall:
            next_index_list.append((current_vertex[0] - 1, current_vertex[1]))
        if current_vertex[0] < self._num_cols - 1 and not self._cells[current_vertex[0] + 1][current_vertex[1]].visited and not current.has_right_wall:
            next_index_list.append((current_vertex[0] + 1, current_vertex[1]))
        if current_vertex[1] > 0 and not self._cells[current_vertex[0]][current_vertex[1] - 1].visited and not current.has_top_wall:
            next_index_list.append((current_vertex[0], current_vertex[1] - 1))
        if current_vertex[1] < self._num_rows - 1 and not self._cells[current_vertex[0]][current_vertex[1] + 1].visited and not current.has_bottom_wall:
            next_index_list.append((current_vertex[0], current_vertex[1] + 1))
        sorted_neighbors = sorted(next_index_list)
        for neighbor in sorted_neighbors:
            current.draw_move(self._cells[neighbor[0]][neighbor[1]], True)
            found_end = self._solve_r(neighbor, end)
            if found_end:
                return True
            else:
                current.draw_move(self._cells[neighbor[0]][neighbor[1]], False)
        return False



    # point_one = Point(2,3)
    # point_two = Point(100,100)
    # line = Line(point_one,point_two)
    # cell = Cell(100,200,100,200, win)
    # cell.draw()
    # cell_two = Cell(200,300,200,300, win)
    # cell_two.draw()
    # cell.draw_move(cell_two, True)