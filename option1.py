"""
Option 1: Logical zoom.

The window stays at a fixed physical size (1000x800) but the game logic works
in a virtual "zoomed" coordinate space (e.g. 3840x2160). Every position is
scaled down to fit the real window. This zooms the LAYOUT but not the pixels:
text stays at the fixed MLX font size because mlx_string_put cannot scale text.
"""
from mlx import Mlx
import sys

# Virtual (zoomed) resolution
VIRTUAL_W = 3840
VIRTUAL_H = 2160

# Physical window size
WIN_W = 1000
WIN_H = 800

# Scale factors from virtual space -> window space
scale_x = WIN_W / VIRTUAL_W
scale_y = WIN_H / VIRTUAL_H


def v_to_w(vx: int, vy: int):
    """Convert a virtual (zoomed) coordinate to a window coordinate."""
    return int(vx * scale_x), int(vy * scale_y)


def draw_text(mlx_obj, init_ptr, win_ptr, vx, vy, color, text):
    """Draw text using a virtual position, scaled to the window."""
    wx, wy = v_to_w(vx, vy)
    mlx_obj.mlx_string_put(init_ptr, win_ptr, wx, wy, color, text)


mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed")
    sys.exit(1)

win_ptr = mlx_obj.mlx_new_window(init_ptr, WIN_W, WIN_H, "Option 1 - Logical Zoom")
if not win_ptr:
    print("Error: mlx_new_window failed")
    sys.exit(1)


def game_loop(param: object) -> int:
    mlx_obj.mlx_clear_window(init_ptr, win_ptr)

    # Top-left (virtual 20,30)
    draw_text(mlx_obj, init_ptr, win_ptr, 20, 30, 0xFFFFFF, "Score: 0")

    # Top-center (virtual 3840/2)
    draw_text(mlx_obj, init_ptr, win_ptr, VIRTUAL_W // 2, 30, 0x00FF00, "Level: 1")

    # Center of the zoomed canvas (virtual 3840/2, 2160/2)
    draw_text(mlx_obj, init_ptr, win_ptr,
              VIRTUAL_W // 2, VIRTUAL_H // 2, 0xFF0000, "PAC-MAN (logical zoom)")
    return 0


def key_handler(keycode: int, param: object) -> int:
    """Quit on ESC (65307) or 'a' (97)."""
    if keycode in (65307, 97):
        mlx_obj.mlx_loop_exit(param)
    return 0


def close_handler(param: object) -> int:
    """Quit when the window X button is clicked."""
    mlx_obj.mlx_loop_exit(param)
    return 0


# KeyRelease = event 3, mask 2 ; ClientMessage (X button) = event 33
mlx_obj.mlx_hook(win_ptr, 3, 2, key_handler, init_ptr)
mlx_obj.mlx_hook(win_ptr, 33, 0, close_handler, init_ptr)

mlx_obj.mlx_loop_hook(init_ptr, game_loop, None)
mlx_obj.mlx_loop(init_ptr)
mlx_obj.mlx_release(init_ptr)
