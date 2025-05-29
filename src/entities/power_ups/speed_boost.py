import pygame

from src.entities import Collectable


class SpeedBoost(Collectable):
    def __init__(self, size: int, screen_width: int, screen_height: int, color: tuple[int, int, int],
                 extra_speed: int, boost_duration: float):
        super().__init__(size, screen_width, screen_height, color)
        self.extra_speed = extra_speed
        self.duration = boost_duration
