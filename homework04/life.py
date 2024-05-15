import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for _ in range(self.rows):
            row = [random.randint(0, 1) if randomize else 0 for _ in range(self.cols)]
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbours = []
        for offset_x, offset_y in offsets:
            neighbour_x, neighbour_y = x + offset_x, y + offset_y
            if 0 <= neighbour_x < self.cols and 0 <= neighbour_y < self.rows:
                neighbours.append(self.curr_generation[neighbour_y][neighbour_x])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0] * self.cols for _ in range(self.rows)]

        for y in range(self.rows):
            for x in range(self.cols):
                current_cell = self.curr_generation[y][x]
                neighbours = self.get_neighbours((y, x))
                neighbours_count = sum(neighbours)

                if current_cell == 1:
                    if 2 <= neighbours_count <= 3:
                        new_grid[y][x] = 1
                    else:
                        new_grid[y][x] = 0
                else:
                    if neighbours_count == 3:
                        new_grid[y][x] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded or not self.is_changing:
            self.prev_generation = self.curr_generation
            self.curr_generation = self.get_next_generation()
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        assert self.max_generations is not None

        return float(self.max_generations) <= self.generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with filename.open() as file:
            lines = file.readlines()
            size = len(lines), len(lines[0].strip())
            grid = [[int(cell) for cell in line.strip()] for line in lines]

        game = GameOfLife(size, randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as file:
            for row in self.curr_generation:
                file.write("".join(map(str, row)) + "\n")
