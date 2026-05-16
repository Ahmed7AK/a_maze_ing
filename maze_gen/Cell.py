class Cell:
    def __init__(self, is_wall: bool = False):
        self.wall = is_wall
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
    