import pygame

from src.entities.player import Player


class Enemy:
    def __init__(self, x: int, y: int, size: float,
                 max_health: int, color: tuple[int, int, int], bar_color: tuple[int, int, int],
                 damage: int):
        self.rect = pygame.Rect(x, y, size, size)
        self.max_health = max_health
        self.health = max_health
        self.color = color
        self.bar_color = bar_color
        self.damage = damage

    def update(self, player: Player):
        pass

    def is_dead(self, damage: int) -> bool:
        self.health -= damage
        if self.health <= 0:
            return True

        return False

    def draw(self, surface, offset=(0, 0)):
        draw_rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.color, draw_rect)
        health_ratio = self.health / self.max_health
        health_bar_width = int(self.rect.width * health_ratio)
        health_bar_rect = pygame.Rect(
            self.rect.x + offset[0],
            self.rect.y - 10 + offset[1],
            health_bar_width,
            5
        )
        pygame.draw.rect(surface, self.bar_color, health_bar_rect)
