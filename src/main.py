import random
from typing import List

import pygame
import sys
from entities import Player, CatchingEnemy, Enemy, Collectable, Bullet, HealthPack
import settings

pygame.init()

WIDTH, HEIGHT = settings.Screen.width, settings.Screen.height
FPS = settings.Screen.fps

PLAYER_SPEED = settings.Player.speed
CATCHING_ENEMY_SPEED = settings.CatchingEnemy.speed
BULLET_SPEED = settings.Bullet.speed
ENEMY_HEALTH = settings.Enemy.health
PLAYER_HEALTH = settings.Player.health
PLAYER_SIZE = settings.Player.size
ENEMY_SIZE = settings.Enemy.size
PLAYER_DAMAGE = settings.Player.damage
CATCHING_ENEMY_DAMAGE = settings.CatchingEnemy.damage
PLAYER_DAMAGE_COOLDOWN = settings.Player.damage_cooldown
POWER_UPS_SIZE = settings.Collectable.size
HEALTH_PACK_HEALTH = settings.HealthPack.health

BLACK = settings.Colors.black
WHITE = settings.Colors.white
GREEN = settings.Colors.green
BLUE = settings.Colors.blue
YELLOW = settings.Colors.yellow
RED = settings.Colors.red
PURPLE = settings.Colors.purple
CYAN = settings.Colors.cyan


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Movement with Collectables")
clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE,
                PLAYER_SPEED, WIDTH, HEIGHT, GREEN, PLAYER_HEALTH,
                PLAYER_DAMAGE,
                PLAYER_DAMAGE_COOLDOWN)

health_packs: List[Collectable] = [
    HealthPack(POWER_UPS_SIZE, WIDTH, HEIGHT, RED, HEALTH_PACK_HEALTH) for _ in range(3)]

bullets = []
catching_enemies: List[Enemy] = [
    CatchingEnemy(random.randint(0, WIDTH - ENEMY_SIZE),
                  random.randint(0, HEIGHT - ENEMY_SIZE),
                  ENEMY_SIZE, ENEMY_HEALTH, PURPLE, RED, CATCHING_ENEMY_SPEED - 1,
                  CATCHING_ENEMY_DAMAGE)
    for _ in range(2)
]
score = 0
enemies_killed = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction = pygame.Vector2(mouse_x - player.rect.centerx, mouse_y - player.rect.centery)
                bullet_x = player.rect.centerx - 5
                bullet_y = player.rect.centery - 5
                bullets.append(Bullet(bullet_x, bullet_y, direction, BULLET_SPEED, BLUE))

    player.handle_input()

    for bullet in bullets[:]:
        bullet.update()
        if (
            bullet.rect.x < 0 or bullet.rect.x > WIDTH or
            bullet.rect.y < 0 or bullet.rect.y > HEIGHT
        ):
            bullets.remove(bullet)

    for catching_enemy in catching_enemies:
        catching_enemy.update(player)

    all_collectables = health_packs
    for collectable in all_collectables[:]:
        if player.rect.colliderect(collectable.rect):
            if collectable in health_packs:
                health_packs.remove(collectable)
                player.heal(HEALTH_PACK_HEALTH)

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
                break

    for enemy in catching_enemies:
        if player.rect.colliderect(enemy.rect):
            if player.is_dead(enemy.damage):
                running = False

    screen.fill(BLACK)
    player.draw(screen)

    for health_pack in health_packs:
        health_pack.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in catching_enemies:
        enemy.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    enemies_killed_text = font.render(f"Enemies killed: {enemies_killed}", True, WHITE)
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(enemies_killed_text, (10, 40))
    screen.blit(health_text, (10, 70))

    pygame.display.flip()

pygame.quit()
sys.exit()
