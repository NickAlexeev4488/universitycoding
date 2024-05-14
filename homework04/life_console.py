import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Display borders."""
        screen.addstr(0, 0, "+" + "-" * self.life.cols + "+")
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, "|")
            screen.addstr(i, self.life.cols + 1, "|")
        screen.addstr(self.life.rows + 1, 0, "+" + "-" * self.life.cols + "+")

    def draw_grid(self, screen) -> None:
        """Display the state of cells."""
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                screen.addstr(y + 1, x + 1, "*" if self.life.curr_generation[y][x] else " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        while not self.life.is_max_generations_exceeded and self.life.is_changing:
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            curses.napms(600)  # Sleep for 1 second
            self.life.step()  # Move to the next generation
            screen.clear()
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife((20, 40), True, 20)
    console_ui = Console(game)
    console_ui.run()
