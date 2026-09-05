# Phase 1: Global Asset Loading

        # Load every single .xpm file (Player, Ghosts, Pac-Gums, Super Pac-Gums) at the very top of your script, right after initializing MLX.

        # Store these image pointers in global variables or a dictionary so they are loaded into your computer's RAM exactly once.

# Phase 2: The Static Canvas

        # Strip your draw_maze function down so it only draws the wall lines and empty black spaces into your img_ptr buffer using your put_pixel math.

        # Remove any logic that draws Pac-Gums, Super Pac-Gums, Ghosts, or the Player from this function.

        # Call this modified draw_maze() exactly one time before mlx_loop() starts.

# Phase 3: The Render Hook Sequence
        # Inside your render_hook, you will now layer everything back-to-front using mlx_put_image_to_window. The order is critical to prevent visual bugs:

        # Layer 1 (Background): Push your pre-drawn img_ptr to the window first. This acts as a clean slate, wiping away the previous frame's ghost and player positions.

        # Layer 2 (Consumables): Loop through your game.maze.cells. If cell.pacgum is True, push the Pac-Gum .xpm to that cell's exact (x * CELL_SIZE, y * CELL_SIZE) coordinate.
        # If cell.super_pacgum is True, push that image instead.

        # Layer 3 (Ghosts): Loop through your game.ghosts list and push the Ghost .xpm to their current (x, y) coordinates.

        # Layer 4 (Player): Push the Pac-Man .xpm to the window last, ensuring the player always renders on top of dots, background elements, and ghosts.

# Phase 4: Game Logic & Eating Dots

    # In your backend game.update() logic, when Pac-Man's coordinates overlap with a Pac-Gum cell, simply set cell.pacgum = False.

    # Because Layer 2 in your render_hook checks that boolean every single frame, the moment it turns False, the loop skips drawing the image.
    # The static black background from Layer 1 will naturally show through, making the dot disappear seamlessly without needing to manually erase anything.


import sys
import time

from mlx import Mlx
from maze import Maze, Player, Ghost, Game, Direction

# --- Window / cell sizing -------------------------------------------------
MAZE_ROWS, MAZE_COLMS = 15, 15
CELL_SIZE = 90  # pixels per maze cell

# Colors (RGB in 24-bit, like the rest of the codebase)
COLOR_WALL = 0x4444FF
COLOR_PATH = 0x222233
COLOR_PACS = 0xFFFF44
COLOR_SUPER = 0xFFAA00
COLOR_PLAYER = 0xFFFF00
COLOR_GHOST = 0xFF2266

# --- Build maze (same logic as practice.py) -------------------------------
maze = Maze(MAZE_ROWS, MAZE_COLMS, 42)
player = Player(maze.get_center_maze(), 300)
ghosts = [Ghost(position) for position in maze.get_ghost_positions()]
game = Game(maze, player, ghosts, time_limit=18099999,
            pacgum_score=10, super_pacgum_score=50, ghost_score=200)
current: Direction = Direction.UP

import sys

def load_all_imgs(init_ptr) -> dict:

    player_path_image = "/home/yrziqi/Pac-Man/src/Images/pac_man.xpm"
    player_img, w, h = mlx_obj.mlx_xpm_file_to_image(init_ptr, player_path_image)
    if not player_img:
        print("\033[91mError: player img not found\033[0m")
        sys.exit(1)

    ghost_path_image = "/home/yrziqi/Pac-Man/src/Images/ghost.xpm"
    ghost_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, ghost_path_image)
    if not ghost_img:
        print("\033[91mError: ghost_img not found\033[0m")
        sys.exit(1)

    super_path_image = "/home/yrziqi/Pac-Man/src/Images/super_pacgum.xpm"
    super_pacgum_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, super_path_image)
    if not super_pacgum_img:
        print("\033[91mError: super_pacgum_img not found\033[0m")
        sys.exit(1)

    pacgum_path_image = "/home/yrziqi/Pac-Man/src/Images/pac_gum.xpm"
    pac_gum_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, pacgum_path_image)
    if not pac_gum_img:
        print("\033[91mError: pac_gum_img not found\033[0m")
        sys.exit(1)

    Down_img_path = "/home/yrziqi/Pac-Man/src/Images/Down.xpm"
    Down_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Down_img_path)
    if not Down_img:
        print("\033[91mError: Down_img not found\033[0m")
        sys.exit(1)

    Up_img_path = "/home/yrziqi/Pac-Man/src/Images/Up.xpm"
    Up_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Up_img_path)
    if not Up_img:
        print("\033[91mError: Up_img not found\033[0m")
        sys.exit(1)

    Right_img_path = "/home/yrziqi/Pac-Man/src/Images/Right.xpm"
    Right_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Right_img_path)
    if not Right_img:
        print("\033[91mError: Right_img not found\033[0m")
        sys.exit(1)

    Left_img_path = "/home/yrziqi/Pac-Man/src/Images/Left.xpm"
    Left_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Left_img_path)
    if not Left_img:
        print("\033[91mError: Left_img not found\033[0m")
        sys.exit(1)



    return {
        "player": player_img,
        "ghost": ghost_img,
        "super_pacgum": super_pacgum_img,
        "pacgum": pac_gum_img,
        "down": Down_img,
        "up": Up_img,
        "right": Right_img,
        "left": Left_img,

    }

mlx_obj = Mlx()

init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: init_ptr = Null")

_ , WIDTH, HEIGHT = mlx_obj.mlx_get_screen_size(init_ptr)


imgs_dict = load_all_imgs(init_ptr)



win_ptr = mlx_obj.mlx_new_window(init_ptr, WIDTH, HEIGHT, "Pac-Man Arcade Game")


def key_hook(keycode: int, param=None) -> None:
    global current
    if keycode == 97:
        mlx_obj.mlx_loop_exit(init_ptr)

    if keycode == 65363:
        current = Direction.RIGHT
    if keycode == 65361:
        current = Direction.LEFT
    if keycode == 65362:
        current = Direction.UP
    if keycode == 65364:
        current = Direction.DOWN


# ??
def put_pixel_on_cell(walls_mem_ptr, walls_linesize, src_mem_ptr, src_linesize, cell_x, cell_y):
    """Overlay non-transparent pixels from the source sprite onto the destination cell."""
    start_x = cell_x * CELL_SIZE
    start_y = cell_y * CELL_SIZE
    row_bytes = CELL_SIZE * 4  # 4 bytes per pixel (BGRA)

    # Copy row-by-row, only writing non-transparent pixels so multiple
    # wall images can be composited into the same cell.
    for y in range(CELL_SIZE):
        src_offset = y * src_linesize
        dest_offset = ((start_y + y) * walls_linesize) + (start_x * 4)

        source_data = src_mem_ptr[src_offset : src_offset + row_bytes]

        for b in range(0, row_bytes, 4):
            # A pixel is transparent when all 4 bytes (BGRA) are 0x00.
            if source_data[b] != 0 or source_data[b + 1] != 0 or source_data[b + 2] != 0 or source_data[b + 3] != 0:
                walls_mem_ptr[dest_offset + b] = source_data[b]
                walls_mem_ptr[dest_offset + b + 1] = source_data[b + 1]
                walls_mem_ptr[dest_offset + b + 2] = source_data[b + 2]
                walls_mem_ptr[dest_offset + b + 3] = source_data[b + 3]


def put_walls_in_walls_img_pixels(mlx_obj: Mlx, walls_img_ptr, maze_cells, imgs_dict: dict):
    left_mem_ptr, _, left_linesize, _ = mlx_obj.mlx_get_data_addr(imgs_dict["left"])
    right_mem_ptr, _, right_linesize, _ = mlx_obj.mlx_get_data_addr(imgs_dict["right"])
    down_mem_ptr, _, down_linesize, _ = mlx_obj.mlx_get_data_addr(imgs_dict["down"])
    up_mem_ptr, _, up_linesize, _ = mlx_obj.mlx_get_data_addr(imgs_dict["up"])


    walls_mem_ptr, _, linesize, _ = mlx_obj.mlx_get_data_addr(walls_img_ptr)


    for y, row in enumerate(maze_cells):
        for x, cell in enumerate(row):

            if cell.left:
                put_pixel_on_cell(walls_mem_ptr, linesize, left_mem_ptr, left_linesize, x, y)

            if cell.right:
                put_pixel_on_cell(walls_mem_ptr, linesize, right_mem_ptr, right_linesize, x, y)

            if cell.up:
                put_pixel_on_cell(walls_mem_ptr, linesize, up_mem_ptr, up_linesize, x, y)

            if cell.down:
                put_pixel_on_cell(walls_mem_ptr, linesize, down_mem_ptr, down_linesize, x, y)





walls_img_ptr = mlx_obj.mlx_new_image(init_ptr, MAZE_COLMS * CELL_SIZE, MAZE_ROWS * CELL_SIZE)
put_walls_in_walls_img_pixels(mlx_obj, walls_img_ptr, game.maze.cells, imgs_dict)
    

def render(param: None = None) -> None:
    """Render hook: push the pre-drawn walls background to the window."""
    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, walls_img_ptr, 500, 100)


mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)

mlx_obj.mlx_loop_hook(init_ptr, render, init_ptr)

mlx_obj.mlx_loop(init_ptr)

mlx_obj.mlx_release(init_ptr)