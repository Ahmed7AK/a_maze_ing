import os


width = os.get_terminal_size().columns
maze_width = 10 * 2
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


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
print("\n")
for row in maze:
    line = ""
    for col in row:
        if col == 1:
            line = line + f"{rgb_back(255, 255, 255)}{WALL}{RESET}"
        else:
            line = line + f"{RESET}{PATH}"
    print(padding + line, end="")
    print("")

print("\n")
