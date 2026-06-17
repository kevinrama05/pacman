import pygame
from codebase.back_end.Maze import Constants

class PacMan:
    """
    This class is responsible of keeping track of the pacman
    on the entirety of the game. It checks different things, like
    the lives remaining, the pacgums, super pacgums and ghosts eaten,
    the total points he has, and directions where can he go

    Args:
        points_per_pacgum (int): Points per pacgum eaten
        points_per_super_pacgum (int): Points per super pacgum eaten
        points_per_ghost (int): Points per ghost eaten
        lives (int): The lives remaining
    
    Attributes:
        points_per_pacgum (int): Points per pacgum eaten
        points_per_super_pacgum (int): Points per super pacgum eaten
        points_per_ghost (int): Points per ghost eaten
        lives (int): The lives remaining
        total_points (int): The accumulated points
        pacgums (int): Total number of pacgums eaten
        super_pacgums (int): Total number of super pacgums eaten
        ghosts (int): Total number of ghosts eaten
    """
    def __init__(
            self,
            points_per_pacgum: int,
            points_per_super_pacgum: int,
            points_per_ghost: int,
            lives: int,
            spawn_point: tuple[int, int],
            constants: Constants) -> None:
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.lives = lives
        self.current_location = spawn_point
        self.total_points = 0
        self.pacgums = 0
        self.super_pacgums = 0
        self.ghosts = 0
        self.direction = 'N'
        self.frames = {}
        self.frame = 1
        self.cell_size = constants.cell_size
        for i in range(1, 5):
            f = {}
            fr = pygame.image.load(f'assets/player_images/{i}.png').convert_alpha()
            fr = pygame.transform.scale(fr, (constants.cell_size - 2, constants.cell_size - 2))
            f['N'] = pygame.transform.rotate(fr, 90)
            f['S'] = pygame.transform.rotate(fr, 270)
            f['W'] = pygame.transform.rotate(fr, 180)
            f['E'] = fr
            f['mask_N'] = pygame.mask.from_surface(f['N'])
            f['mask_S'] = pygame.mask.from_surface(f['S'])
            f['mask_W'] = pygame.mask.from_surface(f['W'])
            f['mask_E'] = pygame.mask.from_surface(f['E'])
            self.frames[f'frame_{i}'] = f
        self.pacman_x = constants.start_x + self.current_location[0] * constants.cell_size
        self.pacman_y = constants.start_y + self.current_location[1] * constants.cell_size
        self.distance_completed = 0
        self.pacman_speed = constants.cell_size // 13

    def pacgum_eaten(self) -> None:
        """
        Increases the total poins when pacman eats a pacgum, and
        the total of pacgums eaten
        """
        self.total_points += self.points_per_pacgum
        self.pacgums += 1

    def super_pacgum_eaten(self) -> None:
        """
        Increases the total poins when pacman eats a super pacgum, and
        the total of super pacgums eaten
        """
        self.total_points += self.points_per_super_pacgum
        self.super_pacgums += 1

    def ghosts_eaten(self) -> None:
        """
        Increases the total poins when pacman eats a ghost, and
        the total of ghosts eaten
        """
        self.total_points += self.points_per_ghost
        self.ghosts += 1

    def remove_a_life(self) -> bool:
        """
        Removes a live frome the pacman lives. If the lives is
        greater than 0, or after the live is removed, is still greater than 0,
        it returns True, else it returns False
        """
        if self.lives == 0:
            return False
        if self.lives - 1 == 0:
            self.lives -= 1
            return False
        self.lives -= 1
        return True
    
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
        self.change_direction('N')

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
        self.change_direction('S')

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
        self.change_direction('W')

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
        self.change_direction('E')
    
    def change_direction(self, direction: str) -> None:
        self.direction = direction

    def get_speed(self, booster: bool) -> int:
        if booster:
            return self.pacman_speed * 2
        else:
            return self.pacman_speed

    def can_move(self, direction: str, maze: list[list[int]]) -> bool:
        DIRECTIONS = {
            'N': 0,
            'E': 1,
            'S': 2,
            'W': 3
        }

        x, y = self.current_location
        result = bool((maze[y][x] >> DIRECTIONS[direction]) & 1)
        return not result
    
    def move(self, direction: str) -> None:
        if direction == 'N':
            self.move_up()
        elif direction == 'S':
            self.move_down()
        elif direction == 'E':
            self.move_right()
        elif direction == 'W':
            self.move_left()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.frames[f'frame_{self.frame}'][self.direction], (self.pacman_x, self.pacman_y))

    def next_frame(self) -> None:
        if self.frame == 4:
            self.frame = 1
        else:
            self.frame += 1

    def pixel_move(
        self,
        current_direction: str,
        booster: bool,
        screen: pygame.Surface,
        maze: list[list[int]]
    ) -> None:
        if self.distance_completed == 0:
            if self.can_move(current_direction, maze):
                self.change_direction(current_direction)

            elif not self.can_move(self.direction, maze):
                return

        if self.distance_completed + self.get_speed(booster) > self.cell_size:
            speed = self.cell_size - self.distance_completed
        else:
            speed = self.get_speed(booster)

        DIRECTIONS = {
            'W': (-speed, 0),
            'E': (speed, 0),
            'S': (0, speed),
            'N': (0, -speed)
        }

        nx, ny = DIRECTIONS[self.direction]

        self.pacman_x += nx
        self.pacman_y += ny

        self.distance_completed += speed

        if self.distance_completed >= self.cell_size:
            self.distance_completed = 0
            self.move(self.direction)

        self.draw(screen)