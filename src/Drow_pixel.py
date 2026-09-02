from mlx import Mlx
import sys
# **  hook functions are called as follow:

# **    expose_hook(void *param);
# **    key_hook(unsigned int keycode, void *param);
# **    mouse_hook(unsigned int button, unsigned int x, unsigned int y,
# **               void *param);
# **    loop_hook(void *param);
# **    loop_hook(void *param);

# mlx_hook() — XCB backend (see mlx__xcb_hook.c / mlx__xcb_event.c):
# x_event = XCB response type, x_mask = XCB event mask that ENABLES delivery.
#  2 → XCB_KEY_PRESS,   mask 1  (XCB_EVENT_MASK_KEY_PRESS)  → any keydown
#  3 → XCB_KEY_RELEASE, mask 2  (XCB_EVENT_MASK_KEY_RELEASE)
#  4 → XCB_BUTTON_PRESS,   mask 4  (XCB_EVENT_MASK_BUTTON_PRESS)
#  5 → XCB_BUTTON_RELEASE, mask 8  (XCB_EVENT_MASK_BUTTON_RELEASE)
# 33 → XCB_CLIENT_MESSAGE, mask 0  (title-bar X button / close)


mlx_obj = Mlx()

init_ptr = mlx_obj.mlx_init()

if not init_ptr:
    print("mlx_init() failer")
    sys.exit(1)


win_ptr = mlx_obj.mlx_new_window(init_ptr, 1000, 640, "Pac-Man")


def key_hook(keycode, param):

    if keycode == 97:
        mlx_obj.mlx_destroy_window(init_ptr, win_ptr) 
        mlx_obj.mlx_loop_exit(init_ptr)


    print(f"Key pressed: {keycode}")



def destroy_hook(keycode, param):
    mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
    mlx_obj.mlx_loop_exit(init_ptr)


# mlx_obj.mlx_key_hook(win_ptr, key_hook, None)

mlx_obj.mlx_hook(win_ptr, 2, 1, destroy_hook, None)

mlx_obj.mlx_loop(init_ptr)



mlx_obj.mlx_release(init_ptr)