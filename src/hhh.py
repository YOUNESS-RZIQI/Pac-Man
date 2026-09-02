import sys
from mlx import Mlx
from maze_printer import print_maze
from maze import Maze, Player, Ghost, Game, Direction

# 1. Setup Game Objects
mz = Maze(15, 15, 42)
game = Game(mz, Player(mz.get_center(), 3), [Ghost(p) for p in mz.get_ghost_positions()], 180, 10, 50, 200)

# 2. Setup MLX
m = Mlx()
p = m.mlx_init()
w = m.mlx_new_window(p, 1000, 640, "Pac-Man Pixel Maze")

# Color mapping (Blue for walls, White for dots, Yellow for Pac-Man, Red for Ghosts)
cols = {'#': 0x0000FF, '.': 0xFFFFFF, 'P': 0xFFFF00, 'G': 0xFF0000}

def draw(*args):
    """Draws the grid pixel by pixel (10x10 blocks per cell)."""
    m.mlx_clear_window(p, w)
    lines = print_maze(game.maze.cells, None, True, False, False)
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            c = cols.get(char, 0) # 0 is black (empty space)
            if c != 0:
                # Draw a 10x10 pixel square for each element
                for dy in range(10):
                    for dx in range(10):
                        m.mlx_pixel_put(p, w, 210 + x * 10 + dx, 10 + y * 10 + dy, c)

def key_hook(k, _):
    """Handles keyboard input and updates the game."""
    if k == 97: # 'a' key to exit
        m.mlx_destroy_window(p, w)
        m.mlx_loop_exit(p)
        return
        
    dirs = {65363: Direction.RIGHT, 65361: Direction.LEFT, 65362: Direction.UP, 65364: Direction.DOWN}
    if k in dirs:
        game.update(direction=dirs[k])
    
    draw() # Redraw the screen after every move

# 3. Register Hooks
m.mlx_expose_hook(w, draw, p) # This ensures the maze is drawn immediately when opened!
m.mlx_key_hook(w, key_hook, p)

# 4. Start Loop
m.mlx_loop(p)