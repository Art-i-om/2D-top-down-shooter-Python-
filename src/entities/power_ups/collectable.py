import pygame
import random


class Collectable:
    def __init__(self, size: int, screen_width: int, screen_height: int, color: tuple[int, int, int]):
        self.size = size
        self.width = screen_width
        self.height = screen_height
        self.color = color
        self.rect = pygame.Rect(
            random.randint(0, self.width - size),
            random.randint(0, self.height - size),
            size, size
        )

    def draw(self, surface, offset=(0, 0)):
        draw_rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.color, draw_rect)