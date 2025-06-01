import random
from typing import List, Union

import pygame
import sys
from entities import Player, CatchingEnemy, Enemy, Bullet, HealthPack, SpeedBoost
from core import Camera
import settings
from managers import SoundManager
from managers import MenuManager

pygame.init()

# Sounds
sound_manager = SoundManager()
sound_manager.set_volume(settings.Sounds.global_volume)

# Map
WORLD_WIDTH, WORLD_HEIGHT = settings.Screen.world_width, settings.Screen.world_height

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = settings.Screen.width, settings.Screen.height
FPS = settings.Screen.fps
SHAKE_DURATION = settings.Screen.shake_duration # given in frames
SHAKE_MAGNITUDE = settings.Screen.shake_magnitude

# Player
PLAYER_SPEED = settings.Player.speed
PLAYER_HEALTH = settings.Player.health
PLAYER_SIZE = settings.Player.size
PLAYER_DAMAGE = settings.Player.damage
PLAYER_DAMAGE_COOLDOWN = settings.Player.damage_cooldown

# Enemy
CATCHING_ENEMY_SPEED = settings.CatchingEnemy.speed
ENEMY_HEALTH = settings.Enemy.health
ENEMY_SIZE = settings.Enemy.size
CATCHING_ENEMY_DAMAGE = settings.CatchingEnemy.damage

# Bullet
BULLET_SPEED = settings.Bullet.speed
BULLET_SIZE = settings.Bullet.size

#Power ups
POWER_UPS_SIZE = settings.Collectable.size
HEALTH_PACK_HEALTH = settings.HealthPack.health
EXTRA_SPEED_BOOST = settings.SpeedBoost.new_speed
EXTRA_SPEED_DURATION = settings.SpeedBoost.duration

# Colors
colors = {
    "black": settings.Colors.black,
    "white": settings.Colors.white,
    "green": settings.Colors.green,
    "blue": settings.Colors.blue,
    "yellow": settings.Colors.yellow,
    "red": settings.Colors.red,
    "purple": settings.Colors.purple,
    "cyan": settings.Colors.cyan
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Movement with Collectables")
clock = pygame.time.Clock()

score = 0
enemies_killed = 0

font = pygame.font.SysFont(None, 36)

camera = Camera(WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
menu_manager = MenuManager(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, colors)

menu_manager.main_menu()

def play_game():
    global score
    global enemies_killed

    player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, PLAYER_SIZE,
                    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
                    colors['green'], PLAYER_HEALTH,
                    PLAYER_DAMAGE,
                    PLAYER_DAMAGE_COOLDOWN)

    health_packs: List[HealthPack] = [
        HealthPack(POWER_UPS_SIZE, WORLD_WIDTH, WORLD_HEIGHT, colors['red'], HEALTH_PACK_HEALTH)
        for _ in range(3)
    ]

    speed_boosts: List[SpeedBoost] = [
        SpeedBoost(POWER_UPS_SIZE, WORLD_WIDTH, WORLD_HEIGHT, colors['blue'], EXTRA_SPEED_BOOST, EXTRA_SPEED_DURATION)
        for _ in range(2)
    ]

    bullets = []
    catching_enemies: List[Enemy] = [
        CatchingEnemy(random.randint(0, SCREEN_WIDTH - ENEMY_SIZE),
                      random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE),
                      ENEMY_SIZE, ENEMY_HEALTH, colors['purple'], colors['red'], CATCHING_ENEMY_SPEED - 1,
                      CATCHING_ENEMY_DAMAGE)
        for _ in range(2)
    ]

    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        player.update_speed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    world_mouse_x = mouse_x + camera.camera_rect.left
                    world_mouse_y = mouse_y + camera.camera_rect.top
                    direction = pygame.Vector2(world_mouse_x - player.rect.centerx, world_mouse_y - player.rect.centery)
                    bullet_x = player.rect.centerx - 5
                    bullet_y = player.rect.centery - 5
                    bullets.append(Bullet(bullet_x, bullet_y, BULLET_SIZE, direction, BULLET_SPEED, colors['yellow']))
                    sound_manager.play_shoot()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_manager.pause_menu()

        player.handle_input()
        camera.update(player)

        for bullet in bullets[:]:
            bullet.update()
            if (
                    bullet.rect.x < 0 or bullet.rect.x > WORLD_WIDTH or
                    bullet.rect.y < 0 or bullet.rect.y > WORLD_HEIGHT
            ):
                bullets.remove(bullet)

        for catching_enemy in catching_enemies:
            catching_enemy.update(player)

        all_collectables: List[Union[HealthPack, SpeedBoost]] = health_packs + speed_boosts
        for collectable in all_collectables[:]:
            if player.rect.colliderect(collectable.rect):
                if collectable in health_packs:
                    health_packs.remove(collectable)
                    player.heal(HEALTH_PACK_HEALTH)
                elif collectable in speed_boosts:
                    speed_boosts.remove(collectable)
                    player.speed = EXTRA_SPEED_BOOST
                    player.boost_end_time = current_time + collectable.duration

        all_enemies = catching_enemies
        for bullet in bullets[:]:
            for enemy in all_enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    if enemy.is_dead(player.damage):
                        if enemy in catching_enemies:
                            catching_enemies.remove(enemy)
                        score += 5
                        enemies_killed += 1
                        sound_manager.play_explosion()
                    break

        for enemy in catching_enemies:
            if player.rect.colliderect(enemy.rect):
                if player.take_damage(enemy.damage):
                    camera.start_shake(SHAKE_DURATION, SHAKE_MAGNITUDE)
                if player.is_dead():
                    running = False

        screen.fill(colors['black'])
        player.draw(screen, camera=camera)

        all_entities = all_collectables + bullets + all_enemies
        for entity in all_entities:
            entity.draw(screen, camera=camera)

        score_text = font.render(f"Score: {score}", True, colors['white'])
        enemies_killed_text = font.render(f"Enemies killed: {enemies_killed}", True, colors['white'])
        health_text = font.render(f"Health: {player.health}", True, colors['white'])
        speed_text = font.render(f"Speed: {player.speed}", True, colors['white'])
        screen.blit(score_text, (10, 10))
        screen.blit(enemies_killed_text, (10, 40))
        screen.blit(health_text, (10, 70))
        screen.blit(speed_text, (10, 100))

        pygame.display.flip()


while True:
    play_game()
    menu_manager.game_over_menu(score)

# pygame.quit()
# sys.exit()
