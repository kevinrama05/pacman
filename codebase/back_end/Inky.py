from codebase.back_end.Ghost import Ghost
from codebase.back_end.PacMan import PacMan


class Inky(Ghost):
    """
    Inky is the light blue Ghost. The origin of Pinky is (1, 0).
    The path of Inky in Chase Mode is based on Pacman's location
    and the Blinky's location. It calculates the distance of Pacman
    and Blinky with the Euclidean equation, and it flips it 180 degrees,
    and uses that point as the target point. It goes to the best valid
    direction, according to the Euclidean equation from Inky's valid
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
        origin (tuple[int, int]): The spawn point of the Inky
        current_lovation (tuple[int, int]): The current location of Inky 
        direction (str): The direction the ghost if facing
    """
    def __init__(self, origin: tuple[int, int]) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        self.direction = 'E'

    def calculate_target(
            pacman: PacMan,
            blinky_location: tuple[int, int],
            height: int,
            width: int
        ) -> tuple[int, int]:
        x2, y2 = pacman.current_location
        if pacman.direction == 'N':
            y2 += 2
        elif pacman.direcion == 'S':
            y2 -= 2
        elif pacman.direction == 'E':
            x2 += 2
        elif pacman.direction == 'W':
            x2 -= 2

        if x2 < 0:
            x2 = 0
        elif x2 >= width:
            x2 = width - 1
        if y2 < 0:
            y2 = 0
        elif y2 >= width:
            y2 = width - 1

        x1, y1 = blinky_location

        x3 = x2 - (x2 - x1)
        y3 = y2 - (x2 - x1)

        if x3 < 0:
            x3 = 0
        elif x3 >= width:
            x3 = width - 1
        if y3 < 0:
            y3 = 0
        elif y3 >= width:
            y3 = width - 1
            
        return (x3, y3)
    
    def move_chase(
        self,
        target_location: tuple[int, int],
        maze: list[list[int]]) -> None:
        
        target = target_location
        current_cell = maze[self.current_location[1]][self.current_location[0]]

        direction = self.choose_the_path(target, current_cell, len(maze), len(maze[0]))

        self.offset(direction)