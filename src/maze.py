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
    is_42: bool = False


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

                # if (cell.north and cell.east and cell.south and cell.west):
                #     cell.is_42 = True

            self.cells.append(row)

        for y in range(self.height):
            for x in range(self.width):
                if self.is_walkable(x, y):
                    self.cells[y][x].pacgum = True

        positions = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in positions:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.cells[y][x].super_pacgum = True
                self.cells[y][x].pacgum = False

        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if (cell.north and cell.east and cell.south and cell.west):
                    cell.is_42 = True
                    cell.pacgum = False

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
            (0, 1),
            (self.width - 1, 1),
            (0, self.height - 2),
            (self.width - 1, self.height - 2),
        ]


class Player:
    def __init__(self, position: tuple[int, int], lives: int) -> None:
        self.x = position[0]
        self.y = position[1]
        self.lives = lives
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

        possible = [
            direction
            for direction in directions
            if maze.can_move(self.x, self.y, direction)
        ]

        if not possible:
            return

        dx = player.x - self.x
        dy = player.y - self.y

        if self.edible:
            toward_player = []
            if dx > 0:
                toward_player.append(Direction.RIGHT)
            elif dx < 0:
                toward_player.append(Direction.LEFT)
            
            if dy > 0:
                toward_player.append(Direction.DOWN)
            elif dy < 0:
                toward_player.append(Direction.UP)

            safe = [d for d in possible if d not in toward_player]
            if safe:
                self.direction = random.choice(safe)
            else:
                self.direction = random.choice(possible)

        else:
            chase_dir = None
            if dx == 0 and 0 < abs(dy) <= 10:
                chase_dir = Direction.DOWN if dy > 0 else Direction.UP
            elif dy == 0 and 0 < abs(dx) <= 10:
                chase_dir = Direction.RIGHT if dx > 0 else Direction.LEFT
            
            if chase_dir and chase_dir in possible:
                self.direction = chase_dir
            else:
                self.direction = random.choice(possible)

        old_x = self.x
        old_y = self.y

        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        maze.cells[self.y][self.x].ghost = True

        if not any(
            g is not self and g.x == old_x and g.y == old_y
            for g in ghosts
        ):
            maze.cells[old_y][old_x].ghost = False


















    def set_edible(self, duration: float = 1999999999999999999999995.0) -> None:
        self.edible = True
        self.edible_until = time.time() + duration

    def respawn(self, maze: Maze, ghosts: list['Ghost']) -> None:
        old_x, old_y = self.x, self.y
        self.x, self.y = self.spawn
        self.edible = False

        maze.cells[self.y][self.x].ghost = True
        #  check this line >> if ...
        if not any(g for g in ghosts if g is not self and g.x == old_x and g.y == old_y):
            maze.cells[old_y][old_x].ghost = False

    def update(self) -> None:
        if self.edible and time.time() >= self.edible_until:
            self.edible = False


class Game:
    def __init__(self, maze: Maze, player: Player, ghosts: list[Ghost], time_limit: int, pacgum_score: int, super_pacgum_score: int, ghost_score: int) -> None:
        self.level = 1
        self.maze = maze
        self.player = player
        self.ghosts = ghosts
        self.start_time = time.time()

        self.time_limit = time_limit
        self.ghost_score = ghost_score
        self.pacgum_score = pacgum_score
        self.super_pacgum_score = super_pacgum_score

        self.maze.cells[self.player.y][self.player.x].player = True
        for ghost in self.ghosts:
            self.maze.cells[ghost.y][ghost.x].ghost = True

    def update(self, direction: Direction) -> None:
        self.player.move(self.maze, direction)
        cell = self.maze.cells[self.player.y][self.player.x]

        self.check_pacgum_eating(cell)
        self.check_super_pacgum_eating(cell)

        if self.is_game_over():
            return

        for ghost in self.ghosts:
            self.check_ghost_position(ghost)

            ghost.update()
            ghost.move(self.maze, self.player, self.ghosts)

            self.check_ghost_position(ghost)

    def check_ghost_position(self, ghost: Ghost) -> None:
        if self.player.x == ghost.x and self.player.y == ghost.y:
            if ghost.edible:
                self.eat_ghost(ghost)
            else:
                self.eat_player()

    def eat_ghost(self, ghost: Ghost) -> None:
        self.player.score += self.ghost_score
        ghost.respawn(self.maze, self.ghosts)

    def eat_player(self) -> None:
        self.player.lives -= 1

        old_x, old_y = self.player.x, self.player.y
        self.player.x, self.player.y = self.maze.get_center()

        self.maze.cells[old_y][old_x].player = False
        self.maze.cells[self.player.y][self.player.x].player = True

        self.reset_ghosts()

    def check_pacgum_eating(self, cell: Cell) -> None:
        if cell.pacgum:
            cell.pacgum = False
            self.player.score += self.pacgum_score

    def check_super_pacgum_eating(self, cell: Cell) -> None:
        if cell.super_pacgum:
            cell.super_pacgum = False
            self.player.score += self.super_pacgum_score

            for ghost in self.ghosts:
                ghost.set_edible()

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
