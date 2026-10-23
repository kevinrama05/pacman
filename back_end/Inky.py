from back_end.Ghost import Ghost
from back_end.PacMan import PacMan
from back_end.constants import Constants
import pygame


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
    def __init__(self, origin: tuple[int, int], constants: Constants) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        self.direction = 'E'
        x, y = self.current_location
        self.cell_size = constants.cell_size
        self.inky_x = constants.start_x + x * constants.cell_size
        self.inky_y = constants.start_y + y * constants.cell_size
        self.inky_img = pygame.image.load(
            'assets/ghost_images/blue.png').convert_alpha()
        self.inky_img = pygame.transform.scale(
            self.inky_img,
            (constants.cell_size - 2, constants.cell_size - 2))
        self.inky_dead = pygame.image.load(
            'assets/ghost_images/powerup.png').convert_alpha()
        self.inky_dead = pygame.transform.scale(
            self.inky_dead,
            (constants.cell_size - 2, constants.cell_size - 2))
        self.eyes = pygame.image.load(
            "assets/ghost_images/dead.png").convert_alpha()
        self.eyes = pygame.transform.scale(
            self.eyes,
            (constants.cell_size - 2, constants.cell_size - 2))
        self.distance_completed = 0
        self.speed = max(1, constants.cell_size // 11)
        self.speed_dead = max(1, constants.cell_size // 9)
        self.speed_frightened = max(1, constants.cell_size // 30)

    def calculate_target(
            self,
            pacman: PacMan,
            blinky_location: tuple[int, int],
            height: int,
            width: int
            ) -> tuple[int, int]:
        x2, y2 = pacman.current_location
        if pacman.direction == 'N':
            y2 -= 2
        elif pacman.direction == 'S':
            y2 += 2
        elif pacman.direction == 'E':
            x2 += 2
        elif pacman.direction == 'W':
            x2 -= 2

        x2 = max(0, min(x2, width - 1))
        y2 = max(0, min(y2, height - 1))

        x1, y1 = blinky_location

        # Mirror Blinky's position through the point ahead of Pacman
        x3 = 2 * x2 - x1
        y3 = 2 * y2 - y1

        x3 = max(0, min(x3, width - 1))
        y3 = max(0, min(y3, height - 1))

        return (x3, y3)

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
            screen.blit(self.eyes, (self.inky_x, self.inky_y))
        elif self.frightened_mode:
            screen.blit(self.inky_dead, (self.inky_x, self.inky_y))
        else:
            screen.blit(self.inky_img, (self.inky_x, self.inky_y))

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

        self.inky_x += nx
        self.inky_y += ny

        self.distance_completed += speed

        if self.distance_completed >= self.cell_size:
            self.distance_completed = 0
