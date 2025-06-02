from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    width: int = 1920
    height: int = 1080
    world_width: int = 3000
    world_height: int = 3000
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
    max_stamina: int = 100
    stamina_recovery_rate: float = 0.5
    stamina_consumption_rate: float = 0.75

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
    speed: int = 20
    size: int = 10

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

@dataclass(frozen=True)
class Sounds:
    global_volume: float = 0.5

@dataclass(frozen=True)
class StaminaBar:
    width: int = 350
    height: int = 40
