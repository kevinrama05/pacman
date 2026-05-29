from codebase.back_end.Ghost import Ghost
from random import choice


class Blinky(Ghost):
    """
    Blinky is the Red Ghost. The origin of Blinky is (width - 2, height - 1).
    The path of Blicky in Chase mode is based on the Pacman's location, which
    is its target. It goes to the best valid direction, according to the
    Euclidean equation from Blinky's valid direction to Pacman's location.
    If they are multiple valid directions with the same Euclidean value,
    it chooses the one with the highest priority. The priorities are
    up, left, down, right

    Args:
        None

    Attributes:
        scatter_mode (bool): If this is True, the ghosts are in Scatter
                             Mode. Else, they are in Chase Mode.
        frightened_mode (bool): If this is True, the ghosts are in Frightened
                                Mode, regardless of the scatter_mode value
        origin (tuple[int, int]): The spawn point of the Blinky
        current_lovation (tuple[int, int]): The current location of Blinky
        direction (str): The direction the ghost if facing
    """
    def __init__(self, origin: tuple[int, int]) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        x, y = self.origin
        self.direction = 'S'

    def move_chase(
        self,
        target_location: tuple[int, int],
        maze: list[list[int]]) -> None:

        target = target_location
        current_cell = maze[self.current_location[1]][self.current_location[0]]

        direction = self.choose_the_path(target, current_cell, len(maze), len(maze[0]))

        self.offset(direction)