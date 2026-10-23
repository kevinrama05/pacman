from back_end.Maze import Maze
from screen_renders import (
    MainMenu, PlayingScreen, PauseMenu, GameWon, GameLost
)
import pygame
import sys

sys.setrecursionlimit(100000)
CURRENT_DIRECTION = 'N'


def draw_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    font: pygame.font.Font,
    color: tuple[int, int, int] = (255, 255, 255)
) -> None:
    """
    Draw text on the screen.

    Args:
        screen: Pygame display surface
        text: Text to display
        x, y: Position of the text
        font: Pre-built pygame Font object (from setup_fonts())
        color: RGB color
    """
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def setup_fonts() -> dict[str, pygame.font.Font]:
    pygame.init()
    pygame.font.init()

    fonts = {
        "title": pygame.font.SysFont("Impact", 190),
        "menu": pygame.font.SysFont("Arial", 40),
        "hint": pygame.font.SysFont("Arial", 40),
        "game_info": pygame.font.SysFont("Arial", 35)
    }

    return fonts


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python3 pac-man.py [configfile.json]")
        sys.exit(1)
    config_path = sys.argv[1] if len(sys.argv) == 2 else "config.json"

    clock = pygame.time.Clock()
    maze_data = Maze(config_path)
    maze_data.place_pacgums()
    fonts = setup_fonts()
    screen = maze_data.constants.screen
    m = maze_data.maze
    CONST = maze_data.constants
    TOP_LEFT = (CONST.start_x, CONST.start_y)
    TOP_RIGHT = (CONST.start_x + CONST.cell_size * len(m[0]), CONST.start_y)
    BOTTOM_LEFT = (CONST.start_x, CONST.start_y + CONST.cell_size * len(m))
    BOTTOM_RIGHT = (
        CONST.start_x + CONST.cell_size * len(m[0]),
        CONST.start_y + CONST.cell_size * len(m))
    # creates the window
    game_over = False
    booster = False
    stopper = False
    death = False
    scatter = True
    frightened = False
    ghost_eaten = False
    inf = False
    highscore_file = maze_data.configs['highscore_filename']
    main_mode = MainMenu(screen, fonts, highscore_file)
    playing = PlayingScreen(screen, maze_data.constants.cell_size)
    pause = PauseMenu(screen, fonts)
    game_won = GameWon(screen, highscore_file)
    game_lost = GameLost(screen, highscore_file)

    current_state = "MENU"
    frames = 0
    death_frame = 0
    scatter_duration = 0
    chase_duration = 0
    frightened_duration = 0
    ghost_duration = 0
    origin_duration = 0
    level_timer = maze_data.configs['level_max_timer']
    level_frame = 1
    running = True
    while running:
        if frames % 6 == 0:
            maze_data.pacman.next_frame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_state == "GAME_WON":
                game_won.handle_event(event, maze_data.pacman.total_points)
            if current_state == "GAME_OVER":
                game_lost.handle_event(event, maze_data.pacman.total_points)
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
                    elif current_state in ("GAME_OVER", "GAME_WON"):
                        current_state = "MENU"

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
                        # Every game started from the menu begins fresh
                        maze_data.new_game()
                        game_won = GameWon(screen, highscore_file)
                        game_lost = GameLost(screen, highscore_file)
                        CURRENT_DIRECTION = 'N'
                        death = False
                        death_frame = 0
                        ghost_eaten = False
                        ghost_duration = 0
                        scatter = True
                        scatter_duration = 0
                        chase_duration = 0
                        frightened = False
                        frightened_duration = 0
                        level_timer = maze_data.configs['level_max_timer']
                        level_frame = 1
                        current_state = "PLAYING"
                    if event.key == pygame.K_i:
                        current_state = "INSTRUCTIONS"

                if current_state == 'PLAYING':
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        CURRENT_DIRECTION = 'N'
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        CURRENT_DIRECTION = 'S'
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        CURRENT_DIRECTION = 'W'
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        CURRENT_DIRECTION = 'E'
                    if event.key == pygame.K_p:
                        stopper = not stopper
                    if event.key == pygame.K_b:
                        booster = not booster
                    if event.key == pygame.K_i:
                        inf = not inf

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            CURRENT_DIRECTION = 'N'
        if keys[pygame.K_a]:
            CURRENT_DIRECTION = 'W'
        if keys[pygame.K_s]:
            CURRENT_DIRECTION = 'S'
        if keys[pygame.K_d]:
            CURRENT_DIRECTION = 'E'

        if current_state == "GAME_WON":
            game_won.draw()
            if not game_won.active:
                current_state = "MENU"
        elif current_state == "MENU":
            main_mode.draw_start_screen()
        elif current_state == "INSTRUCTIONS":
            main_mode.instructions()
        elif current_state == "GAME_OVER":
            game_lost.draw()
            if not game_lost.active:
                current_state = "MENU"
        elif current_state == "PLAYING":
            if death:
                if death_frame == 90:
                    death = False
                    death_frame = 0
                    maze_data.reset()
                else:
                    death_frame += 1
            elif ghost_eaten:
                if ghost_duration == 60:
                    ghost_eaten = False
                    ghost_duration = 0
                else:
                    ghost_duration += 1
            else:
                playing.draw_maze(maze_data.maze, maze_data.pacgums)
                maze_data.pacman.draw(screen)
                maze_data.blinky.draw(screen)
                maze_data.inky.draw(screen)
                maze_data.pinky.draw(screen)
                maze_data.clyde.draw(screen)
                mode, ghost, collision = maze_data.collision_type()
                if collision:
                    if mode == 'origin':
                        pass
                    elif mode == 'frightened':
                        ghost.origin_mode = True
                        ghost_eaten = True
                        maze_data.pacman.ghosts_eaten()
                    elif mode == 'normal':
                        death = True
                        scatter = True
                        scatter_duration = 0
                        chase_duration = 0
                        frightened = False
                        frightened_duration = 0
                        if not inf:
                            maze_data.pacman.remove_a_life()
                            if maze_data.pacman.lives == 0:
                                current_state = "GAME_OVER"
                if frightened:
                    if frightened_duration == 600:
                        maze_data.blinky.exit_frightened_mode()
                        maze_data.inky.exit_frightened_mode()
                        maze_data.pinky.exit_frightened_mode()
                        maze_data.clyde.exit_frightened_mode()
                        frightened = False
                        frightened_duration = 0
                    else:
                        frightened_duration += 1
                if scatter:
                    if scatter_duration == 360:
                        maze_data.change_mode_all()
                        scatter_duration = 0
                        scatter = False
                    else:
                        scatter_duration += 1
                else:
                    if chase_duration == 300:
                        maze_data.change_mode_all()
                        chase_duration = 0
                        scatter = True
                    else:
                        chase_duration += 1
                if maze_data.pacman.distance_completed == 0:
                    if maze_data.pacman.current_location in maze_data.pacgums:
                        h = len(maze_data.maze)
                        w = len(maze_data.maze[0])
                        c = ((0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1))
                        loc = maze_data.pacman.current_location
                        if (maze_data.pacman.current_location in c
                                and not maze_data.pacgums[loc]):
                            maze_data.blinky.enter_frightened_mode()
                            maze_data.inky.enter_frightened_mode()
                            maze_data.pinky.enter_frightened_mode()
                            maze_data.clyde.enter_frightened_mode()
                            frightened = True
                            frightened_duration = 0
                            maze_data.pacman.super_pacgum_eaten()
                        elif not maze_data.pacgums[loc]:
                            maze_data.pacman.pacgum_eaten()
                        maze_data.pacgums[loc] = True
                h = len(maze_data.maze)
                w = len(maze_data.maze[0])
                pinky_target = maze_data.pinky.calculate_target(
                    maze_data.pacman, h, w)
                inky_target = maze_data.inky.calculate_target(
                    maze_data.pacman,
                    maze_data.blinky.current_location, h, w)
                maze_data.blinky.pixel_move(
                    stopper,
                    maze_data.maze, maze_data.pacman.current_location)
                maze_data.inky.pixel_move(
                    stopper,
                    maze_data.maze,
                    inky_target)
                maze_data.pinky.pixel_move(
                    stopper,
                    maze_data.maze,
                    pinky_target)
                maze_data.clyde.pixel_move(
                    stopper,
                    maze_data.maze,
                    maze_data.pacman.current_location)
                maze_data.pacman.pixel_move(
                    CURRENT_DIRECTION, booster, maze_data.maze)
                if all(maze_data.pacgums.values()):
                    t = maze_data.next_level()
                    level_timer = maze_data.configs["level_max_timer"]
                    level_frame = 1
                    # Fresh ghosts start in scatter mode, so resync timers
                    scatter = True
                    scatter_duration = 0
                    chase_duration = 0
                    frightened = False
                    frightened_duration = 0
                    if t:
                        current_state = 'GAME_WON'
                draw_text(
                    screen,
                    f"Level {maze_data.current_level}",
                    TOP_LEFT[0], TOP_LEFT[1] - 35, fonts["game_info"])
                draw_text(
                    screen,
                    f"Score: {maze_data.pacman.total_points}",
                    TOP_RIGHT[0] - 190, TOP_RIGHT[1] - 35, fonts["game_info"])
                if level_frame % 60 == 0 and level_timer > 0:
                    level_timer -= 1
                if level_timer == 0:
                    current_state = "GAME_OVER"
                level_frame += 1
                draw_text(
                    screen,
                    f"Time: {level_timer}",
                    BOTTOM_LEFT[0], BOTTOM_LEFT[1] + 5, fonts["game_info"])
                draw_text(
                    screen,
                    f"Lives: {maze_data.pacman.lives if not inf else '∞'}",
                    BOTTOM_RIGHT[0] - 120,
                    BOTTOM_RIGHT[1], fonts['game_info'])

        elif current_state == "PAUSE":
            pause.draw_pausemenu()
        frames += 1
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
