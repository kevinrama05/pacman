import pygame
from back_end.config_parser import ConfigDict


class Constants:
    def __init__(self, json: ConfigDict) -> None:
        self.width = json['width']
        self.height = json['height']
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h), pygame.FULLSCREEN)
        self.screen_w, self.screen_h = info.current_w, info.current_h
        self.cell_size = max(
            2,
            min(
                self.screen_w * 3 // 4 // self.width,
                self.screen_h * 3 // 4 // self.height))
        if self.cell_size > 80:
            self.cell_size = 80
        self.start_x = (self.screen_w - self.width * self.cell_size) // 2
        self.start_y = (self.screen_h - self.height * self.cell_size) // 2
