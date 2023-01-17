# Game basic
WIDTH, HEIGHT = 1280, 700
FPS = 60
TILE_SIZE = 64

MAP = [
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '-', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-'],
    ['-', '-', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-'],
    ['-', '-', 'x', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['-', '-', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', '-'],
    ['-', '-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-'],
    ['-', '-', '-', '-', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
]


MAP_LEVEL_2 = [
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', 'x', 'x', 'x', 'x', 'x', '-', '-'],
    ['-', '-', '-', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '-', '-', '-', '-', 'x', 'x', ' ', ' ', ' ', ' ', ' ', 'x', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-'],
    ['-', '-', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', 'x'],
    ['-', '-', 'x', ' ', ' ', ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', 'x'],
    ['-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', 'x'],
    ['-', '-', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-'],
    ['-', '-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-'],
    ['-', '-', '-', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', '-', '-', '-', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '-', '-', '-'],
    ['-', '-', '-', '-', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
]

# COLORS
COLORS = {"background": (0, 162, 232)}
