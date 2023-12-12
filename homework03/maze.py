from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    grid_copy = deepcopy(grid)
    x, y = coord
    if grid_copy[x][y] != " ":
        grid_copy[x][y] = " "
    elif y + 1 < len(grid_copy[0]) - 1:
        grid_copy[x][y + 1] = " "
    elif x - 1 > 1:
        grid_copy[x - 1][y] = " "
    return grid_copy


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for row_x, row in enumerate(grid):
        for col_y, _ in enumerate(row):
            if row_x % 2 == 1 and col_y % 2 == 1:
                grid[row_x][col_y] = " "
                empty_cells.append((row_x, col_y))

    for current_row in range(1, rows - 1, 2):
        for current_col in range(1, cols - 1, 2):
            coin_flip = randint(0, 1)
            if coin_flip == 0:
                if current_row == 1:
                    if current_col + 1 == cols - 1:
                        continue
                    grid = remove_wall(grid, (current_row, current_col + 1))
                elif current_row + 1 <= rows - 1:
                    grid = remove_wall(grid, (current_row - 1, current_col))
            else:
                if current_row == 1:
                    if current_col + 1 == cols - 1:
                        continue
                    grid = remove_wall(grid, (current_row, current_col + 1))
                elif current_col + 1 < cols - 1:
                    grid = remove_wall(grid, (current_row, current_col + 1))
                else:
                    grid = remove_wall(grid, (current_row - 1, current_col))

    if random_exit:
        entry_x, exit_x = randint(0, rows - 1), randint(0, rows - 1)
        entry_y = randint(0, cols - 1) if entry_x in (0, rows - 1) else choice((0, cols - 1))
        exit_y = randint(0, cols - 1) if exit_x in (0, rows - 1) else choice((0, cols - 1))
    else:
        entry_x, entry_y = 0, cols - 2
        exit_x, exit_y = rows - 1, 1

    grid[entry_x][entry_y], grid[exit_x][exit_y] = "X", "X"
    get_exits(grid)
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exit_coordinates = []
    for i in range(len(grid[0]) - 1):
        if grid[0][i] == "X":
            exit_coordinates.append((0, i))
    for i in range(len(grid) - 1):
        if grid[i][0] == "X":
            exit_coordinates.append((i, 0))
    for i in range(len(grid) - 1):
        if grid[i][len(grid) - 1] == "X":
            exit_coordinates.append((i, len(grid) - 1))
    for i in range(len(grid[0]) - 1):
        if grid[len(grid[0]) - 1][i] == "X":
            exit_coordinates.append((len(grid[0]) - 1, i))
    if len(exit_coordinates) > 1:
        if exit_coordinates[0][0] > exit_coordinates[1][0]:
            exit_coordinates[0], exit_coordinates[1] = (
                exit_coordinates[1],
                exit_coordinates[0],
            )
    return exit_coordinates


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    current_cell = []
    coefficient = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == k:
                current_cell.append((row, col))
                coefficient.append(k + 1)
    while current_cell and coefficient:
        x, y = current_cell[0]
        for x_shift, y_shift in directions:
            if 0 <= x + x_shift < len(grid) and 0 <= y + y_shift < len(grid[0]):
                if grid[x + x_shift][y + y_shift] == 0:
                    grid[x + x_shift][y + y_shift] = coefficient[0]
        current_cell.pop(0)
        coefficient.pop(0)
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    x, y = exit_coord
    k = grid[x][y]
    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    path = [(x, y)]
    while k != 1:
        for x_move, y_move in moves:
            if 0 <= x + x_move < len(grid) and 0 <= y + y_move < len(grid[0]):
                next_cell = grid[x + x_move][y + y_move]
                if type(next_cell) == int and next_cell < int(k):
                    x, y = x + x_move, y + y_move
                    path.append((x, y))
                    k = grid[x][y]

    for i in range(len(grid) - 1):
        for j in range(len(grid[0])):
            if grid[i][j] != "■":
                grid[i][j] = " "
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    if (
        coord == (0, 0)
        or coord == (len(grid) - 1, len(grid) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (0, len(grid) - 1)
        or x == 0
        and grid[1][y] != " "
        or x == len(grid) - 1
        and grid[len(grid) - 2][y] != " "
        or y == 0 and grid[x][1] != " "
        or y == len(grid) - 1
        and grid[x][len(grid) - 2] != " "
    ):
        return True
    else:
        return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits = get_exits(grid)
    if len(exits) < 2:
        return (
            grid,
            exits[0],
        )
    else:
        for door in exits:
            if encircled_exit(grid, door):
                return grid, None
    enter = exits[0]
    exit_point = exits[1]
    if exit_point[1] - enter[1] == 1 and exit_point[0] - enter[0] == 0:
        return grid, exits[::-1]
    elif exit_point[1] - enter[1] == 0 and exit_point[0] - enter[0] == 1:
        return grid, exits[::-1]
    elif exit_point[0] - enter[0] == 0 and exit_point[1] - enter[1] == 1:
        return grid, exits[::-1]
    elif exit_point[0] - enter[0] == 1 and exit_point[1] - enter[1] == 0:
        return grid, exits[::-1]

    grid[exits[0][0]][exits[0][1]] = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " ":
                grid[i][j] = 0
            elif grid[i][j] == "X":
                grid[i][j] = 0

    k = 1
    while grid[exits[1][0]][exits[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1

    path = shortest_path(grid, exits[1])

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    grid_copy = deepcopy(grid)
    if path:
        for i, row in enumerate(grid_copy):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid_copy[i][j] = "X"
    return grid_copy


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
