import pygame
from codebase.back_end.Maze import Maze
import sys
sys.setrecursionlimit(1000000)
pacman_maze = Maze(sys.argv[1])
WIDTH = pacman_maze.configs['width']
HEIGHT = pacman_maze.configs['height']

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W, SCREEN_H = screen.get_size()

CELL_SIZE = max(2, min(SCREEN_W // WIDTH, SCREEN_H // HEIGHT))
if CELL_SIZE > 60:
    CELL_SIZE = 60

START_X = (SCREEN_W - WIDTH * CELL_SIZE) // 2
START_Y = (SCREEN_H - HEIGHT * CELL_SIZE) // 2


def get_walls(hex_value: str) -> list[bool]:
    value = int(hex_value, 16)
    bit_length = len(hex_value) * 4
    binary_str = format(value, f"0{bit_length}b")
    return [c == "1" for c in binary_str]

def build_maze(screen: pygame.Surface, maze: list[list[int]]) -> list[pygame.Rect]:
    walls = []
    x = START_X
    y = START_Y
    n = 5
    for i in maze:
        for j in i:
            cell = get_walls(format(j, 'X'))
            if False not in cell:
                pygame.draw.rect(screen, (0, 0, 255), (x + 1, y + 1, CELL_SIZE - 6, CELL_SIZE - 6))
            if cell[3]:
                walls.append(pygame.draw.rect(screen, (255,255,255), (x, y, CELL_SIZE, 1)))
            if cell[2]:
                walls.append(pygame.draw.rect(screen, (255,255,255), (x + CELL_SIZE - 1, y, 1, CELL_SIZE)))
            if cell[1]:
                walls.append(pygame.draw.rect(screen, (255,255,255), (x, y + CELL_SIZE - 1, CELL_SIZE, 1)))
            if cell[0]:
                walls.append(pygame.draw.rect(screen, (255,255,255), (x, y, 1, CELL_SIZE)))
            x += CELL_SIZE
        x = START_X
        y += CELL_SIZE
    return walls

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

running = True
x, y = pacman_maze.pacman.current_location
pacman_x, pacman_y = START_X + x * CELL_SIZE + 1, START_Y + y * CELL_SIZE
print(x, y)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("black")
    pacman = pygame.image.load('pacman_assets/pacman_half_open_up.png').convert_alpha()
    pacman = pygame.transform.scale(pacman, (CELL_SIZE - 2, CELL_SIZE - 2))
    screen.blit(pacman, (pacman_x, pacman_y))
    
    walls = build_maze(screen, pacman_maze.maze)
    # draw_maze(pacman_maze.maze, screen)
    pygame.display.flip()

pygame.quit()