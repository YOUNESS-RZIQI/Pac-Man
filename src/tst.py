import sys
from mlx import Mlx

mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed, returned NULL pointer.")
    sys.exit(1)

win_ptr = mlx_obj.mlx_new_window(init_ptr, 1000, 640, "Pac-Man")
if not win_ptr:
    print("Error: mlx_new_window failed, returned NULL pointer.")
    sys.exit(1)

img_ptr = mlx_obj.mlx_new_image(init_ptr, 1000, 640)
img, bpp, line_size, fmt = mlx_obj.mlx_get_data_addr(img_ptr)



def key_hook(keycode: int, param=None) -> None:
    global current
    if keycode == 97:  # 'a' -> quit
        mlx_obj.mlx_loop_exit(init_ptr)
        mlx_obj.mlx_destroy_window(init_ptr, win_ptr)

    print("key= ", keycode)

    
def put_pixel(x, y):
    if x < 0 or x >= 1000 or y < 0 or y >= 640:
        return

    offset = (y * line_size) + (x * 4)

    img[offset + 0] = 0     #Blue
    img[offset + 1] = 0     #Green
    img[offset + 2] = 255   #Red
    img[offset + 3] = 255   # Alpha channel on your system



def draw_horizontal_line(x_start, x_end, y):
    if x_start > x_end:
        print("x_start must not be greater then x_end")
        return
    for i in range(x_start, x_end + 1):
        put_pixel(i, y)

def draw_vertical_line(x, y_start, y_end):
    if y_start > y_end:
        print("x_start must not be greater then x_end")
        return
    for i in range(y_start, y_end + 1):
        put_pixel(x, i)



draw_horizontal_line(0, 999, 320)
draw_vertical_line(0, 0, 600)

mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, img_ptr, 0,0)

mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)



mlx_obj.mlx_loop(init_ptr)


mlx_obj.mlx_release(init_ptr)
