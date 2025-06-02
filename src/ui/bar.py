import pygame

class Bar:
    def __init__(self, x, y, width, height, border_color, fill_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.border_color = border_color
        self.fill_color = fill_color

    def draw(self, surface, current_value, max_value):
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        fill_width = int(self.rect.width * (current_value / max_value))

        fill_rect = self.rect.copy()
        fill_rect.width = fill_width
        pygame.draw.rect(surface, self.fill_color, fill_rect)
