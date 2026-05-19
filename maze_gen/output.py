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

    def save_maze_as_hex(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        with open(self.filename, "w") as f:
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
    
    def add_move(self, dr, dc):
        self.solution_path.append(self._solution_dirs[(dr, dc)])
    
    def save_solution_path(self, moves_list):
        self.solution_path.reverse()
        with open(self.filename, "a") as f:
            f.write("".join(self.solution_path) + "\n")
        self.solution_path = []