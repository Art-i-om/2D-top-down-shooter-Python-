import random

import pygame
import sys
from player import Player
from collectable import Collectable
from bullet import Bullet
from enemy import Enemy
from catching_enemy import CatchingEnemy

pygame.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
DEFAULT_UNIT_SPEED = 5
BULLET_SPEED = 10
ENEMY_HEALTH = 3
DEFAULT_UNIT_SIZE = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Movement with Collectables")
clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2, DEFAULT_UNIT_SIZE, DEFAULT_UNIT_SPEED, WIDTH, HEIGHT, GREEN)
collectables = [Collectable(30, WIDTH, HEIGHT, YELLOW) for _ in range(5)]
bullets = []
enemies = [
    Enemy(random.randint(0, WIDTH - DEFAULT_UNIT_SIZE),
          random.randint(0, HEIGHT - DEFAULT_UNIT_SIZE),
          DEFAULT_UNIT_SIZE, ENEMY_HEALTH, PURPLE, RED)
    for _ in range(0)]
catching_enemies = [
    CatchingEnemy(random.randint(0, WIDTH - DEFAULT_UNIT_SIZE),
                  random.randint(0, HEIGHT - DEFAULT_UNIT_SIZE),
                  DEFAULT_UNIT_SIZE, ENEMY_HEALTH, PURPLE, RED, DEFAULT_UNIT_SPEED - 1)
    for _ in range(2)
]
score = 0
enemies_killed = 0
font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(FPS)
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

    for enemy in enemies:
        enemy.update(player)
    for catching_enemy in catching_enemies:
        catching_enemy.update(player)

    for collectable in collectables[:]:
        if player.rect.colliderect(collectable.rect):
            collectables.remove(collectable)
            score += 1
            collectables.append(Collectable(30, WIDTH, HEIGHT, YELLOW))

    all_enemies = enemies + catching_enemies
    for bullet in bullets[:]:
        for enemy in all_enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                enemy.health -= 1
                bullets.remove(bullet)
                if enemy.health <= 0:
                    if enemy in enemies:
                        enemies.remove(enemy)
                    elif enemy in catching_enemies:
                        catching_enemies.remove(enemy)
                    score += 5
                    enemies_killed += 1
                break

    for enemy in catching_enemies:
        if player.rect.colliderect(enemy.rect):
            print("You were caught by an enemy")
            running = False

    screen.fill(BLACK)
    player.draw(screen)
    for collectable in collectables:
        collectable.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies + catching_enemies:
        enemy.draw(screen)

    score_text = font.render(f"Score: {score}", True, WHITE)
    enemies_killed_text = font.render(f"Enemies killed: {enemies_killed}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(enemies_killed_text, (10, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
