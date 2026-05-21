*This project has been created as part of the 42 curriculum by sechavez, akheiral*

# A-Maze-ing

## Description:

This project involves building a maze generator and solver, it should take in a configuration file that dictates how everything needs to be handled and then work accordingly. For the bonus, we chose to implement the animation for drawing the maze as well as solving it, in addition to adding a mini game that allows users to control a character within the bounds of the maze.

An output file will then be generated showcasing the maze in hexadecimal format, as well as entry/exit coordinates and instructions in NSEW showing the best path to solving the maze.

We chose to use Depth First Search backtracking to create and solve the maze, it is a tree-based algorithm that checks all possible options carving a path, until it runs into a dead end at which it backtracks to a previous checkpoint to check a different path and so on and so forth. 

The generation of the maze is mostly randomized, we are told to allow users the capability regenerate the same maze using a seed, this is done by using the random library.

We chose an object-oriented approach for the maze, its 2D-list consisting of Cells. Each Cell holds different attributes allowing us to distinguish between walls, protected cells in the 42 pattern, the exit and entrance. All of this culminates in the MazeGenerator class. 

## Intructions:

The config file must be structured and formatted as follows:

| Key | Description | Example |
| :--- | :--- | :--- |
| **WIDTH** | Maze width (number of cells) | `WIDTH=20` |
| **HEIGHT** | Maze height | `HEIGHT=15` |
| **ENTRY** | Entry coordinates (x,y) | `ENTRY=0,0` |
| **EXIT** | Exit coordinates (x,y) | `EXIT=19,14` |
| **OUTPUT_FILE** | Output filename | `OUTPUT_FILE=maze.txt` |
| **PERFECT** | Is the maze perfect? | `PERFECT=True` |
| **SEED** | Used to create a unique maze | `PERFECT=True` |

```ini
# a_maze_ing configuration
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=True
# Optional
SEED=42
```

In order to run the 'A_Maze_ing' program, run the following command:

```bash
python3 a_maze_ing.py config.txt
```

Must Haves:
* No crashing at all, handle all exceptions
* Docstrings to explain code functionality
* venv, .gitignore, and Makefile
* Possible test program???

Summary:
Maze generator that takes in a config file and generates a maze, and afterwards writing the hexadecimal representation into a file.

Algorithm:
Depth First Search or backtracking is an algorithm used to generate mazes by randomly selecting cells, and going back to another cell if trapped in a corner. 

To-do:
- Make config.txt handler - akheiral
- Finish Maze Generator perfect and imperfect - akheiral
- Finish Maze solver - sechavez
- Finish Output maker - sechavez
- Finish Makefile - akheiral, sechavez
- Finish README.md - akheiral, sechavez

## Resources:
https://professor-l.github.io/mazes/ (Amazing resource for maze generation algorithms)
