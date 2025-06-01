import pygame
from src.entities.entity import Entity


class Bullet(Entity):
    def __init__(self, x: int, y: int, size: int, direction: pygame.Vector2,
                 bullet_speed: float, color: tuple[int, int, int]):
        super().__init__(x, y, size, size, color)
        self.direction = direction.normalize()
        self.bullet_speed = bullet_speed

    def update(self):
        self.rect.x += self.direction.x * self.bullet_speed
        self.rect.y += self.direction.y * self.bullet_speed
