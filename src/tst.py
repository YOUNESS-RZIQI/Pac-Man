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
WIDTH, HEIGHT = 1000, 640
MAZE_ROWS, MAZE_COLMS = 15, 15
CELL_SIZE = 40  # pixels per maze cell

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


mlx_obj = Mlx()

init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: init_ptr = Null")


player_path_image = "/home/yrziqi/Pac-Man/src/Images/pac_man.xpm"
player_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, player_path_image)
if not player_img:
    print("player img error")

ghost_path_image = "/home/yrziqi/Pac-Man/src/Images/host.xpm"
ghost_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, ghost_path_image)
if not ghost_img:
    print("ghost_img error")

super_path_image = "/home/yrziqi/Pac-Man/src/Images/super_pacgum.xpm"
super_pacgum_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, super_path_image)
if not super_pacgum_img:
    print("super_pacgum_img error")


pacgum_path_image = "/home/yrziqi/Pac-Man/src/Images/pac_gum.xpm"
pac_gum_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, pacgum_path_image)
if not pac_gum_img:
    print("pac_gum_img error")

Down_img_path = "/home/yrziqi/Pac-Man/src/Images/Down.xpm"
Down_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Down_img_path)
if not Down_img:
    print("Down_img error")

Up_img_path = "/home/yrziqi/Pac-Man/src/Images/Up.xpm"
Up_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Up_img_path)
if not Up_img:
    print("Up_img error")


Right_img_path = "/home/yrziqi/Pac-Man/src/Images/Right.xpm"
Right_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Right_img_path)
if not Right_img:
    print("Right_img error")


Left_img_path = "/home/yrziqi/Pac-Man/src/Images/Left.xpm"
Left_img, _, _ = mlx_obj.mlx_xpm_file_to_image(init_ptr, Left_img_path)
if not Left_img:
    print("Left_img error")



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


def render(param):
    pass


mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)

mlx_obj.mlx_loop_hook(init_ptr, render, init_ptr)

mlx_obj.mlx_loop(init_ptr)

mlx_obj.mlx_release(init_ptr)