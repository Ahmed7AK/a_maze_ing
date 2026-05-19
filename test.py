import os
import random
import time
import sys
import tty
import termios


width = os.get_terminal_size().columns
maze_width = 40 * 2
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
    # vv made animation smoother
    # vv added more if statements for maze solving
    # vv added another if statement for the player
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n")
    for row in maze:
        line = ""
        for col in row:
            if col == 1:
                line = line + f"{rgb(255, 255, 255)}{WALL}{RESET}"
            elif col == 2:
                line = line + f"{RED}{WALL}{RESET}"
            elif col == 3:
                line = line + f"{GREEN}{WALL}{RESET}"
            elif col == 4:
                line = line + f"{BLUE}{WALL}{RESET}"
            elif col == 5:
                line = line + f"{YELLOW}{WALL}{RESET}"
            else:
                line = line + f"{RESET}{PATH}"
        print(padding + line, end="")
        print("")

    print("\n")


def gen_output(grid, filename="output.txt"):
    # vv turns maze into hex only so far
    rows = len(grid)
    cols = len(grid[0])

    with open(filename, "w") as f:
        for r in range(1, rows, 2):
            row_hex = ""
            for c in range(1, cols, 2):
                val = 0
                if r - 1 < 0 or grid[r-1][c]:
                    val += 1
                if c + 1 >= cols or grid[r][c+1]:
                    val += 2
                if r + 1 >= rows or grid[r+1][c]:
                    val += 4
                if c - 1 < 0 or grid[r][c-1]:
                    val += 8

                row_hex += hex(val)[2:].upper()
            f.write(row_hex + "\n")


def add_42_sym(grid):
    rows = len(grid)
    cols = len(grid[0])
    mid_r = rows // 2
    mid_c = cols // 2

    grid[mid_r][mid_c - 2] = 5
    grid[mid_r + 2][mid_c - 2] = 5
    grid[mid_r + 4][mid_c - 2] = 5
    grid[mid_r][mid_c - 4] = 5
    grid[mid_r][mid_c - 6] = 5
    grid[mid_r - 2][mid_c - 6] = 5
    grid[mid_r - 4][mid_c - 6] = 5

    grid[mid_r][mid_c + 2] = 5
    grid[mid_r + 2][mid_c + 2] = 5
    grid[mid_r + 4][mid_c + 2] = 5
    grid[mid_r + 4][mid_c + 4] = 5
    grid[mid_r + 4][mid_c + 6] = 5
    grid[mid_r][mid_c + 4] = 5
    grid[mid_r][mid_c + 6] = 5
    grid[mid_r - 2][mid_c + 6] = 5
    grid[mid_r - 4][mid_c + 6] = 5
    grid[mid_r - 4][mid_c + 4] = 5
    grid[mid_r - 4][mid_c + 2] = 5

    return grid


def generate_maze(rows, cols):
    grid = [[True] * cols for _ in range(rows)]
    grid = add_42_sym(grid)

    def carve(r, c):
        grid[r][c] = False
        #draw(grid)
        #time.sleep(0.1)
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] is True:
                grid[r + dr//2][c + dc//2] = False
                carve(nr, nc)

    carve(1, 1)
    draw(grid)
    return grid


# added maze solver
def solve_maze(grid, filename="output.txt"):
    rows = len(grid)
    cols = len(grid[0])
    start = (1, 1)
    end = (rows - 2, cols - 2)

    visited = set()
    
    output_moves = []
        
    output_dir = {
        (1, 0): "S",
        (0, 1): "E",
        (-1, 0): "N",
        (0, -1): "W"
    }

    def search(r, c):
        if (r, c) == end:
            grid[r][c] = 3
            draw(grid)
            return 1

        if (r, c) in visited or grid[r][c] == 1:
            return 0

        visited.add((r, c))

        grid[r][c] = 2
        draw(grid)
        #time.sleep(0.1)

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            if 0 <=nr < rows and 0 <= nc < cols:
                if search(nr, nc):
                    grid[r][c] = 3
                    output_moves.append(output_dir[(dr, dc)])
                    return 1

        grid[r][c] = 0
        draw(grid)
        #time.sleep(0.1)
        return 0

    found = search(start[0], start[1])

    if found:
        draw(grid)
        
        output_moves.reverse()
        
        with open(filename, "a") as f:
            f.write("".join(output_moves) + "\n")

# key presses thru microsoft visual c runtime (just for my laptop)
def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return char

# interactive maze
def play_maze(grid):
    rows = len(grid)
    cols = len(grid[0])
    pr = 1
    pc = 1
    endr = rows - 2
    endc = cols - 2
    
    while True:
        old_val = grid[pr][pc]
        grid[pr][pc] = 4
        draw(grid)
        if (pr, pc) == (endr, endc):
            break
        grid[pr][pc] = old_val
        key = get_key()
        if key == 'q':
            break
        dr = 0
        dc = 0
        if key == 'w':
            dr = -1
        elif key == 's':
            dr = 1
        elif key == 'a':
            dc = -1
        elif key == 'd':
            dc = 1
        else: continue
        nr = pr + dr
        nc = pc + dc
        if (0 <= nr < rows and 0 <= nc < cols):
            if grid[nr][nc] != 1:
                pr, pc = nr, nc


if __name__ == "__main__":
    maze = generate_maze(51, 51)
    gen_output(maze)
    while True:
        choice = input("maze generated! 1 to play game, 2 to solve maze")
        if choice == "1":
            play_maze(maze)
        elif choice == "2":
            solve_maze(maze)
        else:
            break