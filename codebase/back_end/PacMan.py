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
            spawn_point: tuple[int, int]) -> None:
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