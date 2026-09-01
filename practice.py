from mlx import Mlx
import sys


# Initialize the MLX library
mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed, returned NULL pointer.")
    sys.exit(1)



# mlx new Window
win_ptr = mlx_obj.mlx_new_window(init_ptr, 800, 600, "Pac-Man")
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






# Enter the event loop — this keeps the window open until the user closes it
mlx_obj.mlx_loop(init_ptr)






# mlx clear Window
clear_int = mlx_obj.mlx_clear_window(init_ptr, win_ptr)
if clear_int != 0:
    print("Error: mlx_clear_window failed, returned Non-zero value.")
    sys.exit(1)
# mlx destroy Window
dest_int = mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
if dest_int != 0:
    print("Error: mlx_destroy_window failed, returned Non-zero value.")
    sys.exit(1)





# Destoy the MLX object when done
release_ptr = mlx_obj.mlx_release(init_ptr)
if release_ptr != 0:
    print("Error: mlx_release failed, returned Non-zero value.")
    sys.exit(1)
