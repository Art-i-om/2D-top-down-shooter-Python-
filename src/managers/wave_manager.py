import random
from src.entities.enemies.catching_enemy import CatchingEnemy

class WaveManager:
    def __init__(self, screen_width, screen_height, enemy_size, enemy_health, enemy_speed, enemy_damage, colors):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemy_size = enemy_size
        self.enemy_health = enemy_health
        self.enemy_speed = enemy_speed
        self.enemy_damage = enemy_damage
        self.colors = colors
        self.wave_number = 1

    def spawn_wave(self):
        num_enemies = 3 + self.wave_number - 1  # Increase enemy count with wave number
        new_enemies = []
        for _ in range(num_enemies):
            enemy = CatchingEnemy(
                random.randint(0, self.screen_width - self.enemy_size),
                random.randint(0, self.screen_height - self.enemy_size),
                self.enemy_size, self.enemy_health,
                self.colors['purple'], self.colors['red'],
                self.enemy_speed, self.enemy_damage
            )
            new_enemies.append(enemy)
        return new_enemies

    def next_wave(self):
        self.wave_number += 1
        return self.spawn_wave()
