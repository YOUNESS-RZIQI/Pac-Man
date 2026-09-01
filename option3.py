"""
Option 3: Bigger-looking text (image fonts, image-buffer version).

mlx_string_put draws a fixed, tiny font that cannot be scaled. Instead we build
our own blocky glyphs into an image buffer with fast slice fills. Each digit is
a 3x5 bitmap, every cell rendered as a `size`x`size` block -> genuinely large,
clean text. The finished image is blitted to the window in ONE call.

Format: B8G8R8A8, 4 bytes/pixel, `size_line` bytes per row.
"""
from mlx import Mlx
import sys

WIN_W = 1000
WIN_H = 800


def color_bytes(color: int) -> bytes:
    """0xRRGGBB -> 4 bytes B8G8R8A8 with alpha=FF."""
    b = color & 0xFF
    g = (color >> 8) & 0xFF
    r = (color >> 16) & 0xFF
    return bytes((b, g, r, 0xFF))


def fill_rect(buf, sl: int, img_w: int, img_h: int,
              x: int, y: int, rw: int, rh: int, color: int) -> None:
    """Fill a rectangle in an image buffer (clamped to image bounds)."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(img_w, x + rw)
    y1 = min(img_h, y + rh)
    row = color_bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        start = yy * sl + x0 * 4
        buf[start:start + len(row)] = row


# 3x5 blocky glyphs (1 = filled cell)
GLYPHS = {
    '0': [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    '1': [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
    '2': [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    '3': [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    '4': [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
    '5': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    '6': [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    '7': [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
    '8': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    '9': [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
}


def draw_big_text(buf, sl: int, img_w: int, img_h: int,
                  x: int, y: int, text: str, cell: int, color: int) -> None:
    """Draw scaled text: each glyph cell is `cell`x`cell` pixels."""
    gap = cell // 2
    for i, ch in enumerate(text):
        glyph = GLYPHS.get(ch, GLYPHS['8'])
        for r, row in enumerate(glyph):
            for c, filled in enumerate(row):
                if filled:
                    fill_rect(buf, sl, img_w, img_h,
                              x + i * (cell * 4 + gap) + c * cell,
                              y + r * cell,
                              cell, cell, color)


mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed")
    sys.exit(1)

win_ptr = mlx_obj.mlx_new_window(init_ptr, WIN_W, WIN_H, "Option 3 - Big Image Text")
if not win_ptr:
    print("Error: mlx_new_window failed")
    sys.exit(1)

img = mlx_obj.mlx_new_image(init_ptr, WIN_W, WIN_H)
if not img:
    print("Error: mlx_new_image failed")
    sys.exit(1)
data, _, sl, _ = mlx_obj.mlx_get_data_addr(img)


def draw_scene() -> None:
    """Black background + big red text, then blit once."""
    fill_rect(data, sl, WIN_W, WIN_H, 0, 0, WIN_W, WIN_H, 0x000000)

    cell = 40  # each glyph cell 40x40 -> digit is 120x200 px
    draw_big_text(data, sl, WIN_W, WIN_H, 170, 250, "123", cell, 0xFF0000)
    draw_big_text(data, sl, WIN_W, WIN_H, 320, 520, "45", cell // 2, 0x00FF00)

    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, img, 0, 0)


draw_scene()  # initial render


def expose_handler(param: object) -> int:
    """Redraw if the window needs repainting."""
    draw_scene()
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


mlx_obj.mlx_expose_hook(win_ptr, expose_handler, None)
mlx_obj.mlx_hook(win_ptr, 3, 2, key_handler, init_ptr)   # KeyRelease
mlx_obj.mlx_hook(win_ptr, 33, 0, close_handler, init_ptr)  # X button

mlx_obj.mlx_loop(init_ptr)

mlx_obj.mlx_destroy_image(init_ptr, img)
mlx_obj.mlx_release(init_ptr)