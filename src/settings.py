from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    width: int = 1920
    height: int = 1080
    fps: int = 60
    shake_duration: int = 10 # given in frames
    shake_magnitude: int = 5

@dataclass(frozen=True)
class Player:
    health: int = 3
    size: int = 50
    damage: int = 1
    speed: int = 5
    damage_cooldown: float = 1000 # millis

@dataclass(frozen=True)
class Enemy:
    health: int = 3
    size: int = 50

@dataclass(frozen=True)
class Collectable:
    size: int = 30

@dataclass(frozen=True)
class HealthPack(Collectable):
    health: int = 1

@dataclass(frozen=True)
class SpeedBoost(Collectable):
    new_speed: int = 10
    duration: float = 3000

@dataclass(frozen=True)
class CatchingEnemy(Enemy):
    damage: int = 1
    speed: int = 5

@dataclass(frozen=True)
class Bullet:
    speed: int = 10

@dataclass(frozen=True)
class Colors:
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)
    green: tuple[int, int, int] = (0, 255, 0)
    blue: tuple[int, int, int] = (0, 0, 255)
    yellow: tuple[int, int, int] = (255, 255, 0)
    red: tuple[int, int, int] = (255, 0, 0)
    purple: tuple[int, int, int] = (255, 0, 255)
    cyan: tuple[int, int, int] = (0, 255, 255)