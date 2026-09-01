from mlx import Mlx
import sys


# Initialize the MLX library
mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed, returned NULL pointer.")
    sys.exit(1)



# mlx new Window
win_ptr = mlx_obj.mlx_new_window(init_ptr, 1000, 800, "Pac-Man")
if not win_ptr:
    print("Error: mlx_new_window failed, returned NULL pointer.")
    sys.exit(1)



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


def expose_hook(param):
    mlx_obj.mlx_string_put(param, win_ptr, 10, 10, 0xFFFFFF, "Hello World!")

def key_hook(keycode, param):
    if keycode == 97:
        mlx_obj.mlx_destroy_window(param, win_ptr)
        mlx_obj.mlx_loop_exit(param)
    if keycode == 99:
        mlx_obj.mlx_clear_window(param, win_ptr)
    print(f"Key pressed: {keycode}")




mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)
mlx_obj.mlx_expose_hook(win_ptr, expose_hook, init_ptr)

mlx_obj.mlx_loop(init_ptr)


# Destoy the MLX object when done
release_ptr = mlx_obj.mlx_release(init_ptr)
if release_ptr != 0:
    print("Error: mlx_release failed, returned Non-zero value.")
    sys.exit(1)
