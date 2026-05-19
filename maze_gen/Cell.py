class Cell:
    def __init__(self, is_wall: bool = False):
        self.wall = is_wall
        self.protect = False
        self.entry = False
        self.exit = False
    