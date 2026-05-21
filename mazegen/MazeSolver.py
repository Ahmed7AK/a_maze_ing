from .OutputHandler import OutputHandler


class MazeSolver:
    def __init__(self, maze, conf):
        self.maze = maze
        self.rows = conf["HEIGHT"] * 2 + 1
        self.cols = conf["WIDTH"] * 2 + 1
        self.start = (conf["ENTRY"][1] * 2 + 1, conf["ENTRY"][0] * 2 + 1)
        self.end = (conf["EXIT"][1] * 2 + 1, conf["EXIT"][0] * 2 + 1)
        self.visited = set()
        self.output = OutputHandler(conf["OUTPUT_FILE"])

    def solve(self, output_handler):
        self.search(self.start[0], self.start[1], output_handler)
        self.output.save_solution_path()
        return self.maze

    def search(self, r, c, output_handler):
        if (r, c) == self.end:
            self.maze[r][c].solution = True
            return True

        self.visited.add((r, c))
        self.maze[r][c].searching = True

        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc
            wall_r = r + dr
            wall_c = c + dc
            if (0 <= nr < self.rows and 0 <= nc < self.cols) and \
                (nr, nc) not in self.visited and \
                not self.maze[nr][nc].wall and \
                    not self.maze[wall_r][wall_c].wall:
                self.visited.add((wall_r, wall_c))
                if self.search(nr, nc, output_handler):
                    self.maze[r][c].solution = True
                    self.maze[r][c].searching = False
                    self.output.add_move(dr, dc)
                    return True

        self.maze[r][c].searching = False
        return False
