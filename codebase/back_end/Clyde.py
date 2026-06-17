from codebase.back_end.Ghost import Ghost
from codebase.back_end.PacMan import PacMan
from codebase.back_end.Maze import Constants
import pygame


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
    def __init__(self, origin: tuple[int, int], constants: Constants) -> None:
        super().__init__()
        self.origin = origin
        self.current_location = self.origin
        x, y = self.current_location
        self.direction = 'S'
        self.cell_size = constants.cell_size
        self.clyde_x = constants.start_x + x * constants.cell_size
        self.clyde_y = constants.start_y + y * constants.cell_size
        self.clyde_img = pygame.image.load('assets/ghost_images/orange.png').convert_alpha()
        self.clyde_img = pygame.transform.scale(self.clyde_img, (constants.cell_size - 2, constants.cell_size - 2))
        self.clyde_mask = pygame.mask.from_surface(self.clyde_img)
        self.distance_completed = 0
        self.speed = constants.cell_size // 12
        self.speed_dead = constants.cell_size // 3
        self.speed_frightened = constants.cell_size // 16

    def move_chase(
            self,
            target_location: tuple[int, int],
            maze: list[list[int]]
        ) -> None:
        x, y = self.current_location
        distance = abs(x - target_location[0]) + (y - target_location[1])
        if distance > 8:
            next_move = self.bfs_next_direction(target_location, self.current_location, maze, len(maze), len(maze[0]))
        else:
            next_move = self.bfs_next_direction(self.origin, self.current_location, maze, len(maze), len(maze[0]))
        self.offset(next_move)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.clyde_img, (self.clyde_x, self.clyde_y))

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

        self.clyde_x += nx
        self.clyde_y += ny

        self.distance_completed += speed

        if self.distance_completed >= self.cell_size:
            self.distance_completed = 0