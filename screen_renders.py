import pygame


class MainMenu:
    def __init__(self, screen, fonts, highscores):
        self.screen = screen
        self.fonts = fonts
        self.highscores = highscores
        self.bg_color = (0, 0, 0)

    def draw_start_screen(self) -> None:
        self.screen.fill(self.bg_color)
        screen_w, screen_h = self.screen.get_size()

        # Access fonts from the dictionary
        title_surface = self.fonts["title"].render(
            "Pac-man", True, (255, 255, 0)
        )
        title_rect = title_surface.get_rect(
            center=(screen_w // 2, screen_h // 2 - 180)
        )
        self.screen.blit(title_surface, title_rect)

        hint_surface = self.fonts["hint"].render(
            "Press SPACE to play or I for instructions",
            True,
            (255, 255, 255)
        )
        hint_rect = hint_surface.get_rect(
            center=(screen_w // 2, screen_h // 2 + 40)
        )
        self.screen.blit(hint_surface, hint_rect)

        start_y = screen_h // 2 + 150
        line_height = 50
        header_surface = self.fonts["menu"].render(
            "Top 10 players:",
            True,
            (255, 255, 255)
        )
        header_rect = header_surface.get_rect(
            center=(screen_w // 2, start_y)
        )
        self.screen.blit(header_surface, header_rect)

        # for i, player_data in enumerate(self.highscores[:10]):
        #     name = player_data["name"]
        #     score = player_data["score"]

        #     score_text = f"{i+1}. {name} - {score}"
        #     score_surface = self.fonts["menu"].render(
        #         score_text,
        #         True,
        #         (200, 200, 200)
        #     )

        #     score_rect = score_surface.get_rect(
        #         center=(screen_w // 2, start_y + 50 + (i * line_height))
        #     )
        #     self.screen.blit(score_surface, score_rect)

    def instructions(self) -> None:
        self.screen.fill(self.bg_color)
        screen_w, screen_h = self.screen.get_size()


        title_surface = self.fonts["title"].render("Instructions:", True, (0, 0, 255))
        title_rect = title_surface.get_rect(center=(screen_w // 2, 100))
        self.screen.blit(title_surface, title_rect)

        content = [
            ("Control:", "'wasd' to move"),
            ("Rules:", "You have 3 lives"),
            ("Rules:", "3 minutes to finish the level")
        ]

        y_offset = 200
        for header, text in content:
            header_surf = self.fonts["menu"].render(
                header,
                True,
                (255, 255, 0)
            )
            self.screen.blit(header_surf, (screen_w // 4, y_offset))
            
            # Render the details
            text_surf = self.fonts["hint"].render(
                text,
                True,
                (255, 255, 255)
            )
            self.screen.blit(text_surf, (screen_w // 4 + 150, y_offset + 5))
            
            y_offset += 60

    def draw(self, state):
        if state == "MENU":
            self.draw_start_screen()
        elif state == "INSTRUCTIONS":
            self.instructions()


class PlayingScreen:
    def __init__(
        self,
        screen,
        cell_size: int,
        wall_color: tuple = (0, 255, 255),
        bg_color: tuple = (0, 0, 0),
        isolated_color: tuple = (255, 255, 255)
    ):
        """Initializing for render engine"""
        self.cell_size = cell_size
        self.wall_color = wall_color
        self.bg_color = bg_color
        self.isolated_color = isolated_color
        self.text_color = (255, 255, 0)
        self.screen = screen

    def calculate_offsets(self, maze: list[list[int]]) -> None:
        rows = len(maze)
        cols = len(maze[0])
        total_w = cols * self.cell_size
        total_h = rows * self.cell_size
        
        self.offset_x = (self.screen.get_width() - total_w) // 2
        self.offset_y = (self.screen.get_height() - total_h) // 2

    def draw_maze(self, maze: list[list[int]], pacgums_eaten: dict[tuple[int, int], bool]) -> None:
        """Clears the screen and draws the maze walls"""
        if not self.screen:
            raise RuntimeError("No screen found. Set up window first!")
        self.calculate_offsets(maze)
        self.screen.fill(self.bg_color)

        rows = len(maze)
        cols = len(maze[0]) if rows > 0 else 0

        total_maze_w = cols * self.cell_size
        total_maze_h = rows * self.cell_size

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        offset_x = (screen_w - total_maze_w) // 2
        offset_y = (screen_h - total_maze_h) // 2

        for r in range(rows):
            for c in range(cols):
                cell_value = maze[r][c]

                # Calculate pixel positions
                x = offset_x + (c * self.cell_size)
                y = offset_y + (r * self.cell_size)

                # check if its isolated block
                if cell_value == 15:
                    pygame.draw.rect(
                        self.screen,
                        self.isolated_color,
                        (x, y, self.cell_size, self.cell_size)
                    )

                # 2 Otherwise draw standard
                else:
                    if cell_value & 1:
                        pygame.draw.line(
                            self.screen,
                            self.wall_color,
                            (x, y),
                            (x + self.cell_size, y),
                            2
                        )
                    if cell_value & 2:
                        pygame.draw.line(
                            self.screen,
                            self.wall_color,
                            (x + self.cell_size, y),
                            (x + self.cell_size, y + self.cell_size),
                            2
                        )
                    if cell_value & 4:
                        pygame.draw.line(
                            self.screen,
                            self.wall_color,
                            (x, y + self.cell_size),
                            (x + self.cell_size, y + self.cell_size),
                            2
                        )
                    if cell_value & 8:
                        pygame.draw.line(
                            self.screen,
                            self.wall_color,
                            (x, y),
                            (x, y + self.cell_size),
                            2
                        )
        
        width = len(maze[0])
        height = len(maze)
        for key, value in pacgums_eaten.items():
            if not value:
                x, y = key
                if key in ((0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)):
                    pygame.draw.circle(self.screen, (255, 255, 0), (offset_x + x * self.cell_size + self.cell_size / 2, offset_y + y * self.cell_size + self.cell_size / 2), 8)
                else:
                    pygame.draw.circle(self.screen, (255, 255, 0), (offset_x + x * self.cell_size + self.cell_size / 2, offset_y + y * self.cell_size + self.cell_size / 2), 4)

class PauseMenu:
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        self.selected_index = 0
        self.options = ["RESUME", "RETURN"]
        self.bg_color = (0, 0, 0)

    def draw_pausemenu(self) -> None:
        self.screen.fill(self.bg_color)
        screen_w = self.screen.get_width()

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.fonts["menu"].render(option, True, color)
            
            y_pos = 200 + (i * 100)
            rect = text.get_rect(center=(screen_w // 2, y_pos))
            self.screen.blit(text, rect)

            if i == self.selected_index:
                selector = self.fonts["menu"].render(">", True, (255, 255, 0))
                self.screen.blit(selector, (rect.left - 40, rect.y))


class Victory:
    pass


class GameOver:
    pass
