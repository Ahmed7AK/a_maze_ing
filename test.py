import os
import random
import time


width = os.get_terminal_size().columns
maze_width = 20 * 2
padding = " " * ((width - maze_width) // 2)

# ANSI escape codes
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0m"
WALL = "\u2588\u2588"
PATH = "  "


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def rgb_back(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def draw(maze):
    print("\n")
    for row in maze:
        line = ""
        for col in row:
            if col == 1:
                line = line + f"{rgb(255, 255, 255)}{WALL}{RESET}"
            else:
                line = line + f"{RESET}{PATH}"
        print(padding + line, end="")
        print("")

    print("\n")


def generate_maze(rows, cols):
    grid = [[True] * cols for _ in range(rows)]

    def carve(r, c):
        grid[r][c] = False
        draw(grid)
        time.sleep(0.1)
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                grid[r + dr//2][c + dc//2] = False
                carve(nr, nc)

    carve(1, 1)
    draw(grid)
    return grid


if __name__ == "__main__":
    generate_maze(21, 21)
