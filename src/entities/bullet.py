import pygame


class Bullet:
    def __init__(self, x: int, y: int, direction: pygame.Vector2,
                 bullet_speed: float, color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.direction = direction.normalize()
        self.bullet_speed = bullet_speed
        self.color = color

    def update(self):
        self.rect.x += self.direction.x * self.bullet_speed
        self.rect.y += self.direction.y * self.bullet_speed

    def draw(self, surface, offset=(0, 0)):
        draw_rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.color, draw_rect)