"""
Option 2: Real pixel zoom (image-buffer version).

The scene is rendered into a full-size virtual image (3840x2160) by writing
pixels directly into its memory buffer (fast slice writes, no per-pixel C calls),
then scaled DOWN pixel-by-pixel (nearest neighbour) into a 1000x800 image
buffer, which is blitted to the window in ONE call. True zoom, fast enough
to actually display.

Format: B8G8R8A8, 4 bytes/pixel, `size_line` bytes per row.
Color 0xRRGGBB is stored little-endian as (BB, GG, RR, FF).
"""
from mlx import Mlx
import sys

VIRTUAL_W = 3840
VIRTUAL_H = 2160
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


def downscale_nearest(dst, dst_sl: int, dst_w: int, dst_h: int,
                      src, src_sl: int, src_w: int, src_h: int) -> None:
    """Nearest-neighbour scale src image buffer into dst image buffer."""
    for wy in range(dst_h):
        vy = min(int(wy * src_h / dst_h), src_h - 1)
        src_row_start = vy * src_sl
        src_row = src[src_row_start:src_row_start + src_w * 4]
        dst_row_start = wy * dst_sl
        for wx in range(dst_w):
            vx = min(int(wx * src_w / dst_w), src_w - 1)
            dst[dst_row_start + wx * 4: dst_row_start + wx * 4 + 4] = \
                src_row[vx * 4: vx * 4 + 4]


mlx_obj = Mlx()
init_ptr = mlx_obj.mlx_init()
if not init_ptr:
    print("Error: mlx_init failed")
    sys.exit(1)

win_ptr = mlx_obj.mlx_new_window(init_ptr, WIN_W, WIN_H, "Option 2 - Real Pixel Zoom")
if not win_ptr:
    print("Error: mlx_new_window failed")
    sys.exit(1)

# Full-resolution virtual scene image
virt_img = mlx_obj.mlx_new_image(init_ptr, VIRTUAL_W, VIRTUAL_H)
if not virt_img:
    print("Error: mlx_new_image (virtual) failed")
    sys.exit(1)
virt_data, _, virt_sl, _ = mlx_obj.mlx_get_data_addr(virt_img)

# Window-sized output image
out_img = mlx_obj.mlx_new_image(init_ptr, WIN_W, WIN_H)
if not out_img:
    print("Error: mlx_new_image (out) failed")
    sys.exit(1)
out_data, _, out_sl, _ = mlx_obj.mlx_get_data_addr(out_img)


def draw_scene() -> None:
    """Render the virtual scene, then scale it into the window image."""
    # Black background on the virtual canvas
    fill_rect(virt_data, virt_sl, VIRTUAL_W, VIRTUAL_H,
              0, 0, VIRTUAL_W, VIRTUAL_H, 0x000000)

    # White rectangle near top-left of the zoomed canvas
    fill_rect(virt_data, virt_sl, VIRTUAL_W, VIRTUAL_H,
              100, 100, 800, 600, 0xFFFFFF)
    # Red rectangle in the center
    fill_rect(virt_data, virt_sl, VIRTUAL_W, VIRTUAL_H,
              VIRTUAL_W // 2, VIRTUAL_H // 2, 1200, 900, 0xFF0000)
    # Green rectangle in the bottom-right corner
    fill_rect(virt_data, virt_sl, VIRTUAL_W, VIRTUAL_H,
              VIRTUAL_W - 800, VIRTUAL_H - 600, 800, 600, 0x00FF00)

    # Scale the 3840x2160 scene down to 1000x800 (true pixel zoom)
    downscale_nearest(out_data, out_sl, WIN_W, WIN_H,
                      virt_data, virt_sl, VIRTUAL_W, VIRTUAL_H)

    # Blit the window-sized image to the window in ONE call
    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, out_img, 0, 0)


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

mlx_obj.mlx_destroy_image(init_ptr, virt_img)
mlx_obj.mlx_destroy_image(init_ptr, out_img)
mlx_obj.mlx_release(init_ptr)