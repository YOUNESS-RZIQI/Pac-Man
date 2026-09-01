

# loop staff: 

    #    int
    #    mlx_key_hook ( void *win_ptr, int (*funct_ptr)(), void *param ); // when a key is released

    #    int
    #    mlx_mouse_hook ( void *win_ptr, int (*funct_ptr)(), void *param );// when a mouse button is clicked You get the button number (left=1, middle=2, right=3) and the x,y position of the click.

    #    int
    #    mlx_expose_hook ( void *win_ptr, int (*funct_ptr)(), void *param );//  when window needs to be redraw

    #    int
    #    mlx_loop_hook ( void *mlx_ptr, int (*funct_ptr)(), void *param );

    #    int
    #    mlx_loop ( void *mlx_ptr );

    #    int
    #    mlx_loop_exit ( void *mlx_ptr );


# **  hook functions are called as follow:

# **    expose_hook(void *param);
# **    key_hook(unsigned int keycode, void *param);
# **    mouse_hook(unsigned int button, unsigned int x, unsigned int y,
# **               void *param);
# **    loop_hook(void *param);


from time import time

from mlx import Mlx
import sys


# Initialize the MLX library
mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed, returned NULL pointer.")
    sys.exit(1)



# mlx new Window
win_ptr = mlx_obj.mlx_new_window(init_ptr, 1000, 640, "Pac-Man")
if not win_ptr:
    print("Error: mlx_new_window failed, returned NULL pointer.")
    sys.exit(1)


from maze_printer import print_maze
from maze import Maze, Player, Ghost, Game
import time


maze = Maze(15, 15, 42)
player = Player(maze.get_center())
ghosts = [
        Ghost(position)
        for position in maze.get_ghost_positions()
    ]
game = Game(maze, player, ghosts, time_limit=180)

# game.update(direction=1)


grid = game.maze.cells
print("\n\nPrinting the maze:", grid, "\n\n")
# list_of_strings = print_maze(grid, None, show_path=True, rand_wals=False, is_slow=False)


def expose_hook(param):
    for i in range(100):
        mlx_obj.mlx_clear_window(param, win_ptr)
        for i, l in enumerate(print_maze(grid, None, show_path=True, rand_wals=False, is_slow=False)):

            mlx_obj.mlx_string_put(param, win_ptr, 210, 10 + i * 20, 0xFFFFFF, l)
        game.update(direction=1)
        time.sleep(0.5)

    # # 60 frame par second
    # time.sleep(1 / 60)


def key_hook(keycode, param):
    if keycode == 97:
        mlx_obj.mlx_destroy_window(param, win_ptr)
        mlx_obj.mlx_loop_exit(param)
    if keycode == 99:
        mlx_obj.mlx_clear_window(param, win_ptr)
    print(f"Key pressed: {keycode}")




mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)
mlx_obj.mlx_expose_hook(win_ptr, expose_hook, init_ptr)

# mlx_obj.mlx_loop_hook(init_ptr, expose_hook, init_ptr)



mlx_obj.mlx_loop(init_ptr)


# Destoy the MLX object when done
release_ptr = mlx_obj.mlx_release(init_ptr)
if release_ptr != 0:
    print("Error: mlx_release failed, returned Non-zero value.")
    sys.exit(1)
