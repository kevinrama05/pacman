import pygame


class TextInputBox:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            font: pygame.font.Font | None = None,
            max_length: int | None = None) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font if font is not None else pygame.font.Font(None, 32)
        self.max_length = max_length

        self.text_color = (255, 255, 255)
        self.box_color = (50, 50, 50)
        self.active_color = (100, 100, 255)
        self.inactive_color = (150, 150, 150)

        self.text = ""
        self.active = False

        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 500

        self.submitted_text: str | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.submitted_text = self.text
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            else:
                char = event.unicode
                if char and (char.isalnum() or char == " "):
                    if (self.max_length is None
                            or len(self.text) < self.max_length):
                        self.text += char

    def draw(self, screen: pygame.Surface) -> None:
        if self.active:
            border_color = self.active_color
        else:
            border_color = self.inactive_color
        pygame.draw.rect(screen, self.box_color, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        x = self.rect.x + 5
        y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (x, y))

        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width() + 2
            cursor_y = self.rect.y + 6
            pygame.draw.line(
                screen,
                self.text_color, (cursor_x, cursor_y),
                (cursor_x, cursor_y + self.rect.height - 12), 2)

    def get_submitted(self) -> str | None:
        result = self.submitted_text
        self.submitted_text = None
        return result
