import pygame

class Label:
    def __init__(self, text, x, y, font_size, color, font_name=None):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        self.font_name = font_name  # None uses default font
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def update_text(self, new_text):
        self.text = new_text

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, (self.x, self.y))
