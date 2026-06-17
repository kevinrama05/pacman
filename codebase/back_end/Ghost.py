from collections import deque
from abc import ABC, abstractmethod
from random import choice
import math


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

    def check_walls(self, current_cell: int) -> list[str]:
        """
        This method returns all the walls that are open
        in the current cell

        Args:
            current_cell (int): The current cell represented with
                                a number from 0 to 15

        Returns:
            list[str]: All the directions where the wall is open
        """
        open_walls = []
        dirs = [(1, "N"), (2, "E"), (4, "S"), (8, "W")]

        for bitmask, label in dirs:
            # if the result of "AND" operator is 0, the wall is open
            if (current_cell & bitmask) == 0:
                open_walls.append(label)

        return open_walls

    def bfs_next_direction(
        self,
        target: tuple[int, int],
        location: tuple[int, int],
        maze: list[list[int]],
        height: int,
        width: int
    ) -> str:
        start = (location[1], location[0])
        end = (target[1], target[0])

        the_path = ""
        queue = deque([(start, "")])
        visited = {start}
        movements = {
            "N": (-1, 0),  # up one row
            "E": (0, 1),  # right one column
            "S": (1, 0),  # down one row
            "W": (0, -1),  # left one column
        }

        while queue:
            (current_row, current_col), current_path = queue.popleft()

            if (current_row, current_col) == end:
                return current_path[0] if len(current_path) != 0 else self.direction

            cell_value = maze[current_row][current_col]
            open_walls = self.check_walls(cell_value)

            for wall in open_walls:
                row_delta, column_delta = movements[wall]
                new_row = current_row + row_delta
                new_col = current_col + column_delta
                coords = (new_row, new_col)

                if 0 <= new_row < height and 0 <= new_col < width:
                    if coords not in visited:
                        visited.add(coords)
                        queue.append(((new_row, new_col), current_path + wall))

        print("The path: " + the_path)
        return the_path[0] if len(the_path) != 0 else self.opposite_directions[self.direction]


    def choose_the_path(
            self,
            target_location: tuple[int, int] | None,
            current_cell: int,
            maze_length: int,
            maze_width: int,
            direction: str | None = None,
            ghost: str | None = None) -> str:
        DIRECTIONS = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        PRIORITY_DEFAULT = {'N': 0, 'W': 1, 'S': 2, 'E': 3}
        PRIORITY_ALT = {'N': 0, 'E': 1, 'S': 2, 'W': 3}

        if direction is None:
            direction = self.direction

        opposite = self.opposite_directions[direction]

        valid_moves = {
            key: value
            for i, (key, value) in enumerate(DIRECTIONS.items())
            if not (current_cell >> i) & 1 and key != opposite
        }

        if not valid_moves:
            return opposite

        if target_location is None:
            return choice(list(valid_moves.keys()))

        x, y = self.current_location
        target_x, target_y = target_location
        priority = PRIORITY_DEFAULT if ghost is None else PRIORITY_ALT

        best_direction = None
        best_key = None

        for key, (dx, dy) in valid_moves.items():
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < maze_length and 0 <= new_y < maze_width):
                continue

            distance = abs(new_x - target_x) + abs(new_y - target_y)
            sort_key = (distance, priority[key])

            if best_key is None or sort_key < best_key:
                best_key = sort_key
                best_direction = key

        return best_direction if best_direction is not None else opposite

 
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
