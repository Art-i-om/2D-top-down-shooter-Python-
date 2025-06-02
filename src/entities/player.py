import pygame
from src.entities.entity import Entity


class Player(Entity):
    def __init__(self, x: int, y: int, size: int, player_speed: float,
                 screen_width: int, screen_height: int, world_width: int, world_height: int, color: tuple[int, int, int],
                 health: int, damage: int, damage_cooldown: float,
                 stamina: int, stamina_recovery_rate: float, stamina_consumption_rate: float):
        super().__init__(x, y, size, size, color)
        self.speed_multiplier = 1.0
        self.speed = player_speed
        self.default_speed = player_speed
        self.width = screen_width
        self.height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.max_health = health
        self.health = self.max_health
        self.max_stamina = stamina
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = stamina_recovery_rate
        self.stamina_consumption_rate = stamina_consumption_rate
        self.is_sprinting = False
        self.damage = damage
        self.last_hit_time = 0
        self.damage_cooldown = damage_cooldown
        self.boost_end_time = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
        self.is_sprinting = keys[pygame.K_LSHIFT] and self.stamina > 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y = 1

        movement = pygame.Vector2(move_x, move_y)
        if movement.length() != 0:
            movement = movement.normalize()

        self.speed_multiplier = 1.5 if self.is_sprinting else 1.0
        self.rect.x += movement.x * self.speed * self.speed_multiplier
        self.rect.y += movement.y * self.speed * self.speed_multiplier

        self.rect.x = max(0, min(self.world_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.world_height - self.rect.height, self.rect.y))

        if self.is_sprinting:
            self.stamina -= self.stamina_consumption_rate
            if self.stamina < 0:
                self.stamina = 0
        else:
            self.stamina += self.stamina_recovery_rate
            if self.stamina > self.max_stamina:
                self.stamina = self.max_stamina

    def take_damage(self, damage: int) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.damage_cooldown:
            self.health -= damage
            self.last_hit_time = current_time
            return True
        return False

    def is_dead(self) -> bool:
        return self.health <= 0

    def heal(self, health):
        self.health = min(self.health + health, self.max_health)

    def update_speed(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.boost_end_time:
            self.speed = self.default_speed
