class Cell:
    '''
    This class represents every cell in the maze,
    giving unique cells different attributes
    '''
    def __init__(self, is_wall: bool = False):
        self.wall = is_wall
        self.searching = False
        self.solution = False
        self.player = False
        self.protect = False
        self.entry = False
        self.exit = False
