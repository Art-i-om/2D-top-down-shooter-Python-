import pygame
import random
from src.entities import Entity


class Collectable(Entity):
    def __init__(self, size: int, world_width: int, world_height: int, color: tuple[int, int, int]):
        width = world_width
        height = world_height
        color = color
        x = random.randint(0, width - size)
        y = random.randint(0, height - size)
        super().__init__(x, y, size, size, color)
