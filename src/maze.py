from dataclasses import dataclass
from mazegenerator import MazeGenerator
from enum import Enum
import random
import time


class Direction(Enum):
    UP = 1
    DOWN = 3
    LEFT = 4
    RIGHT = 2


@dataclass
class Cell:
    right: bool = True
    left: bool = True
    down: bool = True
    up: bool = True

    is_42: bool = False
    ghost: bool = False
    player: bool = False
    pacgum: bool = False
    super_pacgum: bool = False


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
                    up=bool(value & 1),
                    right=bool(value & 2),
                    down=bool(value & 4),
                    left=bool(value & 8),
                )

                row.append(cell)

                if (cell.up and cell.right and cell.down and cell.left):
                    cell.is_42 = True

            self.cells.append(row)

        for y in range(self.height):
            for x in range(self.width):
                if self.is_walkable(x, y) and not self.cells[y][x].is_42:
                    self.cells[y][x].pacgum = True

        super_pacgum_positions = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in super_pacgum_positions:
            self.cells[y][x].super_pacgum = True
            self.cells[y][x].pacgum = False

    def is_walkable(self, x: int, y: int) -> bool:
        cell = self.cells[y][x]

        return not (
            cell.up
            and cell.right
            and cell.down
            and cell.left
        )

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        if not self.is_walkable(x, y):
            return False

        cell = self.cells[y][x]

        if direction == Direction.UP:
            return not cell.up

        if direction == Direction.RIGHT:
            return not cell.right

        if direction == Direction.DOWN:
            return not cell.down

        if direction == Direction.LEFT:
            return not cell.left

        return False

    def get_center_maze(self) -> tuple[int, int]:
        x, y = self.width // 2, self.height // 2
        centre = self.cells[y][x]

        if centre.right and centre.up and centre.down and centre.left:
            return (self.width - 1) // 2, self.height // 2
        return x, y

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

        self.score = 0
        self.lives = lives
        self.is_invincibility = False

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
        self.edible = False
        self.spawn = position
        self.respawn_at = 0.0
        self.edible_until = 0.0
        self.direction = Direction.UP

    def move(self, maze: Maze, player: Player, ghosts: list['Ghost']) -> None:
        directions = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT
        ]

        possible = [
            direction for direction in directions
            if maze.can_move(self.x, self.y, direction)
        ]

        if not possible:
            print("NOT POSSIBLE")
            return

        dx = player.x - self.x
        dy = player.y - self.y

        chase = None

        if not self.edible:
            if dx == 0 and 0 < abs(dy) <= 5:
                chase = Direction.DOWN if dy > 0 else Direction.UP
            elif dy == 0 and 0 < abs(dx) <= 5:
                chase = Direction.RIGHT if dx > 0 else Direction.LEFT

        if self.edible:
            if abs(dx) <= 5 and abs(dy) <= 5:
                away = []

                if dx > 0:
                    away.append(Direction.LEFT)
                elif dx < 0:
                    away.append(Direction.RIGHT)

                if dy > 0:
                    away.append(Direction.UP)
                elif dy < 0:
                    away.append(Direction.DOWN)

                choices = [d for d in possible if d in away]

                if choices:
                    self.direction = random.choice(choices)
                elif self.direction not in possible:
                    self.direction = random.choice(possible)

            elif self.direction not in possible:
                self.direction = random.choice(possible)

        elif chase in possible:
            self.direction = chase

        elif self.direction not in possible:
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

    def set_edible(self, duration: float = 15.0) -> None:
        self.edible = True
        self.edible_until = time.time() + duration

    def respawn(self, maze: Maze, ghosts: list['Ghost']) -> None:
        old_x, old_y = self.x, self.y
        self.x, self.y = self.spawn
        self.edible = False

        #  check this line >> if ...
        # had l if ila kano joj d lghost f balsa o klahom plyer yaklhom bjoj
        if not any(g for g in ghosts if g is not self and g.x == old_x and g.y == old_y):
            maze.cells[old_y][old_x].ghost = False
        if not self.respawn_at:
            maze.cells[self.y][self.x].ghost = True

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

        self.player_count = 0
        self.ghost_count = 0
        self.player_direction = Direction.UP
        self.ghost_freeze = False
        self.time_limit = time_limit
        self.ghost_score = ghost_score
        self.pacgum_score = pacgum_score
        self.super_pacgum_score = super_pacgum_score

        self.maze.cells[self.player.y][self.player.x].player = True
        self.maze.cells[self.player.y][self.player.x].pacgum = False
        for ghost in self.ghosts:
            self.maze.cells[ghost.y][ghost.x].ghost = True

    def update(self, direction: Direction, player_speed: int = 50, ghost_speed: int = 50) -> None:

        if self.maze.can_move(self.player.x, self.player.y , direction):
            self.player_direction = direction

        self.player_count += player_speed

        self.ghost_count += ghost_speed // 2 if any(
            ghost.edible for ghost in self.ghosts
        ) else ghost_speed

        if self.player_count >= 100:
            self.player.move(self.maze, self.player_direction)
            self.player_count -= 100

            cell = self.maze.cells[self.player.y][self.player.x]
            self.check_pacgum_eating(cell)
            self.check_super_pacgum_eating(cell)

            for ghost in self.ghosts:
                self.check_ghost_position(ghost)

        if self.is_game_over():
            return

        if self.ghost_count >= 100:
            for ghost in self.ghosts:
                self.check_ghost_position(ghost)

                ghost.update()

                if ghost.respawn_at:
                    if time.time() >= ghost.respawn_at:
                        ghost.respawn_at = 0.0
                        ghost.respawn(self.maze, self.ghosts)
                    continue

                if not self.ghost_freeze:
                    ghost.move(self.maze, self.player, self.ghosts)

                self.check_ghost_position(ghost)

            self.ghost_count -= 100

    def check_ghost_position(self, ghost: Ghost) -> None:
        if ghost.respawn_at:
            return

        if self.player.x == ghost.x and self.player.y == ghost.y:
            if ghost.edible:
                self.eat_ghost(ghost)
            elif not self.player.is_invincibility:
                self.eat_player()

    def eat_ghost(self, ghost: Ghost) -> None:
        self.player.score += self.ghost_score
        ghost.respawn_at = time.time() + 3
        ghost.respawn(self.maze, self.ghosts)

    def eat_player(self) -> None:
        self.player.lives -= 1

        old_x, old_y = self.player.x, self.player.y
        self.player.x, self.player.y = self.maze.get_center_maze()

        self.maze.cells[old_y][old_x].player = False
        self.maze.cells[self.player.y][self.player.x].player = True

        self.reset_ghosts()

    def cheat_mode(self, invincible=False, ghost_freeze=False, extra_lives=0, fast_mode=False):
        if invincible:
            self.player.is_invincibility = True
        if ghost_freeze:
            self.ghost_freeze = True
        if extra_lives:
            self.player.lives += extra_lives
        if fast_mode:
            self.player_count += 100

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
