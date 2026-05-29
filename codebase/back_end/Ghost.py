from abc import ABC, abstractmethod
from random import choice


class Ghost(ABC):
    """
    The Ghost abstract class is the base class for the
    four ghosts which will be used for the PacMan game.
    A ghost has two modes: Frightened and Non-frightened
    
    On the Frightened mode, the ghosts are all edible, and
    they choose a random valid direction, and this mode is
    activated when the pacman eats a super pacgum.

    On the Non-frightened mode, they are two sub-modes.
    The first one is the Chase Mode, where each ghost chases
    the pacman according to their instructions. The second mode
    is Scatter Mode. On this mode, the ghosts wander around in a 
    specific location. 

    Attributes:
        scatter_mode (bool): If this is True, the ghosts are in Scatter
                             Mode. Else, they are in Chase Mode.
        frightened_mode (bool): If this is True, the ghosts are in Frightened
                                Mode, regardless of the scatter_mode value
    """
    def __init__(self) -> None:
        self.scatter_mode = True
        self.frightened_mode = False
        self.origin_mode = False
        self.opposite_directions = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def change_mode(self, origin: str | None = None) -> None:
        if origin == 'origin':
            self.origin_mode = True
            return
        if self.scatter_mode:
            self.scatter_mode = False
        else:
            self.scatter_mode = True

    def choose_the_path(
            self,
            target_location: tuple[int, int] | None,
            current_cell: int,
            maze_length: int,
            maze_width: int,
            direction: str | None = None) -> str:
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }
        if direction == None:
            direction = self.direction
        valid_moves = {}
        for i, (key, value) in enumerate(directions.items()):
            if not (current_cell >> i) & 1:
                if key != self.opposite_directions[direction]:
                    valid_moves[key] = value

        if target_location != None:
            distances = {}
            for key, value in valid_moves.items():
                x, y = self.current_location
                nx, ny = value
                new_x, new_y = x + nx, y + ny
                if 0 <= new_x < maze_length and 0 <= new_y < maze_width:
                    pacman_x, pacman_y = target_location
                    distance = abs(new_x - pacman_x) + abs(new_y - pacman_y)
                    distances[key] = distance

            priority = {'N': 0, 'W': 1, 'S': 2, 'E': 3}

            sorted_d = dict(sorted(distances.items(), key=lambda item: (-item[1], -priority[item[0]])))

            return self.opposite_directions[direction] if sorted_d == {} else list(sorted_d.keys())[-1]
        
        else:
            return choice(list(valid_moves.keys())) if valid_moves != {} else self.opposite_directions[direction]
 
    def enter_frightened_mode(self) -> None:
        """
        Enters Frightened Mode

        Args:
            None

        Returns:
            None
        """
        self.frightened_mode = True

    def exit_frightened_mode(self) -> None:
        """
        Exits Frightened Mode

        Args:
            None

        Returns:
            None
        """
        self.frightened_mode = False

    def move(self, maze: list[list[int]], pacman_location: tuple[int, int]) -> None:
        """
        Based on the mode of the ghost, it moves in the maze.

        Args:
            None

        Returns:
            None
        """
        if self.origin_mode:
            self.return_to_origin(maze)
        elif self.frightened_mode:
            self.move_frightened(maze)
        elif self.scatter_mode:
            self.move_scatter(maze)
        elif not self.scatter_mode:
            self.move_chase(pacman_location, maze)

    def move_scatter(self, maze: list[list[int]]) -> None:
        directions = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        target = self.origin
        current_cell = maze[self.current_location[1]][self.current_location[0]]
        direction = self.choose_the_path(target, current_cell, len(maze), len(maze[0]))
        self.offset(direction)

    def move_frightened(self, maze: list[list[int]]) -> None:
        valid_moves = {}
        current_cell = maze[self.current_location[1]][self.current_location[0]]
        next_move = self.choose_the_path(None, current_cell, len(maze), len(maze[0]))
        self.offset(next_move)

    def return_to_origin(self, maze: list[list[int]]) -> None:
        if self.current_location != self.origin:
            direction = self.choose_the_path(self.origin, maze[self.current_location[1]][self.current_location[0]], len(maze), len(maze[0]))

        self.offset(direction)
        if self.current_location == self.origin:
            self.origin_mode = False

    def offset(self, direction: str) -> None:
        if direction == 'N':
            self.move_up()
            self.direction = 'N'
        elif direction == 'S':
            self.move_down()
            self.direction = 'S'
        elif direction == 'E':
            self.move_right()
            self.direction = 'E'
        elif direction == 'W':
            self.move_left()
            self.direction = 'W'

    @abstractmethod
    def move_chase(
        self,
        target_location: tuple[int, int],
        maze: list[list[int]]) -> None:
        """
        When in Chase Mode, each ghost moves according to its instructions.
        The instructions differ from one ghost to another

        Args:
            None

        Returns:
            None
        """
        pass

    def move_up(self) -> None:
        """
        Moves the Pacman up

        Args:
            None

        Returns:
            None
        """
        x, y = self.current_location
        self.current_location = (x, y - 1)

    def move_down(self) -> None:
        """
        Moves the Pacman down

        Args:
            None

        Returns:
            None
        """
        x, y = self.current_location
        self.current_location = (x, y + 1)

    def move_left(self) -> None:
        """
        Moves the Pacman left

        Args:
            None

        Returns:
            None
        """
        x, y = self.current_location
        self.current_location = (x - 1, y)

    def move_right(self) -> None:
        """
        Moves the Pacman right

        Args:
            None

        Returns:
            None
        """
        x, y = self.current_location
        self.current_location = (x + 1, y)
