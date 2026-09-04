import sys
from mlx import Mlx
from maze import Maze, Player, Ghost, Game, Cell, Direction
import time

class Colors:
    RED        = 0xFF0000FF
    BLUE       = 0xFFFF0000
    GREEN      = 0xFF00FF00
    YELLOW     = 0xFF00FFFF
    ORANGE     = 0xFF0080FF
    PURPLE     = 0xFFFF00FF
    PINK       = 0xFFFF80FF
    CYAN       = 0xFFFFFF00
    WHITE      = 0xFFFFFFFF
    BLACK      = 0xFF000000
    GRAY       = 0xFF808080
    DARK_GRAY  = 0xFF404040
    LIGHT_GRAY = 0xFFC0C0C0
    BROWN      = 0xFF008040
    GOLD       = 0xFF00D7FF
    LIME       = 0xFF00FF80
    NAVY       = 0xFF800000
    TEAL       = 0xFF808000
    MAGENTA    = 0xFFFF00FF
    MAROON     = 0xFF000080
    OLIVE      = 0xFF008080
    SKY_BLUE   = 0xFFEBCE87
    DARK_BLUE  = 0xFF8B0000
    DARK_GREEN = 0xFF006400
    DARK_RED   = 0xFF00008B

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

# هنا كنجبدو التصويرة ديال اللاعب مرة وحدة باش مانعمروش الميموار
player_sprite, pw, ph = mlx_obj.mlx_xpm_file_to_image(init_ptr, "/home/yrziqi/Pac-Man/src/Images/pac_40_40.xpm")
if not player_sprite:
    print("Error: Could not load pac_40_40.xpm")
    sys.exit(1)

# متغيرات باش نعقلو على البلاصة فين كاين اللاعب
player_x = 0
player_y = 0

def put_pixel(x, y, color = 0xFFFFFFFF):
    if x < 0 or x >= 1000 or y < 0 or y >= 640:
        return

    offset = (y * line_size) + (x * 4)
    img[offset] = (color >> 16) & 0xFF       # B
    img[offset + 1] = (color >> 8) & 0xFF    # G
    img[offset + 2] = color & 0xFF           # R
    img[offset + 3] = 0xFF                   # A

def draw_horizontal_line(x_start, x_end, y):
    if x_start > x_end:
        return
    for i in range(x_start, x_end + 1):
        put_pixel(i, y)

def draw_vertical_line(x, y_start, y_end):
    if y_start > y_end:
        return
    for i in range(y_start, y_end + 1):
        put_pixel(x, i)

CELL_SIZE = 40

def draw_cell_walls(x, y, cell: Cell):
    left = x * CELL_SIZE
    right = (x + 1) * CELL_SIZE
    top = y * CELL_SIZE
    bottom = (y + 1) * CELL_SIZE

    if cell.west:
        for i in range(0, 6):
            draw_vertical_line(left + i, top, bottom)
    if cell.east:
        for i in range(0, 6):
            draw_vertical_line(right - i, top, bottom)
    if cell.north:
        for i in range(0, 6):
            draw_horizontal_line(left, right, top + i)
    if cell.south:
        for i in range(0, 6):
            draw_horizontal_line(left, right, bottom - i)

def draw_pacgum(center_x, center_y, color):
    for y in range(-2, 4):
        for x in range(-2, 4):
            put_pixel(center_x + x, center_y + y, color)

def draw_player(top_x, top_y, color):
    global player_x, player_y
    # كنخبيو غير الإحداثيات هنا، الرسم غايكون فـ render_hook
    player_x = top_x
    player_y = top_y

def draw_ghost(center_x, center_y, color):
    for y in range(-10, 10 + 1):
        for x in range(-10, 10 + 1):
            put_pixel(center_x + x, center_y + y, color)

def draw_42(center_x, center_y, color):
    for y in range(-18, 18):
        for x in range(-18, 18):
            put_pixel(center_x + x, center_y + y, color)

def draw_super_pacgum(center_x, center_y, color):
    for y in range(-5, 5 + 1):
        for x in range(-5, 5 + 1):
            put_pixel(center_x + x, center_y + y, color)

def clean_cell(x, y):
    left = x * CELL_SIZE
    top = y * CELL_SIZE
    for py in range(top, top + CELL_SIZE):
        for px in range(left, left + CELL_SIZE):
            put_pixel(px, py, 0xFF000000)

def draw_cell(x, y, cell: Cell):
    clean_cell(x, y)
    draw_cell_walls(x, y, cell)

    center_x = (x * CELL_SIZE) + (CELL_SIZE // 2)
    center_y = (y * CELL_SIZE) + (CELL_SIZE // 2)

    if cell.pacgum:
        draw_pacgum(center_x, center_y, Colors.GRAY)
    if cell.super_pacgum:
        draw_super_pacgum(center_x, center_y, Colors.PURPLE)
    if cell.player:
        draw_player(x * CELL_SIZE, y * CELL_SIZE, Colors.SKY_BLUE)
    if cell.ghost:
        draw_ghost(center_x, center_y, Colors.GOLD)
    if cell.is_42:
        draw_42(center_x, center_y, Colors.RED)

def draw_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            draw_cell(x, y, maze[y][x])


print("format:", fmt)

MAZE_ROWS = 15
MAZE_COLMS = 15
maze = Maze(MAZE_ROWS, MAZE_COLMS, 42)
player = Player(maze.get_center_maze(), 300)
ghosts = [Ghost(position) for position in maze.get_ghost_positions()]
game = Game(maze, player, ghosts, time_limit=18099999,
            pacgum_score=10, super_pacgum_score=50, ghost_score=200)

current = Direction.UP

def render_hook(param=None) -> None:
    """Render the current maze state every frame."""
    game.update(direction=current, player_speed=100, ghost_speed=100)
    
    # 1. رسم المتاهة فالخلفية
    draw_maze(game.maze.cells)
    
    # 2. حط الخلفية فالنافذة هي اللولة
    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, img_ptr, 0, 0)
    
    # 3. عاد حط التصويرة ديال اللاعب من الفوق
    mlx_obj.mlx_put_image_to_window(init_ptr, win_ptr, player_sprite, player_x, player_y)


def key_hook(keycode: int, param=None) -> None:
    global current
    if keycode == 97:  # 'a' -> quit
        mlx_obj.mlx_loop_exit(init_ptr)
        mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
    if keycode == 65363:
        current = Direction.RIGHT
    if keycode == 65361:
        current = Direction.LEFT
    if keycode == 65362:
        current = Direction.UP
    if keycode == 65364:
        current = Direction.DOWN

mlx_obj.mlx_key_hook(win_ptr, key_hook, init_ptr)
mlx_obj.mlx_loop_hook(init_ptr, render_hook, None)

mlx_obj.mlx_loop(init_ptr)
mlx_obj.mlx_release(init_ptr)