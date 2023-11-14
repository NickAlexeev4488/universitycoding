import typing as tp
import random

N = 10


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for i in grid:
        col.append(i[pos[1]])
    return col


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    vert_block = (pos[0] - (pos[0] % 3), pos[0] - (pos[0] % 3) + 1, pos[0] - (pos[0] % 3) + 2)
    hor_block = (pos[1] - (pos[1] % 3), pos[1] - (pos[1] % 3) + 1, pos[1] - (pos[1] % 3) + 2)
    for i in vert_block:
        for j in hor_block:
            block.append(grid[i][j])
    return block

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row, col, block = set(get_row(grid, pos)), set(get_col(grid, pos)), set(get_block(grid, pos))
    return {str(i) for i in range(1, len(grid) + 1)}.difference(row.union(col).union(block))


grid = [['.'] * 9 for i in range(9)]
if N >= 81:
    return solve(grid)

for i in range(N):
    row, col = random.randint(0, 8), random.randint(0, 8)
    while grid[row][col] != '.':
        row, col = random.randint(0, 8), random.randint(0, 8)
    grid[row][col] = str(random.randint(1, 9))

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] != '.':
            for k in find_possible_values(grid, (i, j)):
                grid[i][j] = k
print(grid)