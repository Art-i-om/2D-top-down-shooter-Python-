import pygame

from enemy import Enemy
from player import Player


class CatchingEnemy(Enemy):
    def __init__(self, x, y, size, max_health, color, bar_color, speed):
        super().__init__(x, y, size, max_health, color, bar_color)
        self.speed = speed

    def update(self, player: Player):
        direction = pygame.Vector2(player.rect.centerx - self.rect.centerx,
                                   player.rect.centery - self.rect.centery)
        if direction.length() != 0:
            direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed
