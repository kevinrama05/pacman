from codebase.back_end.Ghost import Ghost
from codebase.back_end.PacMan import PacMan


class Clyde(Ghost):
    """
    Clyde is the Orange Ghost. The origin of Clyde is (width - 1, 1).
    The path of Clyde in Chase Modeis like Blinky's path, when is 8 tiles away
    from the Pacman, based on the Eucledian equation. If it is in the ranve of
    8 tiles, it goes to Scatter Mode. And it goes back to Chase Mode after it
    goes awa from the 8 tile range. It goes It goes to the best valid
    direction, according to the Euclidean equation from Clyde's valid
    direction to the target location. If they are multiple valid directions
    with the same Euclidean value, it chooses the one with the highest
    priority. The priorities are up, left, down, right 

    Args:
        None

    Attributes:
        scatter_mode (bool): If this is True, the ghosts are in Scatter
                             Mode. Else, they are in Chase Mode.
        frightened_mode (bool): If this is True, the ghosts are in Frightened
                                Mode, regardless of the scatter_mode value
        origin (tuple[int, int]): The spawn point of the Clyde
        current_lovation (tuple[int, int]): The current location of Clyde
        direction (str): The direction the ghost if facing
    """
    def __init__(self, origin: tuple[int, int]) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        self.direction = 'S'

    def move_chase(
            self,
            target_location: tuple[int, int],
            maze: list[list[int]]
        ) -> None:
        x, y = self.current_location
        current_cell = maze[y][x]
        distance = abs(x - target_location[0]) + (y - target_location[1])
        if distance > 8:
            next_move = self.choose_the_path(target_location, current_cell, len(maze), len(maze[0]))
        else:
            next_move = self.choose_the_path(self.origin, current_cell, len(maze), len(maze[0]))
        self.offset(next_move)
