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
        self._seed = config["SEED"]
        self._rng = random.Random(self._seed)

    def create_maze(self) -> list[list[Cell]]:
        for y in range(self._height + 2):
            row = []
            for x in range(self._width + 2):
                if x == 0 or y == 0:
                    row.append(Cell(True))
                elif x == self._width + 1 or y == self._height + 1:
                    row.append(Cell(True))
                else:
                    row.append(Cell(False))
            self.maze.append(row)
        return self.maze

    def forty_two_pattern(self) -> None:
        if self._width < 8 or self._height < 6:
            print("Maze is too small to acomodate 42 pattern")
            return
        center_x = int(self._width / 2) + 1
        center_y = int(self._height / 2) + 1

        self.maze[center_y - 2][center_x - 3].wall = True
        self.maze[center_y - 2][center_x + 1].wall = True
        self.maze[center_y - 2][center_x + 2].wall = True
        self.maze[center_y - 2][center_x + 3].wall = True

        self.maze[center_y - 1][center_x - 3].wall = True
        self.maze[center_y - 1][center_x + 3].wall = True

        self.maze[center_y][center_x - 3].wall = True
        self.maze[center_y][center_x - 2].wall = True
        self.maze[center_y][center_x - 1].wall = True
        self.maze[center_y][center_x + 1].wall = True
        self.maze[center_y][center_x + 2].wall = True
        self.maze[center_y][center_x + 3].wall = True

        self.maze[center_y + 1][center_x - 1].wall = True
        self.maze[center_y + 1][center_x + 1].wall = True

        self.maze[center_y + 2][center_x - 1].wall = True
        self.maze[center_y + 2][center_x + 1].wall = True
        self.maze[center_y + 2][center_x + 2].wall = True
        self.maze[center_y + 2][center_x + 3].wall = True
    
    def generate_maze(self) -> None:
        pass


if __name__ == "__main__":
    config = {'WIDTH': 20, 'HEIGHT': 15, 'ENTRY': (0, 0), 'EXIT': (19, 14), 'OUTPUT_FILE': 'maze.txt', 'PERFECT': True, 'SEED': 42}
    mg = MazeGenerator(config)
    maze = mg.create_maze()
    mg.forty_two_pattern()
    for row in maze:
        for col in row:
            if col.wall:
                print(1, end="")
            else:
                print(0, end="")
        print()
