# from mlx import Mlx
# import sys
# # **  hook functions are called as follow:

# # **    expose_hook(void *param);
# # **    key_hook(unsigned int keycode, void *param);
# # **    mouse_hook(unsigned int button, unsigned int x, unsigned int y,
# # **               void *param);
# # **    loop_hook(void *param);
# # **    loop_hook(void *param);

# # mlx_hook() — XCB backend (see mlx__xcb_hook.c / mlx__xcb_event.c):
# # x_event = XCB response type, x_mask = XCB event mask that ENABLES delivery.
# #  2 → XCB_KEY_PRESS,   mask 1  (XCB_EVENT_MASK_KEY_PRESS)  → any keydown
# #  3 → XCB_KEY_RELEASE, mask 2  (XCB_EVENT_MASK_KEY_RELEASE)
# #  4 → XCB_BUTTON_PRESS,   mask 4  (XCB_EVENT_MASK_BUTTON_PRESS)
# #  5 → XCB_BUTTON_RELEASE, mask 8  (XCB_EVENT_MASK_BUTTON_RELEASE)
# # 33 → XCB_CLIENT_MESSAGE, mask 0  (title-bar X button / close)


# WIDTH, HEIGHT = 1000, 640

# mlx_obj = Mlx()

# init_ptr = mlx_obj.mlx_init()

# if not init_ptr:
#     print("mlx_init() failer")
#     sys.exit(1)


# win_ptr = mlx_obj.mlx_new_window(init_ptr, WIDTH, HEIGHT, "Pac-Man")

# # Image buffer we draw into (reliable, unlike mlx_pixel_put in this backend).
# img_ptr = mlx_obj.mlx_new_image(init_ptr, WIDTH, HEIGHT)
# img_data, bpp, line_size, fmt = mlx_obj.mlx_get_data_addr(img_ptr)


# def put_pixel(x, y, color):
#     """Write one RGBA pixel into the image buffer at (x,y)."""
#     if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
#         return
#     offset = y * line_size + x * 4
#     img_data[offset] = (color >> 16) & 0xFF       # R
#     img_data[offset + 1] = (color >> 8) & 0xFF    # G
#     img_data[offset + 2] = color & 0xFF           # B
#     img_data[offset + 3] = 0xFF                   # A (opaque)


# def draw_line(sx, sy, ex, ey, color):
#     """Draw a line from (sx,sy) to (ex,ey). Same idea as pygame.draw.line."""
#     dx = abs(ex - sx)
#     dy = abs(ey - sy)
#     steps = max(dx, dy) or 1  # avoid division by zero for a single point
#     for i in range(steps + 1):
#         t = i / steps
#         x = round(sx + (ex - sx) * t)
#         y = round(sy + (ey - sy) * t)
#         put_pixel(x, y, color)


# def draw_hook(param):
#     # Draw lines straight into the image buffer.
#     draw_line(0, 0, WIDTH - 1, HEIGHT - 1, 0xFF0000)      # red diagonal
#     draw_line(100, 500, 900, 500, 0x00FF00)               # green horizontal
#     draw_line(100, 100, 900, 200, 0x0000FF)               # blue line
#     # Present the image to the window every frame.
#     mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, img_ptr, 0, 0)


# def key_hook(keycode, param):

#     if keycode == 97:
#         mlx_obj.mlx_destroy_window(init_ptr, win_ptr) 
#         mlx_obj.mlx_loop_exit(init_ptr)

#     print(f"Key pressed: {keycode}")



# def destroy_hook(keycode, param):
#     mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
#     mlx_obj.mlx_loop_exit(init_ptr)


# mlx_obj.mlx_key_hook(win_ptr, key_hook, None)

# # Redraw every frame (loop hook) so the pixels stay visible.
# mlx_obj.mlx_loop_hook(init_ptr, draw_hook, None)

# # mlx_obj.mlx_hook(win_ptr, 2, 1, destroy_hook, None)

# mlx_obj.mlx_loop(init_ptr)



# mlx_obj.mlx_release(init_ptr)



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

import sys

mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
win_ptr = mlx_obj.mlx_new_window(init_ptr, 1000, 640, "Pac-Man")

def key_hook(key_num, param):
    if key_num == 97:
        mlx_obj.mlx_destroy_window(param, win_ptr)
        mlx_obj.mlx_loop_exit(init_ptr)

# 1. Load the image
img_path = "/home/yrziqi/Pac-Man/src/Images/image.xpm"
png_ptr, w, h = mlx_obj.mlx_xpm_file_to_image(init_ptr, img_path)



print(f"Image loaded: {w}x{h}")

# 3. Draw the image (x=50, y=50) instead of (w, h)
mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, png_ptr, 100, 100)

mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)
mlx_obj.mlx_loop(init_ptr)
mlx_obj.mlx_release(init_ptr)