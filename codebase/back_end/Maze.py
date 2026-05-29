from mazegenerator.mazegenerator import MazeGenerator as Mg
from codebase.back_end.config_parser import ParseJSON
from codebase.back_end.PacMan import PacMan
from codebase.back_end.Blinky import Blinky
from codebase.back_end.Inky import Inky
from codebase.back_end.Pinky import Pinky
from codebase.back_end.Clyde import Clyde
import random


class MazeGenerator(Mg):
    def generate(self, seed: int = 0) -> None:
        random.seed(seed) if seed > 0 else random.seed()
        self._seed = seed
        self._create_empty_maze()
        self._add_42_to_maze()
        self._generate_maze(self._entryx, self._entryy, 0)

class Maze:
    """
    The Maze class is the Manager Class, that is responsible for all
    the events in the PacMan game. It checks the location of each ghost
    and the pacman, and it stores the location of all pacgums and super
    pacgums. It keeps track of each level, when is completed, and everything
    related to it.

    Args:
        path (str): The path of the JSON file, with the necessary configuration

    Attributes:
        height (int): The height of the maze
        width (int): The width of the maze
        configs (ConfigDict): The dictionary of the configurations
        maze (list[list[int]]): The maze in represented in hexadecimal numbers
        pacman (PacMan): The Pacman
        blinky (Blinky): The red ghost
        inky (Inky): The light blue ghost
        pinky (Pinky): The pink ghost
        clyde (Clyde): The orange ghost
        pacgums_eaten (dict[tuple[int, int]], bool]):
                        All the locations of the pacgums, and if they are
                        eaten or not
        current_level (int): The current level
    """
    def __init__(self, path) -> None:
        self.configs = ParseJSON(path).validate_json()
        self.height = self.configs['height']
        self.width = self.configs['width']
        self.maze = MazeGenerator(
            size=(self.height, self.width),
            seed=self.configs['seed']).maze
        pacman_position_y = int(int(self.height - 5) / 2 + 1)
        pacman_position_x = int(int(self.width - 7) / 2 + 2)
        self.pacman_position = pacman_position_x, pacman_position_y
        self.pacman = PacMan(
            self.configs['points_per_pacgum'],
            self.configs['points_per_super_pacgum'],
            self.configs['points_per_ghost'],
            self.configs['lives'],
            self.pacman_position
        )
        self.blinky = Blinky((1, 0))
        self.inky = Inky((self.width - 1, 1))
        self.pinky = Pinky((self.width - 2, self.height - 1))
        self.clyde = Clyde((0, self.height - 2))
        self.pacgums_eaten = {}
        self.levels = self.configs['levels']
        self.current_level = 1
        self.modes_duration = {
            'level_1': [6, 15, 6, 15, 6, -1],
            'level_2_5': [5, 17, 5, 17, 5, -1],
            'level_5+': [4, 18, 4, 18, 4, -1]
        }
        self.lives = self.configs['lives']

    def place_pacgums(self) -> None:
        """
        Sets the location of the pacgums

        Args:
            None

        Returns:
            None
        """
        coords = [[[i, j] for i in range(self.width)] for j in range(self.height)]
        coords[0].pop(0)
        coords[0].pop(0)
        coords[0].pop()
        coords[1].pop()
        coords[-1].pop()
        coords[-1].pop()
        coords[-2].pop(0)
        coords[-1].pop(0)

        while len(self.pacgums_eaten) < self.configs['pacgum'] - 4:
            x, y = random.choice(random.choice(coords))
            if self.maze[y][x] != 15 or self.pacman_position == (x, y) or self.pacman_position == (x, y):
                self.pacgums_eaten[x, y] = False
                for i, j in enumerate(coords[y]):
                    if j[0] == x:
                        coords[y].pop(i)
                        break

        self.pacgums_eaten[(0, 0)] = False
        self.pacgums_eaten[(self.width - 1, 0)] = False
        self.pacgums_eaten[(self.width - 1, self.height - 1)] = False
        self.pacgums_eaten[(0, self.height - 1)] = False
