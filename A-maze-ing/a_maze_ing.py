from parser import Settings
from mazegen.maze import MazeGenerator, Cell
from maze_printer import print_maze
import os
import sys
import time
import copy
from enum import IntEnum
from typing import Optional, cast
import traceback

REGENERAT: IntEnum
PATH: IntEnum
OTHERPATH: IntEnum
CHANGEWALSCOLOR: IntEnum
STEPBACK: IntEnum
EXIT: IntEnum


class Options(IntEnum):
    """Enum representing menu options for maze interaction.

    Attributes:
        REGENERAT: Regenerate the maze.
        SHORTPATH: Show the shortest path.
        HIDEPATH: Hide the current path.
        STEPBACK: Step back to the previous menu.
        CHANGEWALSCOLOR: Change the wall color.
        OTHERPATH: Display an alternative path.
        EXIT: Exit the program.
    """

    REGENERAT = 1
    PATH = 2
    OTHERPATH = 3
    CHANGEWALSCOLOR = 4
    STEPBACK = 5
    EXIT = 6


def maze_result(onece: int) -> None:
    """Run the maze_result maze interaction loop.

    Initializes maze settings, generates the maze, computes paths,
    and presents an interactive menu for the user to explore the maze.

    Args:
        onece: An integer controlling the animation and banner display.
            Pass 0 on first launch to show the start banner and animate
            the menu; pass 1 to skip the banner.

    Returns:
        None.

    Raises:
        ValueError: If onece is not of type int.
    """
    if not isinstance(onece, int):
        raise ValueError("The arg 'onece' sould be of type (int)")

    settings: Settings = Settings(_env_file=sys.argv[1])  # type: ignore

    maze: MazeGenerator = MazeGenerator(
        settings.WIDTH,
        settings.HEIGHT,
        cast(tuple[int, int], settings.ENTRY),
        cast(tuple[int, int], settings.EXIT),
        settings.PERFECT,
        settings.SEED
    )

    maze.generate()
    path1: list[tuple[int, int]] = maze.bfs_shortest_path()
    old_grid: list[list[Cell]] = copy.deepcopy(maze.grid)

    path2: Optional[list[tuple[int, int]]] = None
    if not maze.perfect:
        maze.block_first_path(path1)
        path2 = maze.bfs_shortest_path()

    maze.save_all(settings.OUTPUT_FILE, path1)

    if onece == 0:
        print_banner("body/start_banner.txt")
        time.sleep(5)
        onece = 1

    show_path: bool = False
    chng_wal_col: bool = False
    is_slow: bool = True
    NUM_COLOR: str = "\033[33m"
    TEXT_COLOR: str = "\033[35m"
    INPUT_COLOR: str = "\033[36m"
    temp_path: list[tuple[int, int]] = path1
    word: str = (
        "1) Regenerat\t2) Show/Hide Path    3) The other Path\t4)"
        " Change Wals Color\t5)Step Back\t6) Exit ? \n\n"
    )

    while True:
        os.system('clear')
        print_maze(old_grid, temp_path, show_path, chng_wal_col, is_slow)
        temp_path = path1
        print("\n")

        char: str
        for char in word:
            if char.isdigit():
                print(f"{NUM_COLOR}{char}{TEXT_COLOR}", end="", flush=True)
            else:
                print(char, end="", flush=True)
            if onece == 1:
                time.sleep(0.03)
        onece = 2
        print("===> " + INPUT_COLOR + "", end="")

        option: int = int(input())
        chng_wal_col = False
        is_slow = False

        if option == Options.REGENERAT:
            maze_result(1)
        elif option == Options.PATH:
            if show_path:
                show_path = False
            else:
                show_path = True
        elif option == Options.STEPBACK:
            break
        elif option == Options.CHANGEWALSCOLOR:
            chng_wal_col = True
        elif option == Options.OTHERPATH:
            if not maze.perfect and path2 is not None:
                temp_path = path2
                show_path = True
            else:
                print("\nMAZE Is PERFECT So there is only one Path :_( ")
                time.sleep(5)
        elif option == Options.EXIT:
            os.system('clear')
            print_banner("body/end_banner.txt")
            sys.exit(0)


def print_banner(path_file: str) -> None:
    """Display a banner from a text file in yellow color.

    Args:
        path_file: The file path to the banner text file.

    Returns:
        None.
    """

    os.system('clear')
    YELLOW: str = '\033[33m'
    RESET: str = '\033[0m'
    try:
        with open(path_file) as file_handle:
            banner: str = file_handle.read()
        print(YELLOW + banner + RESET)
    except FileNotFoundError:
        print(f"{YELLOW}[!] Banner file not found{RESET}")
    except Exception as e:
        print(f"{YELLOW}[!] Error loading banner: {e}{RESET}")


def main() -> None:
    """Entry point of the program.

    Calls maze_result to launch the maze interaction loop,
    and prints the full traceback if any exception occurs.
    """
    try:
        maze_result(0)
    except Exception:
        print('\033[31m' + traceback.format_exc())


if __name__ == "__main__":
    main()
