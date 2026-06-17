import pygame
from codebase.back_end.PacMan import PacMan
from codebase.back_end.Maze import Maze
from time import sleep


        

class Ghosts:
    def __init__(self, maze_data: Maze, cell_size):
        self.maze_data = maze_data
        self.cell_size = cell_size
        self.blinky = maze_data.blinky
        self.pinky = maze_data.pinky
        self.inky = maze_data.inky
        self.clyde = maze_data.clyde
        self.blinky_img = pygame.image.load('assets/ghost_images/red.png')
        self.pinky_img = pygame.image.load('assets/ghost_images/pink.png')
        self.inky_img = pygame.image.load('assets/ghost_images/blue.png')
        self.clyde_img = pygame.image.load('assets/ghost_images/orange.png')
        self.frightened = pygame.image.load('assets/ghost_images/powerup.png')
        self.dead = pygame.image.load('assets/ghost_images/dead.png')
        self.blinky_img = pygame.transform.scale(self.blinky_img, (cell_size - 2, cell_size - 2))
        self.pinky_img = pygame.transform.scale(self.pinky_img, (cell_size - 2, cell_size - 2))
        self.inky_img = pygame.transform.scale(self.inky_img, (cell_size - 2, cell_size - 2))
        self.clyde_img = pygame.transform.scale(self.clyde_img, (cell_size - 2, cell_size - 2))
        self.frightened = pygame.transform.scale(self.frightened, (cell_size - 2, cell_size - 2))
        self.dead = pygame.transform.scale(self.dead, (cell_size - 2, cell_size - 2))

    def move_blinky(
        self,
        x: int,
        y: int,
        distance_completed: int,
        speed: int
    ):
        if distance_completed + speed > self.cell_size:
            speed = self.cell_size - distance_completed

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.blinky.direction]

        x += nx
        y += ny

        distance_completed += speed

        if distance_completed >= self.cell_size:
            distance_completed = 0

        return x, y, distance_completed
    
    def move_inky(
        self,
        x: int,
        y: int,
        distance_completed: int,
        speed: int
    ):
        if distance_completed + speed > self.cell_size:
            speed = self.cell_size - distance_completed

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.inky.direction]

        x += nx
        y += ny

        distance_completed += speed

        if distance_completed >= self.cell_size:
            distance_completed = 0

        return x, y, distance_completed

    def move_pinky(
        self,
        x: int,
        y: int,
        distance_completed: int,
        speed: int
    ):
        if distance_completed + speed > self.cell_size:
            speed = self.cell_size - distance_completed

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.pinky.direction]

        x += nx
        y += ny

        distance_completed += speed

        if distance_completed >= self.cell_size:
            distance_completed = 0

        return x, y, distance_completed

    def move_clyde(
        self,
        x: int,
        y: int,
        distance_completed: int,
        speed: int
    ):
        if distance_completed + speed > self.cell_size:
            speed = self.cell_size - distance_completed

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.clyde.direction]

        x += nx
        y += ny

        distance_completed += speed

        if distance_completed >= self.cell_size:
            distance_completed = 0

        return x, y, distance_completed

    def draw_inky(self, screen, x, y) -> None:
        screen.blit(self.inky_img, (x, y))

    def draw_blinky(self, screen, x, y) -> None:
        screen.blit(self.blinky_img, (x, y))
    
    def draw_pinky(self, screen, x, y) -> None:
        screen.blit(self.pinky_img, (x, y))

    def draw_clyde(self, screen, x, y) -> None:
        screen.blit(self.clyde_img, (x, y))

    def movement(coordinates: tuple) -> pygame.key:
        pass

    def change_color(stage: str) -> pygame.color:
        pass

    def edible(status: str) -> bool:
        pass
 
class GumsAndPacGums:
    pass

class Pacman:
    def __init__(self, x, y, pac_man: PacMan, cell_size):
        self.grid_x = x
        self.grid_y = y
        self.cell_size = cell_size
        self.pac_man = pac_man
        self.frames = {}
        self.frame = 1
        for i in range(1, 5):
            f = {}
            fr = pygame.image.load(f'assets/player_images/{i}.png').convert_alpha()
            fr = pygame.transform.scale(fr, (self.cell_size - 2, self.cell_size - 2))
            f['N'] = pygame.transform.rotate(fr, 90)
            f['S'] = pygame.transform.rotate(fr, 270)
            f['W'] = pygame.transform.rotate(fr, 180)
            f['E'] = fr
            self.frames[f'frame_{i}'] = f

    def draw(self, screen, offset_x, offset_y):
        """Draw Pacman at the correct pixel coordinates."""
        screen.blit(self.frames[f'frame_{self.frame}'][self.pac_man.direction], (offset_x, offset_y))
    def change_frame(self) -> None:
        if self.frame == 4:
            self.frame = 1
        else:
            self.frame += 1

    def move(
        self,
        x: int,
        y: int,
        distance_completed: int,
        speed: int,
        current_direction: str,
        maze: list[list[int]]
    ):
        if distance_completed == 0:
            if self.pac_man.can_move(current_direction, maze):
                self.pac_man.change_direction(current_direction)

            elif not self.pac_man.can_move(self.pac_man.direction, maze):
                return x, y, distance_completed

        if distance_completed + speed > self.cell_size:
            speed = self.cell_size - distance_completed

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.pac_man.direction]

        x += nx
        y += ny

        distance_completed += speed

        if distance_completed >= self.cell_size:
            distance_completed = 0
            self.pac_man.move(self.pac_man.direction)

        return x, y, distance_completed

    def collision(self, ghosts: Ghosts, positions: list[tuple[int, int]], start_x, start_y) -> bool:
        pacman_location = positions[0]
        blinky_location = positions[1]
        inky_location = positions[2]
        pinky_location = positions[3]
        clyde_location = positions[4]
        pacman = pygame.Rect(pacman_location[0], pacman_location[1], self.cell_size - 2, self.cell_size - 2)
        blinky = pygame.Rect(blinky_location[0], blinky_location[1], self.cell_size - 2, self.cell_size - 2)
        inky = pygame.Rect(inky_location[0], inky_location[1], self.cell_size - 2, self.cell_size - 2)
        pinky = pygame.Rect(pinky_location[0], pinky_location[1], self.cell_size - 2, self.cell_size - 2)
        clyde = pygame.Rect(clyde_location[0], clyde_location[1], self.cell_size - 2, self.cell_size - 2)

        for i in [blinky, inky, pinky, clyde]:
            if pacman.colliderect(i):
                return True
        return False

    def spawn(self, screen):
        ...