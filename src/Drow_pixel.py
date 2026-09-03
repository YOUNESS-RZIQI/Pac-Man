"""Graphic maze renderer using MLX image-buffer drawing.

Renders the A-Maze-ing maze into an MLX image (instead of ASCII), reusing
the image drawing logic from Drow_pixel.py: draw into an image buffer, then
mlx_put_image_to_window every frame.
"""
import sys
import time

from mlx import Mlx
from maze import Maze, Player, Ghost, Game, Direction

# --- Window / cell sizing -------------------------------------------------
WIDTH, HEIGHT = 1000, 640
MAZE_ROWS, MAZE_COLMS = 15, 15
CELL = 40  # pixels per maze cell

# Colors (RGB in 24-bit, like the rest of the codebase)
COLOR_WALL = 0x4444FF
COLOR_PATH = 0x222233
COLOR_PACS = 0xFFFF44
COLOR_SUPER = 0xFFAA00
COLOR_PLAYER = 0xFFFF00
COLOR_GHOST = 0xFF2266

# --- Build maze (same logic as practice.py) -------------------------------
maze = Maze(MAZE_ROWS, MAZE_COLMS, 42)
player = Player(maze.get_center(), 300)
ghosts = [Ghost(position) for position in maze.get_ghost_positions()]
game = Game(maze, player, ghosts, time_limit=18099999,
            pacgum_score=10, super_pacgum_score=50, ghost_score=200)


# --- MLX setup -------------------------------------------------------------
mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed, returned NULL pointer.")
    sys.exit(1)

win_ptr = mlx_obj.mlx_new_window(init_ptr, WIDTH, HEIGHT, "Pac-Man")
if not win_ptr:
    print("Error: mlx_new_window failed, returned NULL pointer.")
    sys.exit(1)

img_ptr = mlx_obj.mlx_new_image(init_ptr, WIDTH, HEIGHT)
img, bpp, line_size, fmt = mlx_obj.mlx_get_data_addr(img_ptr)

# Maze is centered on screen.
OFFSET_X = (WIDTH - MAZE_COLMS * CELL) // 2
OFFSET_Y = (HEIGHT - MAZE_ROWS * CELL) // 2


def put_pixel(x: int, y: int, color: int) -> None:
    """Write one opaque RGBA pixel into the image buffer at (x, y)."""
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return
    offset = y * line_size + x * 4
    img[offset] = (color >> 16) & 0xFF       # R
    img[offset + 1] = (color >> 8) & 0xFF    # G
    img[offset + 2] = color & 0xFF           # B
    img[offset + 3] = 0xFF                   # A

def fill_rect(x0: int, y0: int, x1: int, y1: int, color: int) -> None:
    """Fill a rectangle defined by top-left (x0, y0) and bottom-right (x1, y1)."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put_pixel(x, y, color)


def draw_cell(cx: int, cy: int, row: int, col: int) -> None:
    """Draw one maze cell: black path, colored walls, and items."""
    cell = game.maze.cells[row][col]
    px = OFFSET_X + col * CELL
    py = OFFSET_Y + row * CELL

    fill_rect(px, py, px + CELL - 1, py + CELL - 1, COLOR_PATH)

    # Walls: thick 4px lines where the bool is True.
    THICK = 4
    if cell.north:
        fill_rect(px, py, px + CELL - 1, py + THICK - 1, COLOR_WALL)
    if cell.south:
        fill_rect(px, py + CELL - THICK, px + CELL - 1, py + CELL - 1, COLOR_WALL)
    if cell.west:
        fill_rect(px, py, px + THICK - 1, py + CELL - 1, COLOR_WALL)
    if cell.east:
        fill_rect(px + CELL - THICK, py, px + CELL - 1, py + CELL - 1, COLOR_WALL)

    center_x = px + CELL // 2
    center_y = py + CELL // 2

    if cell.super_pacgum:
        fill_rect(center_x - 7, center_y - 7, center_x + 7, center_y + 7, COLOR_SUPER)
    elif cell.pacgum:
        fill_rect(center_x - 2, center_y - 2, center_x + 2, center_y + 2, COLOR_PACS)

    if cell.player:
        fill_rect(px + 8, py + 8, px + CELL - 8, py + CELL - 8, COLOR_PLAYER)
    elif cell.ghost:
        fill_rect(px + 8, py + 8, px + CELL - 8, py + CELL - 8, COLOR_GHOST)


def draw_maze() -> None:
    """Draw the whole maze into the image buffer."""
    rows = len(game.maze.cells)
    cols = len(game.maze.cells[0])
    for row in range(rows):
        for col in range(cols):
            draw_cell(OFFSET_X + col * CELL, OFFSET_Y + row * CELL, row, col)


current = Direction.RIGHT

def render_hook(param=None) -> None:
    """Render the current maze state every frame."""
    game.update(direction=current)
    draw_maze()
    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, img_ptr, 0, 0)
    time.sleep(0.15)


def key_hook(keycode: int, param=None) -> None:
    global current
    if keycode == 97:  # 'a' -> quit
        mlx_obj.mlx_loop_exit(init_ptr)
        mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
    if keycode == 65363:
        current = Direction.RIGHT
    if keycode == 65361:
        current = Direction.LEFT
    if keycode == 65362:
        current = Direction.UP
    if keycode == 65364:
        current = Direction.DOWN


mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)
mlx_obj.mlx_loop_hook(init_ptr, render_hook, None)

mlx_obj.mlx_loop(init_ptr)

mlx_obj.mlx_release(init_ptr)
