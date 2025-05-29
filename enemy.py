import pygame
from player import Player


class Enemy:
    def __init__(self, x: int, y: int, size: float,
                 max_health: int, color: tuple[int, int, int], bar_color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, size, size)
        self.max_health = max_health
        self.health = max_health
        self.color = color
        self.bar_color = bar_color

    def update(self, player: Player):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        health_ratio = self.health / self.max_health
        health_bar_width = int(self.rect.width * health_ratio)
        pygame.draw.rect(surface, self.bar_color, (self.rect.x, self.rect.y - 10, health_bar_width, 5))
