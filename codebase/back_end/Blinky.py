from codebase.back_end.Ghost import Ghost
from random import choice
from codebase.back_end.Maze import Constants
import pygame


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
    def __init__(self, origin: tuple[int, int], constants: Constants) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        self.cell_size = constants.cell_size
        x, y = self.current_location
        self.cell_size = constants.cell_size
        self.direction = 'S'
        self.blinky_x = constants.start_x + x * constants.cell_size
        self.blinky_y = constants.start_y + y * constants.cell_size
        self.blinky_img = pygame.image.load('assets/ghost_images/red.png').convert_alpha()
        self.blinky_img = pygame.transform.scale(self.blinky_img, (constants.cell_size - 2, constants.cell_size - 2))
        self.blinky_mask = pygame.mask.from_surface(self.blinky_img)
        self.distance_completed = 0
        self.speed = constants.cell_size // 10
        self.speed_dead = constants.cell_size // 3
        self.speed_frightened = constants.cell_size // 16


    def move_chase(
        self,
        target_location: tuple[int, int],
        maze: list[list[int]]) -> None:

        target = target_location
        current_cell = maze[self.current_location[1]][self.current_location[0]]

        direction = self.choose_the_path(target, current_cell, len(maze), len(maze[0]))

        self.offset(direction)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.blinky_img, (self.blinky_x, self.blinky_y))

    def get_speed(self, stopper: bool) -> None:
        if stopper:
            return 0
        elif self.origin_mode:
            return self.speed_dead
        elif self.frightened_mode:
            return self.speed_frightened
        else:
            return self.speed 

    def pixel_move(
        self,
        stopper: bool,
        screen: pygame.Surface,
        maze: list[list[int]],
        pacman_location: tuple[int, int]
    ):
        if stopper:
            return
        if self.distance_completed == 0:
            self.move(maze, pacman_location)
        if self.distance_completed + self.get_speed(stopper) > self.cell_size:
            speed = self.cell_size - self.distance_completed
        else:
            speed = self.get_speed(stopper)

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.direction]

        self.blinky_x += nx
        self.blinky_y += ny

        self.distance_completed += speed

        if self.distance_completed >= self.cell_size:
            self.distance_completed = 0