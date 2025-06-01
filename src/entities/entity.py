import pygame

class Entity:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surface, camera=None):
        if camera:
            draw_rect = camera.apply(self.rect)
        else:
            draw_rect = self.rect
        pygame.draw.rect(surface, self.color, draw_rect)
