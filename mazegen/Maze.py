import random
import time
import os
from .Cell import Cell

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0m"
WALL = "\u2588\u2588"
PATH = "  "


class MazeGenerator:
    '''This class contains all the methods required to generate the maze'''
    def __init__(self, config: dict) -> None:
        '''When initialized configuration is passed and used in the class'''
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
        self.create_maze()

    def create_maze(self) -> list[list[Cell]]:
        '''Creates the base empty maze'''
        self.maze = []
        for y in range(self._height * 2 + 1):
            row = []
            for x in range(self._width * 2 + 1):
                wall = Cell(True)
                if x == 0 or y == 0:
                    row.append(wall)
                elif x == self._width * 2 or y == self._height * 2:
                    row.append(wall)
                else:
                    row.append(wall)
            self.maze.append(row)
        self.maze[self._entry[1] * 2 + 1][self._entry[0] * 2 + 1].entry = True
        self.maze[self._exit[1] * 2 + 1][self._exit[0] * 2 + 1].exit = True
        return self.maze

    def forty_two_pattern(self) -> None:
        '''Handles showcasing the forty-two pattern if possible'''
        if self._width < 13 or self._height < 11:
            print("Maze is too small to acomodate 42 pattern")
            return

        mid_r = (self._height // 2) * 2 + 1
        mid_c = (self._width // 2) * 2 + 1

        cells_4 = [
            (-4, -6), (-2, -6), (0, -6),
            (0, -4),
            (0, -2), (2, -2), (4, -2)
        ]
        cells_2 = [
            (-4, 2), (-4, 4), (-4, 6),
            (-2, 6),
            (0, 2), (0, 4), (0, 6),
            (2, 2),
            (4, 2), (4, 4), (4, 6)
        ]

        set_4 = {(mid_r + dr, mid_c + dc) for dr, dc in cells_4}
        set_2 = {(mid_r + dr, mid_c + dc) for dr, dc in cells_2}
        all_pattern_cells = set_4.union(set_2)

        for r, c in all_pattern_cells:
            self.maze[r][c].wall = False
            self.maze[r][c].protect = True

        for r, c in all_pattern_cells:
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                wall_r, wall_c = r + dr, c + dc
                neighbor_r, neighbor_c = r + 2 * dr, c + 2 * dc

                if (r, c) in set_4 and (neighbor_r, neighbor_c) in set_4:
                    self.maze[wall_r][wall_c].wall = True
                    self.maze[wall_r][wall_c].protect = True
                elif (r, c) in set_2 and (neighbor_r, neighbor_c) in set_2:
                    self.maze[wall_r][wall_c].wall = True
                    self.maze[wall_r][wall_c].protect = True
                elif (neighbor_r, neighbor_c) not in all_pattern_cells:
                    self.maze[wall_r][wall_c].wall = True
                    self.maze[wall_r][wall_c].protect = True

    def generate_maze(self) -> None:
        '''
        Uses a backtracking DFS algorithm that carves a path through the maze.
        The maze is perfect by default as a result of the algorithm used.
        '''
        self.forty_two_pattern()

        def carve(r, c):
            self.maze[r][c].wall = False
            dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            self._rng.shuffle(dirs)
            self.draw_maze()
            time.sleep(0.02)
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self._height * 2 + 1 and \
                   0 <= nc < self._width * 2 + 1 and \
                   self.maze[nr][nc].wall and \
                   not self.maze[nr][nc].protect:
                    self.maze[r + dr//2][c + dc//2].wall = False
                    carve(nr, nc)
        carve(1, 1)
        self.make_loops()

    def make_loops(self) -> None:
        '''
        This method turns the perfect maze, imperfect by adding loops.
        The loops open up multiple paths possible making the maze imperfect.
        '''
        if self._perfect:
            return

        internal_walls = []
        for r in range(1, self._height * 2):
            for c in range(1, self._width * 2):
                is_horizontal_wall = (r % 2 == 0 and c % 2 != 0)
                is_vertical_wall = (r % 2 != 0 and c % 2 == 0)

                if (is_horizontal_wall or is_vertical_wall):
                    if self.maze[r][c].wall and not self.maze[r][c].protect:
                        internal_walls.append((r, c))

        self._rng.shuffle(internal_walls)

        target_removals = max(1, len(internal_walls) // 10)
        removed = 0

        for r, c in internal_walls:
            if removed >= target_removals:
                break

            self.maze[r][c].wall = False

            if self._forms_3x3(r, c):
                self.maze[r][c].wall = True
            else:
                removed += 1

    def _forms_3x3(self, r: int, c: int) -> None:
        '''
        This is used to check if the make_loops() function
        produced an invalid maze as specified in the subject
        '''
        for start_r in range(r - 2, r + 1):
            for start_c in range(c - 2, c + 1):
                if start_r < 1 or start_r + 2 >= self._height * 2:
                    continue
                if start_c < 1 or start_c + 2 >= self._width * 2:
                    continue

                is_3x3_empty = True
                for i in range(3):
                    for j in range(3):
                        if self.maze[start_r + i][start_c + j].wall:
                            is_3x3_empty = False
                            break
                    if not is_3x3_empty:
                        break

                if is_3x3_empty:
                    return True

        return False

    def draw_maze(self, show_path=False, color="\033[37m") -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.maze:
            for col in row:
                if col.player:
                    print(f"{BLUE}{WALL}{RESET}", end="")
                elif col.entry or col.exit:
                    print(f"{RED}{WALL}{RESET}", end="")
                elif col.protect and not col.wall:
                    print(f"{YELLOW}{WALL}{RESET}", end="")
                elif col.wall:
                    print(f"{color}{WALL}{RESET}", end="")
                elif col.searching:
                    print(f"{RED}{WALL}{RESET}", end="")
                elif col.solution and show_path:
                    print(f"{GREEN}{WALL}{RESET}", end="")
                else:
                    print("  ", end="")
            print()
