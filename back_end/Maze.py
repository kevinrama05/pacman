from mazegenerator.mazegenerator import MazeGenerator as Mg
from back_end.config_parser import ParseJSON
from back_end.constants import Constants
from back_end.Ghost import Ghost
import random
import pygame
from back_end.PacMan import PacMan
from back_end.Blinky import Blinky
from back_end.Inky import Inky
from back_end.Pinky import Pinky
from back_end.Clyde import Clyde


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
        pacgums (dict[tuple[int, int]], bool]):
                        All the locations of the pacgums, and if they are
                        eaten or not
        current_level (int): The current level
    """
    def __init__(self, path: str) -> None:
        self.configs = ParseJSON(path).validate_json()
        self.constants = Constants(self.configs)
        self.height = self.configs['height']
        self.width = self.configs['width']
        self.maze = MazeGenerator(
            size=(self.width, self.height),
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
        self.pacgums = {}
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
        # Corners hold super pacgums; ghost spawns and pacman spawn stay empty
        excluded = {
            (0, 0), (1, 0), (self.width - 1, 0), (self.width - 1, 1),
            (self.width - 1, self.height - 1),
            (self.width - 2, self.height - 1),
            (0, self.height - 2), (0, self.height - 1),
            self.pacman_position
        }
        coords = [
            (i, j)
            for j in range(self.height)
            for i in range(self.width)
            if (i, j) not in excluded and self.maze[j][i] != 15
        ]
        count = min(self.configs['pacgum'] - 4, len(coords))
        for x, y in random.sample(coords, count):
            self.pacgums[x, y] = False

        self.pacgums[(0, 0)] = False
        self.pacgums[(self.width - 1, 0)] = False
        self.pacgums[(self.width - 1, self.height - 1)] = False
        self.pacgums[(0, self.height - 1)] = False

    def collision_type(self) -> tuple[str, Ghost | None, bool]:
        def circles_collide(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
            radius1 = rect1.width / 2
            radius2 = rect2.width / 2
            dx = rect1.centerx - rect2.centerx
            dy = rect1.centery - rect2.centery
            return dx * dx + dy * dy <= (radius1 + radius2) ** 2
        pacman_rect = pygame.Rect(
            self.pacman.pacman_x + 2,
            self.pacman.pacman_y + 2,
            self.constants.cell_size - 4, self.constants.cell_size - 4)
        blinky_rect = pygame.Rect(
            self.blinky.blinky_x + 2,
            self.blinky.blinky_y + 2,
            self.constants.cell_size - 4, self.constants.cell_size - 4)
        pinky_rect = pygame.Rect(
            self.pinky.pinky_x + 2,
            self.pinky.pinky_y + 2,
            self.constants.cell_size - 4, self.constants.cell_size - 4)
        inky_rect = pygame.Rect(
            self.inky.inky_x + 2,
            self.inky.inky_y + 2,
            self.constants.cell_size - 4, self.constants.cell_size - 4)
        clyde_rect = pygame.Rect(
            self.clyde.clyde_x + 2,
            self.clyde.clyde_y + 2,
            self.constants.cell_size - 4, self.constants.cell_size - 4)
        ghosts = (self.blinky, self.pinky, self.inky, self.clyde)
        for i, j in zip(
                (blinky_rect, pinky_rect, inky_rect, clyde_rect), ghosts):
            if circles_collide(pacman_rect, i):
                if j.origin_mode:
                    return 'origin', j, True
                elif j.frightened_mode:
                    return 'frightened', j, True
                else:
                    return 'normal', j, True
        return 'none', None, False

    def reset(self) -> None:
        start_x = self.constants.start_x
        start_y = self.constants.start_y
        cell_size = self.constants.cell_size
        pacman_position_y = int(int(self.height - 5) / 2 + 1)
        pacman_position_x = int(int(self.width - 7) / 2 + 2)
        self.pacman.current_location = (pacman_position_x, pacman_position_y)
        self.direction = 'N'
        self.frame = 1
        self.pacman.pacman_x = start_x + pacman_position_x * cell_size
        self.pacman.pacman_y = start_y + pacman_position_y * cell_size
        self.pacman.distance_completed = 0

        self.blinky.current_location = self.blinky.origin
        self.blinky.direction = 'S'
        x, y = self.blinky.current_location
        self.blinky.blinky_x = start_x + x * cell_size
        self.blinky.blinky_y = start_y + y * cell_size
        self.blinky.exit_frightened_mode()
        self.blinky.origin_mode = False
        self.blinky.scatter_mode = True
        self.blinky.distance_completed = 0

        self.pinky.current_location = self.pinky.origin
        self.pinky.direction = 'S'
        x, y = self.pinky.current_location
        self.pinky.pinky_x = start_x + x * cell_size
        self.pinky.pinky_y = start_y + y * cell_size
        self.pinky.exit_frightened_mode()
        self.pinky.origin_mode = False
        self.pinky.scatter_mode = True
        self.pinky.distance_completed = 0

        self.inky.current_location = self.inky.origin
        self.inky.direction = 'N'
        x, y = self.inky.current_location
        self.inky.inky_x = start_x + x * cell_size
        self.inky.inky_y = start_y + y * cell_size
        self.inky.exit_frightened_mode()
        self.inky.origin_mode = False
        self.inky.scatter_mode = True
        self.inky.distance_completed = 0

        self.clyde.current_location = self.clyde.origin
        self.clyde.direction = 'S'
        x, y = self.clyde.current_location
        self.clyde.clyde_x = start_x + x * cell_size
        self.clyde.clyde_y = start_y + y * cell_size
        self.clyde.exit_frightened_mode()
        self.clyde.origin_mode = False
        self.clyde.scatter_mode = True
        self.clyde.distance_completed = 0

    def change_mode_all(self, origin: str | None = None) -> None:
        self.clyde.change_mode(origin)
        self.blinky.change_mode(origin)
        self.inky.change_mode(origin)
        self.pinky.change_mode(origin)

    def total_reset(self) -> None:
        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=random.randint(0, 1000)).maze
        pacman_position_y = int(int(self.height - 5) / 2 + 1)
        pacman_position_x = int(int(self.width - 7) / 2 + 2)
        self.pacman_position = pacman_position_x, pacman_position_y
        current_score = self.pacman.total_points
        self.pacman = PacMan(
            self.configs['points_per_pacgum'],
            self.configs['points_per_super_pacgum'],
            self.configs['points_per_ghost'],
            self.configs['lives'],
            self.pacman_position,
            self.constants,
            current_score
        )
        self.blinky = Blinky((1, 0), self.constants)
        self.inky = Inky((self.width - 1, 1), self.constants)
        self.pinky = Pinky((self.width - 2, self.height - 1), self.constants)
        self.clyde = Clyde((0, self.height - 2), self.constants)
        self.pacgums = {}
        self.place_pacgums()
        self.levels = self.configs['levels']
        self.lives = self.configs['lives']

    def new_game(self) -> None:
        """Restarts from level 1 with the configured seed and zero score"""
        self.maze = MazeGenerator(
            size=(self.width, self.height),
            seed=self.configs['seed']).maze
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
        self.pacgums = {}
        self.place_pacgums()
        self.current_level = 1

    def next_level(self) -> bool | None:
        if self.current_level == self.configs['levels']:
            return True
        else:
            self.total_reset()
            self.current_level += 1
            return None
