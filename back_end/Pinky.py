from back_end.Ghost import Ghost
from back_end.PacMan import PacMan
from back_end.constants import Constants
import pygame


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
    def __init__(self, origin: tuple[int, int], constants: Constants) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        x, y = self.current_location
        self.direction = 'N'
        self.cell_size = constants.cell_size
        self.pinky_x = constants.start_x + x * constants.cell_size
        self.pinky_y = constants.start_y + y * constants.cell_size
        self.pinky_img = pygame.image.load(
            'assets/ghost_images/pink.png').convert_alpha()
        self.pinky_img = pygame.transform.scale(
            self.pinky_img,
            (constants.cell_size - 2, constants.cell_size - 2))
        self.pinky_dead = pygame.image.load(
            'assets/ghost_images/powerup.png').convert_alpha()
        self.pinky_dead = pygame.transform.scale(
            self.pinky_dead,
            (constants.cell_size - 2, constants.cell_size - 2))
        self.eyes = pygame.image.load(
            "assets/ghost_images/dead.png").convert_alpha()
        self.eyes = pygame.transform.scale(
            self.eyes, (constants.cell_size - 2, constants.cell_size - 2))
        self.distance_completed = 0
        self.speed = max(1, constants.cell_size // 11)
        self.speed_dead = max(1, constants.cell_size // 9)
        self.speed_frightened = max(1, constants.cell_size // 30)

    def calculate_target(
            self,
            pacman: PacMan,
            height: int,
            width: int
    ) -> tuple[int, int]:
        x, y = pacman.current_location
        if pacman.direction == 'N':
            y -= 4
        elif pacman.direction == 'S':
            y += 4
        elif pacman.direction == 'E':
            x += 4
        elif pacman.direction == 'W':
            x -= 4

        x = max(0, min(x, width - 1))
        y = max(0, min(y, height - 1))
        return (x, y)

    def move_chase(
            self,
            target_location: tuple[int, int],
            maze: list[list[int]]) -> None:

        target = target_location

        direction = self.bfs_next_direction(
            target, self.current_location, maze, len(maze), len(maze[0]))

        self.offset(direction)

    def draw(self, screen: pygame.Surface) -> None:
        if self.origin_mode:
            screen.blit(self.eyes, (self.pinky_x, self.pinky_y))
        elif self.frightened_mode:
            screen.blit(self.pinky_dead, (self.pinky_x, self.pinky_y))
        else:
            screen.blit(self.pinky_img, (self.pinky_x, self.pinky_y))

    def get_speed(self, stopper: bool) -> int:
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
        maze: list[list[int]],
        pacman_location: tuple[int, int]
    ) -> None:
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

        self.pinky_x += nx
        self.pinky_y += ny

        self.distance_completed += speed

        if self.distance_completed >= self.cell_size:
            self.distance_completed = 0
