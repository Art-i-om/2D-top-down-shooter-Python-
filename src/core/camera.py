import pygame
import random


class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.world_width = world_width
        self.world_height = world_height
        self.shake_duration = 0
        self.shake_magnitude = 0
        self.shake_offset = pygame.Vector2(0, 0)

    def apply(self, target_rect):
        offset_x = self.camera_rect.left - self.shake_offset.x
        offset_y = self.camera_rect.top - self.shake_offset.y
        return target_rect.move(-offset_x, -offset_y)

    def update(self, target):
        x = target.rect.centerx - self.camera_rect.width // 2
        y = target.rect.centery - self.camera_rect.height // 2

        # Clamp to world boundaries
        x = max(0, min(x, self.world_width - self.camera_rect.width))
        y = max(0, min(y, self.world_height - self.camera_rect.height))

        self.camera_rect.topleft = (x, y)

        if self.shake_duration > 0:
            self.shake_duration -= 1
            self.shake_offset.x = random.randint(-self.shake_magnitude, self.shake_magnitude)
            self.shake_offset.y = random.randint(-self.shake_magnitude, self.shake_magnitude)
        else:
            self.shake_offset.x = 0
            self.shake_offset.y = 0

    def start_shake(self, duration, magnitude):
        self.shake_duration = duration
        self.shake_magnitude = magnitude
