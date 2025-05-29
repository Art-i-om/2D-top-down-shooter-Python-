import pygame


class Player:
    def __init__(self, x: int, y: int, size: int, player_speed: float,
                 screen_width: int, screen_height: int, color: tuple[int, int, int],
                 health: int, damage: int, damage_cooldown: float):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = player_speed
        self.default_speed = player_speed
        self.width = screen_width
        self.height = screen_height
        self.color = color
        self.health = health
        self.max_health = health
        self.damage = damage
        self.last_hit_time = 0
        self.damage_cooldown = damage_cooldown
        self.boost_end_time = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0
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
        self.rect.x += movement.x * self.speed
        self.rect.y += movement.y * self.speed

        self.rect.x = max(0, min(self.width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.height - self.rect.height, self.rect.y))

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

    def draw(self, surface, offset=(0, 0)):
        draw_rect = self.rect.move(offset)
        pygame.draw.rect(surface, self.color, draw_rect)
