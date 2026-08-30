from typing import List, Tuple, Dict
from dataclasses import dataclass
from collections import deque
import random


N: int = 1
E: int = 2
S: int = 4
W: int = 8

DIRS: Dict[int, Tuple[int, int]] = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}

OPPOSITE: Dict[int, int] = {
    N: S,
    S: N,
    E: W,
    W: E
}


@dataclass
class Cell:
    """
    Represents a single cell in the maze grid.

    Attributes:
        north, east, south, west (bool):
        True if the north wall exists, False if removed.
        is_42 (bool): True if the cell is part of the "42" pattern in the maze.
    """

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True
    is_42: bool = False


class MazeGenerator:
    """Maze generator that creates a grid with optional perfect paths
    and special '42' marking for large mazes.
    """

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool, seed: int | None = None,
                 ) -> None:
        """
        Initialize the maze generator with dimensions, entry/exit points,
        perfect maze flag, and optional random seed.

        Args:
            width: Width of the maze (number of columns).
            height: Height of the maze (number of rows).
            entry: Coordinates of the entry cell (x, y).
            exit: Coordinates of the exit cell (x, y).
            perfect: If True, maze will have a single unique path.
            seed: Optional seed for random number generation.
        """
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect: bool = perfect
        self.seed: int | None = seed

        # Initialize grid with default Cell instances
        self.grid: list[list[Cell]] = [
            [Cell() for _ in range(width)] for _ in range(height)]

    def dir_to_attr(self, direction: int) -> str:
        """
        Convert a direction bitmask to the corresponding Cell attribute name.

        Args:
            direction: One of N=1, E=2, S=4, W=8.

        Returns:
            The attribute name as a string: 'north', 'east', 'south', or 'west'
        """
        return {N: 'north', E: 'east', S: 'south', W: 'west'}[direction]

    def get_neighbors(self,
                      cell: tuple[int, int], visited: set[tuple[int, int]]
                      ) -> list[tuple[tuple[int, int], int]]:
        """
        Get all valid neighboring cells for a given cell that are not visited
        and not part of the '42' pattern.

        Args:
            cell: Coordinates (x, y) of the current cell.
            visited: Set of already visited coordinates.

        Returns:
            A list of tuples containing neighbor coordinates and the
            direction from the current cell as an int (N=1, E=2, S=4, W=8).
        """
        x, y = cell
        neighbors: list[tuple[tuple[int, int], int]] = []

        for direction, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < self.width and
                0 <= ny < self.height and
                (nx, ny) not in visited and
                not self.grid[ny][nx].is_42
            ):
                neighbors.append(((nx, ny), direction))

        return neighbors

    def remove_wall(self, current: tuple[int, int], neighbor: tuple[int, int],
                    direction: int) -> None:
        """
        Remove the wall between the current cell and its neighbor
        in the specified direction, updating both cells.

        Args:
            current: Coordinates (x, y) of the current cell.
            neighbor: Coordinates (x, y) of the neighbor cell.
            direction: 'N', 'E', 'S', or 'W' representing the direction
                    from the current cell to the neighbor.
        """

        cx, cy = current
        nx, ny = neighbor

        setattr(self.grid[cy][cx], self.dir_to_attr(direction), False)
        setattr(self.grid[ny][nx], self.dir_to_attr(OPPOSITE[direction]
                                                    ), False)

    def dfs_algorithm(self) -> None:
        """
        Generate maze paths using depth-first search.

        The algorithm starts from the entry cell and explores neighbors
        randomly, removing walls to carve paths. Backtracks when no
        unvisited neighbors remain.

        Raises:
            RuntimeError: If neighbor retrieval or wall removal fails.
        """

        try:
            stack: list[tuple[int, int]] = [self.entry]
            visited: set[tuple[int, int]] = set([self.entry])

            while stack:
                current: tuple[int, int] = stack[-1]
                neighbors = self.get_neighbors(current, visited)
                if neighbors:
                    next_cell, direction = random.choice(neighbors)
                    self.remove_wall(current, next_cell, direction)
                    visited.add(next_cell)
                    stack.append(next_cell)
                else:
                    stack.pop()
        except Exception as e:
            raise RuntimeError(f"DFS algorithm failed: {e}") from e

    def exit_or_entry_in_42(self) -> None:
        """
        Ensure that the maze entry and exit are not inside the '42' pattern.

        Raises:
            ValueError: If the entry or exit is located inside the '42' cells.
        """
        ex, ey = self.entry
        xx, xy = self.exit

        if self.grid[ey][ex].is_42:
            raise ValueError("Entry inside 42!")

        if self.grid[xy][xx].is_42:
            raise ValueError("Exit inside 42!")

    def generate(self) -> None:
        """
        Generate the maze grid.

        Steps:
            1. Set the random seed for reproducibility.
            2. If the maze is large enough, mark the '42' pattern and
            possibly adjust entry/exit positions inside it.
            3. Build the maze using the depth-first search algorithm.
            4. If the maze is not perfect, add an additional safe path
            at the entry and exit.

        Raises:
            RuntimeError: If maze generation fails for any reason.
        """

        try:
            random.seed(self.seed)

            if self.width >= 10 and self.height >= 10:
                self.mark_42()
                self.exit_or_entry_in_42()

            self.dfs_algorithm()

            if not self.perfect:
                self.add_mor_safe_path()

        except Exception as e:
            raise RuntimeError(f"Error during maze generation: {e}") from e

    def block_first_path(self, path: List[Tuple[int, int]]) -> None:
        """
        Close the first step of a given path in the maze to force
        BFS to find an alternative route.

        Args:
            path: List of coordinates [(x, y), ...] representing a path.

        Returns:
            None
        """

        x1, y1 = path[0]
        x2, y2 = path[1]

        entry_cell: Cell = self.grid[y1][x1]
        next_cell: Cell = self.grid[y2][x2]

        if x2 == x1 + 1:  # East
            entry_cell.east = True
            next_cell.west = True
        elif x2 == x1 - 1:  # West
            entry_cell.west = True
            next_cell.east = True
        elif y2 == y1 + 1:  # South
            entry_cell.south = True
            next_cell.north = True
        elif y2 == y1 - 1:  # North
            entry_cell.north = True
            next_cell.south = True

    def add_mor_safe_path(self) -> None:
        """Open walls around the entry cell safely without touching 42 cells.

        This function checks all four directions (east, south, west, north)
        around the entry cell and removes walls if the neighboring cell is
        not part of the 42 pattern and the wall exists.

        Returns:
            None
        """
        ex, ey = self.entry
        entry_cell: Cell = self.grid[ey][ex]

        # Open walls in all four directions if safe
        if (
            ex + 1 < self.width and not
            self.grid[ey][ex+1].is_42 and entry_cell.east
        ):
            entry_cell.east = False
            self.grid[ey][ex+1].west = False

        if (
            ey + 1 < self.height and not
            self.grid[ey+1][ex].is_42 and entry_cell.south
        ):
            entry_cell.south = False
            self.grid[ey+1][ex].north = False

        if ex - 1 >= 0 and not self.grid[ey][ex - 1].is_42 and entry_cell.west:
            entry_cell.west = False
            self.grid[ey][ex - 1].east = False

        if ey - 1 >= 0 and not self.grid[ey-1][ex].is_42 and entry_cell.north:
            entry_cell.north = False
            self.grid[ey - 1][ex].south = False

    def cell_to_hex(self, cell: Cell) -> str:
        """
        Convert a maze cell to a hexadecimal value.

        Each wall direction corresponds to a bit value:
            north = 1
            east  = 2
            south = 4
            west  = 8

        Args:
            cell: The cell object representing maze walls.

        Returns:
            str: Hexadecimal representation of the cell.
        """
        value: int = 0

        if cell.north:
            value += N
        if cell.east:
            value += E
        if cell.south:
            value += S
        if cell.west:
            value += W

        return format(value, "X")

    def path_to_directions(self, path: list[tuple[int, int]]) -> str:
        """
        Convert a path of coordinates into movement directions.

        Args:
            path: List of (x, y) coordinates representing the solution path.

        Returns:
            str: String of directions using N, S, E, W.
        """
        directions: list[str] = []

        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]

            if x2 == x1 + 1:
                directions.append("E")
            elif x2 == x1 - 1:
                directions.append("W")
            elif y2 == y1 + 1:
                directions.append("S")
            elif y2 == y1 - 1:
                directions.append("N")

        return "".join(directions)

    def save_all(self, filename: str, path: list[tuple[int, int]]) -> None:
        """
        Save the maze, entry/exit coordinates, and solution path to a file.

        Args:
            filename: Path to the output file.
            path: List of coordinates representing the solution path.

        Raises:
            OSError: If the file cannot be written.
        """
        try:
            with open(filename, "w") as f:
                for row in self.grid:
                    line = "".join(self.cell_to_hex(cell) for cell in row)
                    f.write(line + "\n")

                f.write("\n")

                ex, ey = self.entry
                fx, fy = self.exit

                f.write(f"{ex},{ey}\n")
                f.write(f"{fx},{fy}\n")

                directions: str = self.path_to_directions(path)
                f.write(directions + "\n")

        except OSError as e:
            raise OSError(f"Error writing file {filename}") from e

    def mark_42(self) -> None:
        """
        Mark cells forming the number '42' in the center of the maze.

        The function calculates the middle of the grid and marks specific
        coordinates so that the shape of "42" appears in the maze.
        """

        mid_x: int = self.width // 2
        mid_y: int = self.height // 2

        coords: List[Tuple[int, int]] = [
            # "4"
            (mid_x - 4, mid_y - 2),
            (mid_x - 4, mid_y - 1),
            (mid_x - 4, mid_y),
            (mid_x - 3, mid_y),
            (mid_x - 2, mid_y - 2),
            (mid_x - 2, mid_y - 1),
            (mid_x - 2, mid_y),
            (mid_x - 2, mid_y + 1),
            (mid_x - 2, mid_y + 2),

            # "2"
            (mid_x,     mid_y - 2),
            (mid_x + 1, mid_y - 2),
            (mid_x + 2, mid_y - 2),
            (mid_x + 2, mid_y - 1),
            (mid_x,     mid_y),
            (mid_x + 1, mid_y),
            (mid_x + 2, mid_y),
            (mid_x,     mid_y + 1),
            (mid_x,     mid_y + 2),
            (mid_x + 1, mid_y + 2),
            (mid_x + 2, mid_y + 2),
        ]

        for x, y in coords:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x].is_42 = True

    def bfs_shortest_path(self) -> List[Tuple[int, int]]:
        """
        Find the shortest path between entry and exit using BFS.

        Returns:
            List[Tuple[int, int]]: List of coordinates representing
            the shortest path from entry to exit.
        """
        start: Tuple[int, int] = self.entry
        end: Tuple[int, int] = self.exit

        queue: deque = deque([start])
        visited: set[Tuple[int, int]] = {start}
        parent: dict[Tuple[int, int], Tuple[int, int] | None] = {start: None}

        while queue:
            current = queue.popleft()

            if current == end:
                break

            x, y = current
            cell: Cell = self.grid[y][x]

            neighbors: list[Tuple[int, int]] = []

            if not cell.north:
                neighbors.append((x, y - 1))
            if not cell.east:
                neighbors.append((x + 1, y))
            if not cell.south:
                neighbors.append((x, y + 1))
            if not cell.west:
                neighbors.append((x - 1, y))

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        path: list[Tuple[int, int]] = []
        curr: Tuple[int, int] | None = end

        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)

        path.reverse()
        return path
