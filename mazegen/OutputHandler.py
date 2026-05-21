class OutputHandler:
    def __init__(self, filename="output.txt"):
        self.filename = filename
        self.solution_path = []
        self._solution_dirs = {
            (1, 0): "S",
            (0, 1): "E",
            (-1, 0): "N",
            (0, -1): "W"
        }

    def save_maze_as_hex(self, maze):
        rows = len(maze)
        cols = len(maze[0])
        with open(self.filename, "w") as f:
            for r in range(1, rows, 2):
                row_hex = ""
                for c in range(1, cols, 2):
                    val = 0
                    if r - 1 < 0 or maze[r-1][c].wall:
                        val += 1
                    if c + 1 >= cols or maze[r][c+1].wall:
                        val += 2
                    if r + 1 >= rows or maze[r+1][c].wall:
                        val += 4
                    if c - 1 < 0 or maze[r][c-1].wall:
                        val += 8
                    row_hex += hex(val)[2:].upper()
                f.write(row_hex + "\n")

    @staticmethod
    def write_coords(entry, exit_t, filename="output.txt"):
        with open(filename, "a") as f:
            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_t[0]},{exit_t[1]}\n")

    def add_move(self, dr, dc):
        self.solution_path.append(self._solution_dirs[(dr, dc)])

    def save_solution_path(self):
        self.solution_path.reverse()
        with open(self.filename, "a") as f:
            f.write("".join(self.solution_path))
        self.solution_path = []
