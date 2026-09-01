from dataclasses import dataclass
from mazegenerator import MazeGenerator
from enum import Enum
import random
import time


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass
class Cell:
    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    pacgum: bool = False
    super_pacgum: bool = False
    player: bool = False
    ghost: bool = False


class Maze:
    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed

        self._generator = MazeGenerator(
            size=(width, height),
            perfect=False,
            seed=seed
        )

        self.cells: list[list[Cell]] = []
        self._build_cells()

    def _build_cells(self) -> None:
        for y in range(self.height):
            row: list[Cell] = []

            for x in range(self.width):
                value = self._generator.maze[y][x]

                cell = Cell(
                    north=bool(value & 1),
                    east=bool(value & 2),
                    south=bool(value & 4),
                    west=bool(value & 8),
                )

                row.append(cell)

            self.cells.append(row)

        for y in range(self.height):
            for x in range(self.width):
                if self.is_walkable(x, y):
                    self.cells[y][x].pacgum = True

        positions = [
            (1, 1),
            (self.width - 2, 1),
            (1, self.height - 2),
            (self.width - 2, self.height - 2),
        ]
        for x, y in positions:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.cells[y][x].super_pacgum = True
                self.cells[y][x].pacgum = False

    def is_walkable(self, x: int, y: int) -> bool:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False

        cell = self.cells[y][x]

        return not (
            cell.north
            and cell.east
            and cell.south
            and cell.west
        )

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        if not self.is_walkable(x, y):
            return False

        cell = self.cells[y][x]

        if direction == Direction.UP:
            return not cell.north

        if direction == Direction.RIGHT:
            return not cell.east

        if direction == Direction.DOWN:
            return not cell.south

        if direction == Direction.LEFT:
            return not cell.west

        return False

    def get_center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def get_ghost_positions(self) -> list[tuple[int, int]]:
        return [
            (2, 1),
            (self.width - 3, 1),
            (2, self.height - 2),
            (self.width - 3, self.height - 2),
        ]


class Player:
    def __init__(self, position: tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]
        self.lives = 3
        self.score = 0

    def move(self, maze: Maze, direction: Direction) -> None:
        if maze.can_move(self.x, self.y, direction):
            old_cell = maze.cells[self.y][self.x]
            if direction == Direction.UP:
                self.y -= 1
            elif direction == Direction.RIGHT:
                self.x += 1
            elif direction == Direction.DOWN:
                self.y += 1
            elif direction == Direction.LEFT:
                self.x -= 1
            new_cell = maze.cells[self.y][self.x]
            old_cell.player = False
            new_cell.player = True

    def is_dead(self) -> bool:
        return self.lives <= 0


class Ghost:
    def __init__(self, position: tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]
        self.spawn = position
        self.direction = Direction.UP
        self.edible = False
        self.edible_until = 0.0

    def move(self, maze: Maze, player: Player, ghosts: list['Ghost']) -> None:
        directions = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT
        ]

        possible = []

        for direction in directions:
            if maze.can_move(self.x, self.y, direction):
                possible.append(direction)

        if not possible:
            return

        if self.edible:
            best_direction = possible[0]
            best_distance = -1

            for direction in possible:
                x = self.x
                y = self.y

                if direction == Direction.UP:
                    y -= 1
                elif direction == Direction.RIGHT:
                    x += 1
                elif direction == Direction.DOWN:
                    y += 1
                elif direction == Direction.LEFT:
                    x -= 1

                distance = abs(x - player.x) + abs(y - player.y)

                if distance > best_distance:
                    best_distance = distance
                    best_direction = direction

            self.direction = best_direction
        else:
            self.direction = random.choice(possible)

        old_x, old_y = self.x, self.y

        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        maze.cells[self.y][self.x].ghost = True
        if not any(g for g in ghosts if g is not self and g.x == old_x and g.y == old_y):
            maze.cells[old_y][old_x].ghost = False

    def set_edible(self, duration: float = 10.0) -> None:
        self.edible = True
        self.edible_until = time.time() + duration

    def respawn(self, maze: Maze, ghosts: list['Ghost']) -> None:
        old_x, old_y = self.x, self.y
        self.x, self.y = self.spawn
        self.edible = False

        maze.cells[self.y][self.x].ghost = True
        if not any(g for g in ghosts if g is not self and g.x == old_x and g.y == old_y):
            maze.cells[old_y][old_x].ghost = False

    def update(self) -> None:
        if self.edible and time.time() >= self.edible_until:
            self.edible = False


class Game:
    def __init__(self, maze: Maze, player: Player, ghosts: list[Ghost], time_limit: int) -> None:
        self.maze = maze
        self.start_time = time.time()
        self.time_limit = time_limit
        self.player = player
        self.ghosts = ghosts
        self.level = 1

        self.maze.cells[self.player.y][self.player.x].player = True
        for ghost in self.ghosts:
            self.maze.cells[ghost.y][ghost.x].ghost = True

    def update(self, direction: Direction) -> None:
        self.player.move(self.maze, direction)

        cell = self.maze.cells[self.player.y][self.player.x]
        if cell.pacgum:
            cell.pacgum = False
            self.player.score += 10

        if cell.super_pacgum:
            cell.super_pacgum = False
            self.player.score += 50
            for ghost in self.ghosts:
                ghost.set_edible()

        if self.is_game_over():
            return

        for ghost in self.ghosts:
            ghost.update()
            ghost.move(self.maze, self.player, self.ghosts)

            if self.player.x == ghost.x and self.player.y == ghost.y:
                if ghost.edible:
                    self.player.score += 200
                    ghost.respawn(self.maze, self.ghosts)
                else:
                    self.player.lives -= 1
                    old_px, old_py = self.player.x, self.player.y
                    self.player.x, self.player.y = self.maze.get_center()
                    self.maze.cells[old_py][old_px].player = False
                    self.maze.cells[self.player.y][self.player.x].player = True
                    self.reset_ghosts()

    def level_complete(self) -> bool:
        for row in self.maze.cells:
            for cell in row:
                if cell.pacgum:
                    return False
        return True

    def time_over(self):
        return time.time() - self.start_time >= self.time_limit

    def is_game_over(self) -> bool:
        return self.player.is_dead() or self.time_over()

    def reset_ghosts(self) -> None:
        for ghost in self.ghosts:
            ghost.respawn(self.maze, self.ghosts)


