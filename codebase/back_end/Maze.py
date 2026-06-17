from mazegenerator.mazegenerator import MazeGenerator as Mg
from codebase.back_end.config_parser import ParseJSON
import random
import pygame


class Constants:
    def __init__(self, json: ParseJSON) -> None:
        self.width = json['width']
        self.height = json['height']
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        self.screen_w, self.screen_h = info.current_w, info.current_h
        self.cell_size = max(
            2,
            min(self.screen_w * 3 // 4 // self.width, self.screen_h * 3 // 4 // self.height))
        if self.cell_size > 80:
            self.cell_size = 80
        self.start_x = (self.screen_w - self.width * self.cell_size) // 2
        self.start_y = (self.screen_h - self.height * self.cell_size) // 2


class MazeGenerator(Mg):
    def generate(self, seed: int = 0) -> None:
        random.seed(seed) if seed > 0 else random.seed()
        self._seed = seed
        self._create_empty_maze()
        self._add_42_to_maze()
        self._generate_maze(self._entryx, self._entryy, 0)
from codebase.back_end.PacMan import PacMan
from codebase.back_end.Blinky import Blinky
from codebase.back_end.Inky import Inky
from codebase.back_end.Pinky import Pinky
from codebase.back_end.Clyde import Clyde

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
        self.constants = Constants(self.configs)
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
            self.pacman_position,
            self.constants
        )
        self.blinky = Blinky((1, 0), self.constants)
        self.inky = Inky((self.width - 1, 1), self.constants)
        self.pinky = Pinky((self.width - 2, self.height - 1), self.constants)
        self.clyde = Clyde((0, self.height - 2), self.constants)
        self.pacgums_eaten = {}
        self.levels = self.configs['levels']
        self.current_level = 1
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

    def collision(self) -> bool:
        def circles_collide(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
            radius1 = rect1.width / 2
            radius2 = rect2.width / 2
            dx = rect1.centerx - rect2.centerx
            dy = rect1.centery - rect2.centery
            return dx * dx + dy * dy <= (radius1 + radius2) ** 2
        pacman_rect = pygame.Rect(self.pacman.pacman_x + 2, self.pacman.pacman_y + 2, self.constants.cell_size - 4, self.constants.cell_size - 4)
        blinky_rect = pygame.Rect(self.blinky.blinky_x + 2, self.blinky.blinky_y + 2, self.constants.cell_size - 4, self.constants.cell_size - 4)
        pinky_rect = pygame.Rect(self.pinky.pinky_x + 2, self.pinky.pinky_y + 2, self.constants.cell_size - 4, self.constants.cell_size - 4)
        inky_rect = pygame.Rect(self.inky.inky_x + 2, self.inky.inky_y + 2, self.constants.cell_size - 4, self.constants.cell_size - 4)
        clyde_rect = pygame.Rect(self.clyde.clyde_x + 2, self.clyde.clyde_y + 2, self.constants.cell_size - 4, self.constants.cell_size)

        for i in (blinky_rect, pinky_rect, inky_rect, clyde_rect):
            if circles_collide(pacman_rect, i):
                return True
        return False
    
    def reset(self) -> None:
        pacman_position_y = int(int(self.height - 5) / 2 + 1)
        pacman_position_x = int(int(self.width - 7) / 2 + 2)
        self.pacman.current_location = (pacman_position_x, pacman_position_y)
        self.pacman.lives -= 1
        self.direction = 'N'
        self.frame = 1
        self.pacman.pacman_x = self.constants.start_x + pacman_position_x * self.constants.cell_size
        self.pacman.pacman_y = self.constants.start_y + pacman_position_y * self.constants.cell_size
        self.pacman.distance_completed = 0

        self.blinky.current_location = self.blinky.origin
        self.blinky.direction = 'S'
        x, y = self.blinky.current_location
        self.blinky.blinky_x = self.constants.start_x + x * self.constants.cell_size
        self.blinky.blinky_y = self.constants.start_y + y * self.constants.cell_size
        self.blinky.distance_completed = 0

        self.pinky.current_location = self.pinky.origin
        self.pinky.direction = 'S'
        x, y = self.pinky.current_location
        self.pinky.pinky_x = self.constants.start_x + x * self.constants.cell_size
        self.pinky.pinky_y = self.constants.start_y + y * self.constants.cell_size
        self.pinky.distance_completed = 0

        self.inky.current_location = self.inky.origin
        self.inky.direction = 'N'
        x, y = self.inky.current_location
        self.inky.inky_x = self.constants.start_x + x * self.constants.cell_size
        self.inky.inky_y = self.constants.start_y + y * self.constants.cell_size
        self.inky.distance_completed = 0

        self.clyde.current_location = self.clyde.origin
        self.clyde.direction = 'S'
        x, y = self.clyde.current_location
        self.clyde.clyde_x = self.constants.start_x + x * self.constants.cell_size
        self.clyde.clyde_y = self.constants.start_y + y * self.constants.cell_size
        self.clyde.distance_completed = 0