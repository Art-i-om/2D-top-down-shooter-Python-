from typing import List, Union

import pygame
import sys
from entities import Player, Bullet, HealthPack, SpeedBoost
from core import Camera
from ui import Label, Bar
import settings
from managers import SoundManager, MenuManager, WaveManager

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
STAMINA = settings.Player.max_stamina
STAMINA_RECOVERY_RATE = settings.Player.stamina_recovery_rate
STAMINA_CONSUMPTION_RATE = settings.Player.stamina_consumption_rate

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

camera = Camera(WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)
menu_manager = MenuManager(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, colors)

menu_manager.main_menu()

# def spawn_wave(wave_number, screen_width, screen_height, enemy_size, enemy_health, catching_enemy_speed, catching_enemy_damage, colors):
#     new_enemies = []
#     for _ in range(enemies_per_wave + wave_number - 1):  # Increase enemies per wave
#         enemy = CatchingEnemy(
#             random.randint(0, screen_width - enemy_size),
#             random.randint(0, screen_height - enemy_size),
#             enemy_size, enemy_health, colors['purple'], colors['red'], catching_enemy_speed, catching_enemy_damage
#         )
#         new_enemies.append(enemy)
#     return new_enemies

def play_game():
    global score

    player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2, PLAYER_SIZE,
                    PLAYER_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, WORLD_WIDTH, WORLD_HEIGHT,
                    colors['green'], PLAYER_HEALTH,
                    PLAYER_DAMAGE,
                    PLAYER_DAMAGE_COOLDOWN,
                    STAMINA, STAMINA_RECOVERY_RATE, STAMINA_CONSUMPTION_RATE)

    health_packs: List[HealthPack] = [
        HealthPack(POWER_UPS_SIZE, WORLD_WIDTH, WORLD_HEIGHT, colors['red'], HEALTH_PACK_HEALTH)
        for _ in range(3)
    ]

    speed_boosts: List[SpeedBoost] = [
        SpeedBoost(POWER_UPS_SIZE, WORLD_WIDTH, WORLD_HEIGHT, colors['blue'], EXTRA_SPEED_BOOST, EXTRA_SPEED_DURATION)
        for _ in range(2)
    ]

    bullets = []

    wave_manager = WaveManager(
        SCREEN_WIDTH, SCREEN_HEIGHT,
        ENEMY_SIZE, ENEMY_HEALTH,
        CATCHING_ENEMY_SPEED, CATCHING_ENEMY_DAMAGE, colors
    )

    catching_enemies = wave_manager.spawn_wave()

    stamina_bar = Bar(10, SCREEN_HEIGHT - 70,
                             350, 40,
                             colors['white'], colors['cyan'])
    health_bar = Bar(10, SCREEN_HEIGHT - 120,
                     350, 40,
                     colors['white'], colors['red'])

    score_label = Label(f"Score: {score}", 10, 10, 36, colors['white'])
    speed_label = Label(f"Speed: {player.speed}", 10, 40, 36, colors['white'])
    wave_number_label = Label(f"Wave number: {wave_manager.wave_number}",
                              SCREEN_WIDTH - 230, 10, 40, colors['white'])

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
        speed_label.update_text(f"Speed: {player.speed * player.speed_multiplier}")
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
                        score_label.update_text(f"Score: {score}")
                        sound_manager.play_explosion()
                    break

        for enemy in catching_enemies:
            if player.rect.colliderect(enemy.rect):
                if player.take_damage(enemy.damage):
                    camera.start_shake(SHAKE_DURATION, SHAKE_MAGNITUDE)
                if player.is_dead():
                    running = False

        if not all_enemies:
            catching_enemies = wave_manager.next_wave()
            wave_number_label.update_text(f"Wave number: {wave_manager.wave_number}")

        screen.fill(colors['black'])
        player.draw(screen, camera=camera)

        all_entities = all_collectables + bullets + all_enemies
        for entity in all_entities:
            entity.draw(screen, camera=camera)

        score_label.draw(screen)
        speed_label.draw(screen)
        wave_number_label.draw(screen)

        stamina_bar.draw(screen, player.stamina, player.max_stamina)
        health_bar.draw(screen, player.health, player.max_health)

        pygame.display.flip()


while True:
    play_game()
    menu_manager.game_over_menu(score)
