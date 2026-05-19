import random
from Cell import Cell


class MazeGenerator:
    def __init__(self, config: dict) -> None:
        if not config:
            raise Exception("Configuration Error")
        self.maze = []
        self._width = config["WIDTH"]
        self._height = config["HEIGHT"]
        self._entry = config["ENTRY"]
        self._exit = config["EXIT"]
        self._output_file = config["OUTPUT_FILE"]
        self._perfect = config["PERFECT"]
        if isinstance(config["SEED"], int):
            self._seed = config["SEED"]
        else:
            self._seed = random.randint(1, 100000)
        self._rng = random.Random(self._seed)

    def create_maze(self) -> list[list[Cell]]:
        for y in range(self._height * 2 + 1):
            row = []
            for x in range(self._width * 2 + 1):
                wall = Cell(True)
                if x == 0 or y == 0:
                    wall.protect = True
                    row.append(wall)
                elif x == self._width * 2 or y == self._height * 2:
                    wall.protect = True
                    row.append(wall)
                else:
                    row.append(wall)
            self.maze.append(row)
        self.maze[self._entry[1] + 1][self._entry[0] + 1].entry = True
        self.maze[self._exit[1] + 1][self._exit[1] + 1].exit = True
        return self.maze

    def forty_two_pattern(self) -> None:
        if self._width < 13 or self._height < 11:
            print("Maze is too small to acomodate 42 pattern")
            return

        rows = len(self.maze)
        cols = len(self.maze[0])
        mid_r = rows // 2
        mid_c = cols // 2

        self.maze[mid_r][mid_c - 2].protect = True
        self.maze[mid_r + 2][mid_c - 2].protect = True
        self.maze[mid_r + 4][mid_c - 2].protect = True
        self.maze[mid_r][mid_c - 4].protect = True
        self.maze[mid_r][mid_c - 6].protect = True
        self.maze[mid_r - 2][mid_c - 6].protect = True
        self.maze[mid_r - 4][mid_c - 6].protect = True

        self.maze[mid_r][mid_c + 2].protect = True
        self.maze[mid_r + 2][mid_c + 2].protect = True
        self.maze[mid_r + 4][mid_c + 2].protect = True
        self.maze[mid_r + 4][mid_c + 4].protect = True
        self.maze[mid_r + 4][mid_c + 6].protect = True
        self.maze[mid_r][mid_c + 4].protect = True
        self.maze[mid_r][mid_c + 6].protect = True
        self.maze[mid_r - 2][mid_c + 6].protect = True
        self.maze[mid_r - 4][mid_c + 6].protect = True
        self.maze[mid_r - 4][mid_c + 4].protect = True
        self.maze[mid_r - 4][mid_c + 2].protect = True


    def generate_maze(self) -> None:
        self.forty_two_pattern()
        def carve(r, c):
            self.maze[r][c].wall = False
            dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            self._rng.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self._height * 2 + 1 and \
                   0 <= nc < self._width * 2 + 1 and \
                   self.maze[nr][nc].wall and \
                   not self.maze[nr][nc].protect:
                    self.maze[r + dr//2][c + dc//2].wall = False
                    carve(nr, nc)
        carve(1, 1)


if __name__ == "__main__":
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    WALL = "\u2588\u2588"
    PATH = "  "

    config = {'WIDTH': 13, 'HEIGHT': 11, 'ENTRY': (0, 0), 'EXIT': (19, 14), 'OUTPUT_FILE': 'maze.txt', 'PERFECT': True, 'SEED': ''}
    mg = MazeGenerator(config)
    maze = mg.create_maze()

    mg.generate_maze()
    for row in mg.maze:
        for col in row:
            if col.entry or col.exit:
                print(f"{RED}{WALL}{RESET}", end="")
            elif col.wall and col.protect:
                print(f"{BLUE}{WALL}{RESET}", end="")
            elif col.wall:
                print(f"{WALL}", end="")
            else:
                print("  ", end="")
        print()
