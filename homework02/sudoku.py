import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as file1:
        puzzle = file1.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    sudoku_grid = group(digits, 9)
    return sudoku_grid


def display(sudoku_grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                sudoku_grid[row][col].center(width) + ("|" if str(col) in "25" else "")
                for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], num: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    count = 0
    matrix = []
    while count < len(values):
        inside_array = []
        for _ in range(num):
            inside_array.append(values[count])
            count += 1
        matrix.append(inside_array)
    return matrix


def get_row(
    sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', "."], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', "."]
    >>> get_row([['1', '2', '3'], ['4', ".", '6'], ['7', '8', '9']], (1, 0))
    ['4', ".", '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], [".", '8', '9']], (2, 0))
    [".", '8', '9']
    """
    return sudoku_grid[pos[0]]


def get_col(
    sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', "."], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', ".", '6'], ['7', '8', '9']], (0, 1))
    ['2', ".", '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], [".", '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for i in sudoku_grid:
        col.append(i[pos[1]])
    return col


def get_block(
    sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.List[str]:
    block = []
    vert_block = (
        pos[0] - (pos[0] % 3),
        pos[0] - (pos[0] % 3) + 1,
        pos[0] - (pos[0] % 3) + 2,
    )
    hor_block = (
        pos[1] - (pos[1] % 3),
        pos[1] - (pos[1] % 3) + 1,
        pos[1] - (pos[1] % 3) + 2,
    )
    for i in vert_block:
        for j in hor_block:
            block.append(sudoku_grid[i][j])
    return block


def find_empty_positions(sudoku_grid: tp.List[tp.List[str]]) -> tp.Tuple[int, int]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', "."], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', ".", '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], [".", '8', '9']])
    (2, 0)
    """
    for i in range(len(sudoku_grid)):
        for j in range(len(sudoku_grid[i])):
            if sudoku_grid[i][j] == ".":
                return i, j
    return -1, -1


def find_possible_values(
    sudoku_grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]
) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row, col, block = (
        set(get_row(sudoku_grid, pos)),
        set(get_col(sudoku_grid, pos)),
        set(get_block(sudoku_grid, pos)),
    )
    possible_values = {str(i) for i in range(1, len(sudoku_grid) + 1)}
    ans = possible_values.difference(row.union(col).union(block))
    return ans


def solve(sudoku_grid: tp.List[tp.List[str]]) -> tp.List[tp.List[str]]:
    """Решение пазла, заданного в grid"""
    if (
        find_empty_positions(sudoku_grid) == (-1, -1)
        or len(find_possible_values(sudoku_grid, find_empty_positions(sudoku_grid)))
        == 0
    ):
        return grid
    for i in find_possible_values(sudoku_grid, find_empty_positions(sudoku_grid)):
        row, col = find_empty_positions(sudoku_grid)
        sudoku_grid[row][col] = i
        solve(sudoku_grid)
        if find_empty_positions(sudoku_grid) == (-1, -1):
            break
        sudoku_grid[row][col] = "."
    return sudoku_grid


def check_solution(inner_solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles

    for i in range(len(inner_solution)):
        for j in range(len(inner_solution[i])):
            loc = (i, j)
            row, col, block = (
                get_row(inner_solution, loc),
                get_col(inner_solution, loc),
                get_block(inner_solution, loc),
            )
            if (
                sorted(list(set(row))) != sorted(row)
                or sorted(list(set(col))) != sorted(col)
                or sorted(list(set(block))) != sorted(block)
            ):
                return False
            if inner_solution[i][j] == ".":
                return False
    return True


def generate_sudoku(num: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == ".")
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == ".")
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == ".")
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    sudoku_grid = [["."] * 9 for i in range(9)]
    sudoku_grid = solve(sudoku_grid)
    empty_cells = 81 - num
    while empty_cells > 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if sudoku_grid[i][j] != ".":
            sudoku_grid[i][j] = "."
            empty_cells -= 1
    return sudoku_grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
