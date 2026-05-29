from codebase.back_end.Ghost import Ghost
from codebase.back_end.PacMan import PacMan


class Pinky(Ghost):
    """
    Pinky is the Pink Ghost. The origin of Pinky is (1, height - 1).
    The path of Pinky in Chase Mode is based on Pacman's location's
    fourth square in front of Pacman as target. For example, if the
    Pacman is in (10, 15) and is facing North, the target of Pinky is
    (6, 15). It goes to the best valid direction, according to the
    Euclidean equation from Pinky's valid direction to Pacman's location.
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
        origin (tuple[int, int]): The spawn point of the Pinky
        current_lovation (tuple[int, int]): The current location of Pinky 
        direction (str): The direction the ghost if facing
    """
    def __init__(self, origin: tuple[int, int]) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        self.direction = 'N'

    def calculate_target(
            pacman: PacMan,
            height: int,
            width: int
    ) -> None:
        x, y = pacman.current_location
        if pacman.direction == 'N':
            y += 4
        elif pacman.direcion == 'S':
            y -= 4
        elif pacman.direction == 'E':
            x += 4
        elif pacman.direction == 'W':
            x -= 4

        if x < 0:
            x = 0
        elif x >= width:
            x = width - 1
        if y < 0:
            y = 0
        elif y >= width:
            y = width - 1

    def move_chase(
        self,
        target_location: tuple[int, int],
        maze: list[list[int]]) -> None:

        target = target_location
        current_cell = maze[self.current_location[1]][self.current_location[0]]

        direction = self.choose_the_path(target, current_cell, len(maze), len(maze[0]))

        self.offset(direction)
