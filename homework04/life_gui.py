import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 30, speed: int = 1) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode((self.life.cols * self.cell_size, self.life.rows * self.cell_size))
        self.onpause = False

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows * self.cell_size))
        for y in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols * self.cell_size, y))

    def draw_grid(self) -> None:
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                color = pygame.Color("green") if self.life.curr_generation[y][x] == 1 else pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    (x * self.cell_size + 1, y * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1),
                )

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode((self.life.cols * self.cell_size, self.life.rows * self.cell_size))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.onpause = not self.onpause
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    cell_x, cell_y = x // self.cell_size, y // self.cell_size
                    self.life.curr_generation[cell_y][cell_x] = (
                        1 if self.life.curr_generation[cell_y][cell_x] == 0 else 0
                    )

            if not self.onpause:
                self.life.step()
            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)


if __name__ == "__main__":
    game = GameOfLife((10, 15), max_generations=50)
    gui = GUI(game)
    gui.run()
