import random


class ScreenShake:
    def __init__(self, magnitude, duration):
        self.magnitude = magnitude
        self.duration = duration
        self.shake_timer = 0

    def start(self, duration=None):
        self.shake_timer = duration if duration is not None else self.duration

    def get_offset(self) -> tuple:
        if self.shake_timer > 0:
            self.shake_timer -= 1
            offset_x = random.randint(-self.magnitude, self.magnitude)
            offset_y = random.randint(-self.magnitude, self.magnitude)
            return offset_x, offset_y
        return 0, 0
