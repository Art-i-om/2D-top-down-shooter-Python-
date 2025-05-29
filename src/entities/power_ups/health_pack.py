import pygame

from src.entities import Collectable


class HealthPack(Collectable):
    def __init__(self, size: int, screen_width: int, screen_height: int, color: tuple[int, int, int],
                 health: int):
        super().__init__(size, screen_width, screen_height, color)
        self.health = health
