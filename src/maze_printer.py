import random
from typing import Optional, Protocol
import time


class MazeCell(Protocol):
    """Protocol defining the interface for a maze cell.

    Attributes:
        north: Whether the north wall is present.
        south: Whether the south wall is present.
        east: Whether the east wall is present.
        west: Whether the west wall is present.
        is_42: Whether the cell is marked as a special '42' cell.
    """

    north: bool
    south: bool
    east: bool
    west: bool
    is_42: bool


def print_maze(
    grid,
    path: Optional[list[tuple[int, int]]] = None,
    show_path: bool = False,
    rand_wals: bool = False,
    is_slow: bool = True
) -> None:
    """Print a colored ASCII representation of the maze.

    Args:
        grid: 2D list of maze cells. Each cell must provide the attributes
            north, south, east, west (bool) and is_42 (bool).
        path: Optional sequence of (x, y) coordinates representing a path.
        show_path: Whether to visually highlight the given path.
        rand_wals: Whether to randomize the wall colors.
        is_slow: Whether to animate the maze printing with delays.

    Returns:
        None.
    """

    RED: str
    GREEN: str
    YELLOW: str
    RED, GREEN, YELLOW = (
        "\033[31m", "\033[32m", "\033[33m"
    )

    BG_RED: str
    BG_GREEN: str
    BG_YELLOW: str
    BG_BLUE: str
    BG_MAGENTA: str
    BG_CYAN: str
    BG_WHITE: str
    (BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE,
     BG_MAGENTA, BG_CYAN, BG_WHITE) = (
        "\033[41m", "\033[42m", "\033[43m", "\033[44m",
        "\033[45m", "\033[46m", "\033[47m"
    )
    BG_ORANGE: str
    BG_PINK: str
    BG_PURPLE: str
    BG_TURQUOISE: str
    BG_LIME: str
    BG_GOLD: str
    BG_GRAY: str

    (BG_ORANGE, BG_PINK, BG_PURPLE, BG_TURQUOISE,
     BG_LIME, BG_GOLD, BG_GRAY) = (
        "\033[48;5;208m",
        "\033[48;5;213m",
        "\033[48;5;93m",
        "\033[48;5;44m",
        "\033[48;5;118m",
        "\033[48;5;220m",
        "\033[48;5;240m"
    )

    RESET: str = "\033[0m"

    col_42: str = random.choice([
        BG_ORANGE, BG_PINK, BG_PURPLE, BG_LIME,
        BG_GOLD, BG_GRAY
    ])
    there_is_42: int = 0

    Back_ground: str = BG_TURQUOISE

    if rand_wals:
        Back_ground = random.choice([
            BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA,
            BG_WHITE, BG_CYAN
        ])

    path_set: set[tuple[int, int]] = set(path) if path else set()

    start: Optional[tuple[int, int]] = path[0] if path else None
    end: Optional[tuple[int, int]] = path[-1] if path else None

    rows: int = len(grid)
    cols: int = len(grid[0])
    Result = []
    for row in range(rows):

        top: str = "+"
        for col in range(cols):
            top += (("---"
                    if grid[row][col].north else "   ")
                    + "+")
        Result.append(top)
        if is_slow:
            time.sleep(0.03)

        mid: str = ""
        for col in range(cols):

            mid += "|" if grid[row][col].west else " "

# 👻
# 😆
# 🍏
# 🍎
#    pacgum: bool = False
#     super_pacgum: bool = False
#     player: bool = False
#     ghost: bool = False

            pos = grid[row][col]

            if pos.ghost:
                mid +=  "GST" 
            
            elif pos.player:
                mid +=  "PLR" 

            elif pos.super_pacgum:
                mid +=  "(*)"

            elif pos.pacgum:
                mid += " . "
            
            else:
                mid += "   "

            # mid += "   "

        mid += "|"
        Result.append(mid)
        if is_slow:
            time.sleep(0.03)

    bottom: str = "+"
    for col in range(cols):
        bottom += (("---" if grid[rows - 1][col].south
                    else "youness") + "+")
    Result.append(bottom)

    if there_is_42 == 0:
        print("\n\033[1;33m42 Does Not Fit in The Maze.\033[0m")

    return Result