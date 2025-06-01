import pygame

from src.entities.player import Player
from src.entities.entity import Entity


class Enemy(Entity):
    def __init__(self, x: int, y: int, size: int,
                 max_health: int, color: tuple[int, int, int], bar_color: tuple[int, int, int],
                 damage: int):
        super().__init__(x, y, size, size, color)
        self.max_health = max_health
        self.health = max_health
        self.bar_color = bar_color
        self.damage = damage

    def update(self, player: Player):
        pass

    def is_dead(self, damage: int) -> bool:
        self.health -= damage
        if self.health <= 0:
            return True

        return False

    def draw(self, surface, camera=None):
        super().draw(surface, camera)

        if camera:
            draw_rect = camera.apply(self.rect)
        else:
            draw_rect = self.rect

        health_bar_width = int(draw_rect.width * (self.health / self.max_health))
        health_bar_height = 5
        health_bar_rect = pygame.Rect(
            draw_rect.x,
            draw_rect.y - health_bar_height - 5,
            health_bar_width,
            health_bar_height
        )
        pygame.draw.rect(surface, self.bar_color, health_bar_rect)
