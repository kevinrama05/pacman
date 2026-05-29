from mlx import Mlx
from mlx_utils import parse_maze_output, change_seed, ParseDict
from random import randint
from typing import Any

output: ParseDict = parse_maze_output()
GREEN = 0xFF00FF00
BLUE = 0xFF0000FF
ORANGE = 0xFFAA0000
RED = 0xFFFF0000
WHITE = 0xFFFFFFFF
BLACK = 0x00000000
SHOW = True
FLIP = True
SCREEN_W, SCREEN_H = 2560, 1440
WIDTH = len(output["maze"][0])
HEIGHT = len(output["maze"])
CELL_SIZE = max(
    2,
    min(SCREEN_W * 3 // 4 // WIDTH, SCREEN_H * 3 // 4 // HEIGHT))
if CELL_SIZE > 80:
    CELL_SIZE = 80
START_X = (SCREEN_W - WIDTH * CELL_SIZE) // 2 + 10
START_Y = ((SCREEN_H - HEIGHT * CELL_SIZE) - 200) // 2 + 10


class DrawPointer:
    """
    DrawPointer class is a wrapper, which holds the
    MLX() class, initializes the mlx pointer and the
    window pointer

    Args:
        None

    Attributes:
        None
    """

    def __init__(self) -> None:
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.win_ptr = None


def walls_(hex_value: str) -> list[bool]:
    """
    It gets the value of the current cell, and returns a
    list of booleans, where each boolean represents the wall,
    where if the wall exists, is True, else, is False
    Example: 15 -> 1111, [True, True, True, True]

    Args:
        hex_value (str): The current cell represented in hexadecimal

    Returns:
        list[bool]: The walls of the cell represented in boolean
    """
    value = int(hex_value, 16)
    bit_length = len(hex_value) * 4
    binary_str = format(value, f"0{bit_length}b")
    walls = []
    for i in binary_str:
        if i == "1":
            walls.append(True)
        else:
            walls.append(False)
    return walls


def draw_cell(drawer: DrawPointer, cell: list[bool], x: int, y: int) -> None:
    """
    This function draws the cell, based on the wall, starting on (x, y)
    If all the walls are available ([True, True, True, True]), It also
    fills the cell

    Args:
        drawer (DrawPointer): MLX wrapper
        cell (list[bool]): Walls on the current cell
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        None
    """
    if cell[3]:
        for i in range(0, CELL_SIZE):
            drawer.m.mlx_pixel_put(
                drawer.mlx_ptr,
                drawer.win_ptr,
                x + i,
                y,
                WHITE if FLIP else BLUE
            )
    if cell[2]:
        for i in range(0, CELL_SIZE):
            drawer.m.mlx_pixel_put(
                drawer.mlx_ptr,
                drawer.win_ptr,
                x + CELL_SIZE,
                y + i,
                WHITE if FLIP else BLUE,
            )
    if cell[1]:
        for i in range(0, CELL_SIZE):
            drawer.m.mlx_pixel_put(
                drawer.mlx_ptr,
                drawer.win_ptr,
                x + CELL_SIZE - i,
                y + CELL_SIZE,
                WHITE if FLIP else BLUE,
            )
    if cell[0]:
        for i in range(0, CELL_SIZE):
            drawer.m.mlx_pixel_put(
                drawer.mlx_ptr,
                drawer.win_ptr,
                x,
                y + CELL_SIZE - i,
                WHITE if FLIP else BLUE,
            )

    if False not in cell:
        for i in range(1, CELL_SIZE - 1):
            for j in range(1, CELL_SIZE - 1):
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr,
                    x + j,
                    y + i,
                    BLUE if FLIP else WHITE,
                )


def draw_square(
        drawer: DrawPointer, coordinates: tuple[int, int], color: int) -> None:
    """
    This draws a square in a coordinate. This is used to identify the entry
    and exit_ in the maze

    Args:
        drawer (DrawPointer): MLX wrapper
        coordinates (tuple[int, int]): Coordinate to start drawing
        color (int): Color used to fill the square, represented in binary

    Returns:
        None
    """
    nx, ny = coordinates

    x = START_X + (nx * CELL_SIZE)
    y = START_Y + (ny * CELL_SIZE)

    for i in range(2, CELL_SIZE - 2):
        for j in range(2, CELL_SIZE - 2):
            drawer.m.mlx_pixel_put(
                drawer.mlx_ptr, drawer.win_ptr, x + j, y + i, color)


def draw_path(drawer: DrawPointer, entry: tuple[int, int], path: str) -> None:
    """
    Draws the path from entry to exit_

    Args:
        drawer (DrawPointer): MLX wrapper
        entry (tuple[int, int]): Entry coordinate
        path (str): The path from entry to exit_

    Returns:
        None
    """
    nx, ny = entry

    x = START_X + (nx * CELL_SIZE) + CELL_SIZE // 2 - 1
    y = START_Y + (ny * CELL_SIZE) + CELL_SIZE // 2 - 1

    for direction in path:
        if direction == "E":
            for i in range(0, CELL_SIZE):
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x + i, y, ORANGE if SHOW else BLACK
                )
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x + i, y + 1, ORANGE if SHOW else BLACK
                )
            x += CELL_SIZE
        elif direction == "W":
            for i in range(0, CELL_SIZE):
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x - i, y, ORANGE if SHOW else BLACK
                )
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x - i, y + 1, ORANGE if SHOW else BLACK
                )
            x -= CELL_SIZE
        elif direction == "N":
            for i in range(0, CELL_SIZE):
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x, y - i, ORANGE if SHOW else BLACK
                )
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x + 1, y - i, ORANGE if SHOW else BLACK
                )
            y -= CELL_SIZE
        elif direction == "S":
            for i in range(0, CELL_SIZE):
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x, y + i, ORANGE if SHOW else BLACK
                )
                drawer.m.mlx_pixel_put(
                    drawer.mlx_ptr,
                    drawer.win_ptr, x + 1, y + i, ORANGE if SHOW else BLACK
                )
            y += CELL_SIZE


def draw_maze(drawer: DrawPointer, maze: list[str]) -> None:
    """
    Draws the whole maze

    Args:
        drawer (DrawPointer): MLX wrapper
        maze (list[str]): The maze represented in hexadecimal

    Returns:
        None
    """
    x = START_X
    y = START_Y

    for i in maze:
        for j in i:
            cell = walls_(j)
            draw_cell(drawer, cell, x, y)
            x += CELL_SIZE
        x = START_X
        y += CELL_SIZE



def options_placeholder(drawer: DrawPointer) -> None:
    """
    Prints the options in the window

    Args:
        drawer (DrawPointer): MLX wrapper

    Returns:
        None
    """
    drawer.m.mlx_string_put(
        drawer.mlx_ptr,
        drawer.win_ptr,
        150,
        SCREEN_H - 150,
        WHITE,
        "1. Re-generate maze",
    )
    drawer.m.mlx_string_put(
        drawer.mlx_ptr,
        drawer.win_ptr,
        450,
        SCREEN_H - 150,
        WHITE,
        "2. Flip the colors"
    )
    drawer.m.mlx_string_put(
        drawer.mlx_ptr,
        drawer.win_ptr,
        750,
        SCREEN_H - 150,
        WHITE,
        "3. Show/Hide path"
    )
    drawer.m.mlx_string_put(
        drawer.mlx_ptr,
        drawer.win_ptr,
        1050,
        SCREEN_H - 150,
        WHITE,
        "4. Quit program"
    )


def keys(key: int, drawer: DrawPointer) -> None:
    """
    Key events;
    Re-generate maze when pressing 1
    Flip the colors when pressing 2
    Show/Hide the path when pressing 3
    Quits the program when pressing 4

    Args:
        key (int): Key evenet
        drawer (DrawPointer): MLX wrapper

    Returns:
        None
    """
    global output
    global FLIP
    global SHOW

    if key == 50:  # Flip the colors when pressing '2'
        FLIP = not FLIP
        options_placeholder(drawer)
        draw_maze(drawer, output["maze"])
    elif key == 51:  # Show/Hide the path when pressing '3'
        SHOW = not SHOW
        drawer.m.mlx_clear_window(drawer.mlx_ptr, drawer.win_ptr)
        options_placeholder(drawer)
        draw_maze(drawer, output["maze"])
    elif key == 52:  # Quits the program when pressing '4'
        drawer.m.mlx_loop_exit(drawer.mlx_ptr)


def mlx_gui() -> None:
    """
    Initializes the DrawPointer class, which is used to create
    the window which the maze is drawn, and draws the maze

    Args:
        None

    Returns:
        None
    """
    drawer = DrawPointer()

    def close_window(dummy: Any) -> None:
        drawer.m.mlx_loop_exit(drawer.mlx_ptr)

    drawer.win_ptr = drawer.m.mlx_new_window(
        drawer.mlx_ptr, SCREEN_W, SCREEN_H, "a_maze_ing"
    )
    drawer.m.mlx_hook(drawer.win_ptr, 33, 0, close_window, None)
    drawer.m.mlx_key_hook(drawer.win_ptr, keys, drawer)

    options_placeholder(drawer)
    draw_maze(drawer, output["maze"])

    drawer.m.mlx_loop(drawer.mlx_ptr)

mlx_gui()