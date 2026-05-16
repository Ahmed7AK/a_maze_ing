class Maze:
    def __init__(self, config: dict):
        if not config:
            raise Exception("Configuration Error")

        self._width = config["WIDTH"]
        self._height = config["HEIGHT"]
        if self._width <= 2 or self._height <= 2:
            raise Exception("Maze must have a width and height > 2")

        self._entry = tuple(config["ENTRY"].split(","))
        self._exit = tuple(config["EXIT"].split(","))
        self._output_file = config["OUTPUT_FILE"]
        if config["PERFECT"] == "False":
            self._perfect = False
        else:
            self._perfect = True
        self._seed = config["SEED"]