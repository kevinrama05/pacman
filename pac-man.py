from codebase.back_end.Maze import Maze
from screen_renders import (
    MainMenu, PlayingScreen,PauseMenu
)
from entities import Pacman, Ghosts
from config_parser import ConfigParser
import pygame
import sys
from time import sleep

def draw_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    size: int = 36,
    color: tuple[int, int, int] = (255, 255, 255),
    font_name: str | None = None
) -> None:
    """
    Draw text on the screen.

    Args:
        screen: Pygame display surface
        text: Text to display
        x, y: Position of the text
        size: Font size
        color: RGB color
        font_name: Font name (None = default font)
    """

    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


sys.setrecursionlimit(100000)
CURRENT_DIRECTION = 'N'
def setup_window() -> None:
    pygame.init()
    pygame.font.init()

    fonts = {
        "title": pygame.font.SysFont("Impact", 190),
        "menu": pygame.font.SysFont("Arial", 40),
        "hint": pygame.font.SysFont("Arial", 40)
    }

    info = pygame.display.Info()

    screen = pygame.display.set_mode((
        info.current_w, info.current_h
    ), pygame.FULLSCREEN)
    pygame.display.set_caption("Pac-Man")

    return screen, fonts, info.current_w, info.current_h

def move(screen, pacman_x, pacman_y, pacman_direction, new_direction):
    
    if screen.get_at(pacman_x, pacman_y) == (0, 255, 255):
        ...

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <configfile.json>")
        sys.exit(1)

    clock = pygame.time.Clock()
    maze_data = Maze(sys.argv[1])
    maze_data.place_pacgums()
    screen, fonts, SCREEN_W, SCREEN_H = setup_window()
    WIDTH = len(maze_data.maze[0])
    HEIGHT = len(maze_data.maze)
    CELL_SIZE = max(
        2,
        min(SCREEN_W * 3 // 4 // WIDTH, SCREEN_H * 3 // 4 // HEIGHT))
    if CELL_SIZE > 80:
        CELL_SIZE = 80
    START_X = (SCREEN_W - WIDTH * CELL_SIZE) // 2 
    START_Y = ((SCREEN_H - HEIGHT * CELL_SIZE)) // 2 


    # sorts the list for top 10 players
    # cfg = ConfigParser()
    # config = cfg.parse(sys.argv[1])
    # scores = config["highscore_filename"]
    # scores.sort(key=lambda x: x['score'], reverse=True)

    # creates the window
    
    main_mode = MainMenu(screen, fonts, {})
    playing = PlayingScreen(screen, CELL_SIZE)
    pause = PauseMenu(screen, fonts)
    pacman = Pacman(1, 1, maze_data.pacman, CELL_SIZE)
    ghosts = Ghosts(maze_data, CELL_SIZE)

    current_state = "PLAYING"
    # game loop and event handler
    x, y = maze_data.pacman.current_location
    bx, by = maze_data.blinky.current_location
    cx, cy = maze_data.clyde.current_location
    ix, iy = maze_data.inky.current_location
    px, py = maze_data.pinky.current_location
    PACMAN_X, PACMAN_Y = START_X + x * CELL_SIZE, START_Y + y * CELL_SIZE
    pacman_x, pacman_y = PACMAN_X, PACMAN_Y
    blinky_x, blinky_y = START_X + bx * CELL_SIZE, START_Y + by * CELL_SIZE
    inky_x, inky_y = START_X + ix * CELL_SIZE, START_Y + iy * CELL_SIZE
    pinky_x, pinky_y = START_X + px * CELL_SIZE, START_Y + py * CELL_SIZE
    clyde_x, clyde_y = START_X + cx * CELL_SIZE, START_Y + cy * CELL_SIZE
    speed = CELL_SIZE // 15
    ghost_speed = CELL_SIZE // 11
    print(f"Blinky: {blinky_x, blinky_y}      Inky: {inky_x, inky_y}")
    blinky_distance = 0
    inky_distance = 0
    pinky_distance = 0
    clyde_distance = 0
    distance_completed = 0
    frames = 0
    running = True
    while running:
        if frames % 6 == 0:
            pacman.change_frame()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # --- GLOBAL NAVIGATION ---
                if event.key == pygame.K_ESCAPE:
                    if current_state == "MENU":
                        running = False
                    elif current_state == "INSTRUCTIONS":
                        current_state = "MENU"
                    elif current_state == "PAUSE":
                        current_state = "PLAYING"
                    elif current_state == "PLAYING":
                        current_state = "PAUSE"

                # --- PAUSE MENU LOGIC ---
                if current_state == "PAUSE":
                    if event.key == pygame.K_UP:
                        pause.selected_index = (
                            pause.selected_index - 1
                        ) % len(pause.options)

                    elif event.key == pygame.K_DOWN:
                        pause.selected_index = (
                            pause.selected_index + 1
                        ) % len(pause.options)

                    elif event.key == pygame.K_RETURN:
                        if pause.selected_index == 0:  # RESUME
                            current_state = "PLAYING"
                        else:  # RETURN TO MENU
                            pacman_x = PACMAN_X
                            pacman_y = PACMAN_Y
                            current_state = "MENU"

                # --- OTHER STATES ---
                elif current_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        current_state = "PLAYING"
                    if event.key == pygame.K_i:
                        current_state = "INSTRUCTIONS"
                
                if current_state == 'PLAYING':
                    if event.key == pygame.K_UP:
                        CURRENT_DIRECTION = 'N'
                    if event.key == pygame.K_DOWN:
                        CURRENT_DIRECTION = 'S'
                    if event.key == pygame.K_LEFT:
                        CURRENT_DIRECTION = 'W'
                    if event.key == pygame.K_RIGHT:
                        CURRENT_DIRECTION = 'E'

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            CURRENT_DIRECTION = 'N'
        if keys[pygame.K_a]:
            CURRENT_DIRECTION = 'W'
        if keys[pygame.K_s]:
            CURRENT_DIRECTION = 'S'
        if keys[pygame.K_d]:
            CURRENT_DIRECTION = 'E'

        if current_state == "MENU":
            main_mode.draw_start_screen()
        elif current_state == "INSTRUCTIONS":
            main_mode.instructions()
        elif current_state == "PLAYING":
            playing.draw_maze(maze_data.maze, maze_data.pacgums_eaten)
            pacman.draw(screen, pacman_x, pacman_y)
            ghosts.blinky.change_mode()
            ghosts.inky.change_mode()
            ghosts.pinky.change_mode()
            ghosts.clyde.change_mode()
            if blinky_distance == 0:
                maze_data.blinky.move(maze_data.maze, maze_data.pacman.current_location)
            if pinky_distance == 0:
                maze_data.pinky.move(maze_data.maze, maze_data.pacman.current_location)
            if inky_distance == 0:
                maze_data.inky.move(maze_data.maze, maze_data.pacman.current_location)
            if clyde_distance == 0:
                maze_data.clyde.move(maze_data.maze, maze_data.pacman.current_location)
            if pacman.collision(ghosts, [(pacman_x, pacman_y), (blinky_x, blinky_y), (inky_x, inky_y), (pinky_x, pinky_y), (clyde_x, clyde_y)], START_X, START_Y):
                sleep(5)
            ghosts.draw_blinky(screen, blinky_x, blinky_y)
            ghosts.draw_pinky(screen, pinky_x, pinky_y)
            ghosts.draw_inky(screen, inky_x, inky_y)
            ghosts.draw_clyde(screen, clyde_x, clyde_y)
            blinky_x, blinky_y, blinky_distance = ghosts.move_blinky(blinky_x, blinky_y, blinky_distance, ghost_speed)
            pinky_x, pinky_y, pinky_distance = ghosts.move_pinky(pinky_x, pinky_y, pinky_distance, ghost_speed)
            inky_x, inky_y, inky_distance = ghosts.move_inky(inky_x, inky_y, inky_distance, ghost_speed)
            clyde_x, clyde_y, clyde_distance = ghosts.move_clyde(clyde_x, clyde_y, clyde_distance, ghost_speed)
            pacman_x, pacman_y, distance_completed = pacman.move(pacman_x, pacman_y, distance_completed, speed, CURRENT_DIRECTION, maze_data.maze)
            x, y = maze_data.pacman.current_location
            blx, bly = ghosts.blinky.current_location
            draw_text(screen, f'x: {blx}. y: {bly}', 0, SCREEN_H - 100)
            draw_text(screen, f"x: {x}, y: {y}", 0, SCREEN_H - 300)
        elif current_state == "PAUSE":
            pause.draw_pausemenu()
        frames += 1
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
