import sys
import tty
import termios


class PlayMaze:
    def __init__(self, maze, mg, conf):
        self.maze = maze
        self.mg = mg
        self.rows = conf["HEIGHT"] * 2 + 1
        self.cols = conf["WIDTH"] * 2 + 1
        self.playerr = conf["ENTRY"][1] * 2 + 1
        self.playerc = conf["ENTRY"][0] * 2 + 1
        self.end = (conf["EXIT"][1] * 2 + 1, conf["EXIT"][0] * 2 + 1)

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

    def play(self, path, color):
        while True:
            self.maze[self.playerr][self.playerc].player = True
            self.mg.draw_maze()
            if (self.playerr, self.playerc) == (self.end):
                break
            self.maze[self.playerr][self.playerc].player = False
            key = self.get_key()
            if key == 'q':
                break
            dr = 0
            dc = 0
            if key == 'w':
                print("pressing w")
                dr = -1
            elif key == 's':
                dr = 1
            elif key == 'a':
                dc = -1
            elif key == 'd':
                dc = 1
            else:
                continue
            nr = self.playerr + dr
            nc = self.playerc + dc
            if (0 <= nr < self.rows and 0 <= nc < self.cols):
                if not self.maze[nr][nc].wall:
                    self.playerr, self.playerc = nr, nc
