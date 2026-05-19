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
        for y in range(self._height + 2):
            row = []
            for x in range(self._width + 2):
                wall = Cell(True)
                if x == 0 or y == 0:
                    wall.protect = True
                    row.append(wall)
                elif x == self._width + 1 or y == self._height + 1:
                    wall.protect = True
                    row.append(wall)
                else:
                    row.append(wall)
            self.maze.append(row)
        return self.maze

    def forty_two_pattern(self) -> None:
        if self._width < 8 or self._height < 6:
            print("Maze is too small to acomodate 42 pattern")
            return
        center_x = int(self._width / 2) + 1
        center_y = int(self._height / 2) + 1

        self.maze[center_y - 2][center_x - 3].protect = True
        self.maze[center_y - 2][center_x + 1].protect = True
        self.maze[center_y - 2][center_x + 2].protect = True
        self.maze[center_y - 2][center_x + 3].protect = True

        self.maze[center_y - 1][center_x - 3].protect = True
        self.maze[center_y - 1][center_x + 3].protect = True

        self.maze[center_y][center_x - 3].protect = True
        self.maze[center_y][center_x - 2].protect = True
        self.maze[center_y][center_x - 1].protect = True
        self.maze[center_y][center_x + 1].protect = True
        self.maze[center_y][center_x + 2].protect = True
        self.maze[center_y][center_x + 3].protect = True

        self.maze[center_y + 1][center_x - 1].protect = True
        self.maze[center_y + 1][center_x + 1].protect = True

        self.maze[center_y + 2][center_x - 1].protect = True
        self.maze[center_y + 2][center_x + 1].protect = True
        self.maze[center_y + 2][center_x + 2].protect = True
        self.maze[center_y + 2][center_x + 3].protect = True

    def generate_maze(self) -> None:
        self.forty_two_pattern()
        def carve(r, c):
            self.maze[r][c].wall = False
            dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            self._rng.shuffle(dirs)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self._height + 1 and \
                   0 <= nc < self._width + 1 and \
                   self.maze[nr][nc].wall and \
                   not self.maze[nr][nc].protect:
                    self.maze[r + dr//2][c + dc//2].wall = False
                    carve(nr, nc)
        carve(1, 1)


if __name__ == "__main__":
    config = {'WIDTH': 21, 'HEIGHT': 21, 'ENTRY': (0, 0), 'EXIT': (19, 14), 'OUTPUT_FILE': 'maze.txt', 'PERFECT': True, 'SEED': ''}
    mg = MazeGenerator(config)
    maze = mg.create_maze()

    mg.generate_maze()
    for row in mg.maze:
        for col in row:
            if (col, row) == config["ENTRY"] or (col, row) == config["EXIT"]:
                print("\033[31m\u2588\u2588\033[0m")
            elif col.wall and col.protect:
                print("\033[34m\u2588\u2588\033[0m", end="")
            elif col.wall:
                print("\u2588\u2588", end="")
            else:
                print("  ", end="")
        print()
