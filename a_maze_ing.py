import mazegen
import sys
from random import randint


def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return
    try:
        config = mazegen.read_config(sys.argv[1])
        mg = mazegen.MazeGenerator(config)
    except Exception:
        return
    mg.generate_maze()
    show_path = False
    current_color = "\033[37m"
    output = mazegen.OutputHandler(config["OUTPUT_FILE"])
    output.save_maze_as_hex(mg.maze)
    mazegen.OutputHandler.write_coords(config["ENTRY"],
                                       config["EXIT"],
                                       config["OUTPUT_FILE"])
    mg.maze = mazegen.MazeSolver(mg.maze, config).solve(output)
    mg.draw_maze()
    while True:
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Play game")
        print("5. Quit")
        choice = input("Choice? (1-5): ")
        if choice == "1":
            mg.create_maze()
            mg.generate_maze()
            output = mazegen.OutputHandler(config["OUTPUT_FILE"])
            mg.maze = mazegen.MazeSolver(mg.maze, config).solve(output)
            mg.draw_maze()
        elif choice == "2":
            show_path = not show_path
            mg.draw_maze(show_path, current_color)
        elif choice == "3":
            r, g, b = randint(1, 255), randint(1, 255), randint(1, 255)
            current_color = rgb(r, g, b)
            mg.draw_maze(show_path, current_color)
        elif choice == "4":
            play = mazegen.PlayMaze(mg.maze, mg, config)
            play.play(show_path, current_color)
        elif choice == "5":
            return False
        else:
            print("No choose different")


if __name__ == "__main__":
    main()
