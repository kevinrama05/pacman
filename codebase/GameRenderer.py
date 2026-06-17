import pygame
from back_end.Maze import Maze
import sys
sys.setrecursionlimit(1000000)
pacman_maze = Maze(sys.argv[1])
WIDTH = pacman_maze.configs['width']
HEIGHT = pacman_maze.configs['height']

 

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W, SCREEN_H = screen.get_size()

CELL_SIZE = max(2, min(SCREEN_W // WIDTH, SCREEN_H // HEIGHT))
if CELL_SIZE > 40:
    CELL_SIZE = 40

START_X = (SCREEN_W - WIDTH * CELL_SIZE) // 2
START_Y = (SCREEN_H - HEIGHT * CELL_SIZE) // 2


def get_walls(hex_value: str) -> list[bool]:
    value = int(hex_value, 16)
    bit_length = len(hex_value) * 4
    binary_str = format(value, f"0{bit_length}b")
    return [c == "1" for c in binary_str]


def draw_maze(maze: list[list[int]], screen: pygame.Surface) -> None:
    x = START_X
    y = START_Y
    walls = []
    for row in maze:
        for cell in row:
            walls = get_walls(format(cell, 'X'))  # fix: int -> proper hex string
            if False not in walls:
                pygame.draw.rect(screen, 'white', (x, y, CELL_SIZE, CELL_SIZE), 0)
            if walls[3]:
                pygame.draw.line(screen, 'white', (x, y), (x + CELL_SIZE, y))
            if walls[2]:
                pygame.draw.line(screen, 'white', (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
            if walls[1]:
                pygame.draw.line(screen, 'white', (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))
            if walls[0]:
                pygame.draw.line(screen, 'white', (x, y), (x, y + CELL_SIZE))
            x += CELL_SIZE
        x = START_X
        y += CELL_SIZE

def put_pacgums_and_mega_pacgums(pacman_maze: Maze, screen: pygame.Surface):
    for key, value in pacman_maze.pacgums_eaten.items():
        if not value:
            x, y = key
            if key in ((0, 0), (pacman_maze.width - 1, 0), (pacman_maze.width - 1, pacman_maze.height - 1), (0, pacman_maze.height - 1)):
                pygame.draw.circle(screen, (255, 255, 0), (START_X + x * CELL_SIZE + CELL_SIZE / 2, START_Y + y * CELL_SIZE + CELL_SIZE / 2), 8)
            else:
                pygame.draw.circle(screen, (255, 255, 0), (START_X + x * CELL_SIZE + CELL_SIZE / 2, START_Y + y * CELL_SIZE + CELL_SIZE / 2), 4)

def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy

clock = pygame.time.Clock()
running = True
x, y = pacman_maze.pacman.current_location
pacman_x, pacman_y = (START_X + x * CELL_SIZE + 2, START_Y + x * CELL_SIZE + 2)
speed = CELL_SIZE // 10
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("black")
    draw_maze(pacman_maze.maze, screen)
    pacman_maze.place_pacgums()
    put_pacgums_and_mega_pacgums(pacman_maze, screen)

    blinky = pygame.image.load('pacman_assets/pacman_half_open_down.png').convert_alpha()
    blinky = pygame.transform.scale(blinky, (CELL_SIZE - 4, CELL_SIZE - 4))
    
    screen.blit(blinky, (pacman_x, pacman_y))
    pacman_x -= speed
    pygame.display.flip()
    clock.tick(60)
    print(CELL_SIZE)
pygame.quit()