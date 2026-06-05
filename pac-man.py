from codebase.back_end.Maze import Maze
from screen_renders import (
    MainMenu, PlayingScreen,PauseMenu
)
import pygame
import sys

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
def setup_fonts():
    pygame.init()
    pygame.font.init()

    fonts = {
        "title": pygame.font.SysFont("Impact", 190),
        "menu": pygame.font.SysFont("Arial", 40),
        "hint": pygame.font.SysFont("Arial", 40)
    }

    return fonts


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <configfile.json>")
        sys.exit(1)

    clock = pygame.time.Clock()
    maze_data = Maze(sys.argv[1])
    maze_data.place_pacgums()
    fonts = setup_fonts()
    screen = maze_data.constants.screen

    # creates the window
    booster = False
    stopper = False
    main_mode = MainMenu(screen, fonts, {})
    playing = PlayingScreen(screen, maze_data.constants.cell_size)
    pause = PauseMenu(screen, fonts)

    current_state = "MENU"
    frames = 0
    running = True
    while running:
        if frames % 6 == 0:
            maze_data.pacman.next_frame()
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
                            current_state = "MENU"

                # --- OTHER STATES ---
                elif current_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        current_state = "PLAYING"
                    if event.key == pygame.K_i:
                        current_state = "INSTRUCTIONS"
                
                if current_state == 'PLAYING':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        CURRENT_DIRECTION = 'N'
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        CURRENT_DIRECTION = 'S'
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        CURRENT_DIRECTION = 'W'
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        CURRENT_DIRECTION = 'E'
                    if event.key == pygame.K_p:
                        stopper = not stopper
                    if event.key == pygame.K_b:
                        booster = not booster
                    

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
            maze_data.pacman.draw(screen)
            maze_data.blinky.draw(screen)
            maze_data.inky.draw(screen)
            maze_data.pinky.draw(screen)
            maze_data.clyde.draw(screen)
            if maze_data.collision():
                print('Collision')
            maze_data.blinky.pixel_move(stopper, screen, maze_data.maze, maze_data.pacman.current_location)
            maze_data.inky.pixel_move(stopper, screen, maze_data.maze, maze_data.pacman.current_location)
            maze_data.pinky.pixel_move(stopper, screen, maze_data.maze, maze_data.pacman.current_location)
            maze_data.clyde.pixel_move(stopper, screen, maze_data.maze, maze_data.pacman.current_location)
            maze_data.pacman.pixel_move(CURRENT_DIRECTION, booster, screen, maze_data.maze)
        elif current_state == "PAUSE":
            pause.draw_pausemenu()
        frames += 1
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
