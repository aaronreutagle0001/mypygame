# C ontrols and Instructions
# spacebar to shoot or fire
# right arrow to go right 
# left arrow to go left
# when you hit the enemey the game proceeds to lvl 2 and you have 2 enemies the game is continuing when you are winning
# when the enemy hits you the game is over

import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame: Enemies Firing and Game Ends on Player Hit")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

rect_size = 50
rect_x, rect_y = width // 2 - rect_size // 2, height - rect_size - 10
rect_speed = 5

bullet_width, bullet_height = 5, 10
bullet_speed = 7
bullets = []

level = 1
enemy_size = 50
enemy_speed = 3
enemy_bullets = []

def create_enemies(num):
    return [[random.randint(0, width - enemy_size),
             random.randint(0, height // 2 - enemy_size),
             random.choice([-enemy_speed, enemy_speed]),
             random.choice([-enemy_speed, enemy_speed])] for _ in range(num)]

enemies = create_enemies(level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append([rect_x + rect_size // 2 - bullet_width // 2, rect_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: rect_x -= rect_speed
    if keys[pygame.K_RIGHT]: rect_x += rect_speed
    if keys[pygame.K_UP]: rect_y -= rect_speed
    if keys[pygame.K_DOWN]: rect_y += rect_speed

    bullets = [[bx, by - bullet_speed] for bx, by in bullets if by > 0]

    for enemy in enemies:
        enemy[0] += enemy[2]
        enemy[1] += enemy[3]
        if enemy[0] <= 0 or enemy[0] >= width - enemy_size:
            enemy[2] = -enemy[2]
        if enemy[1] <= 0 or enemy[1] >= height - enemy_size:
            enemy[3] = -enemy[3]
        if random.randint(0, 100) < 2:
            enemy_bullets.append([enemy[0] + enemy_size // 2 - bullet_width // 2, enemy[1] + enemy_size])

    enemy_bullets = [[bx, by + bullet_speed] for bx, by in enemy_bullets if by < height]

    for enemy in enemies[:]:
        if any(pygame.Rect(bx, by, bullet_width, bullet_height).colliderect(pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)) for bx, by in bullets):
            enemies.remove(enemy)
            bullets = [b for b in bullets if not pygame.Rect(b[0], b[1], bullet_width, bullet_height).colliderect(pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size))]

    if not enemies:
        level += 1
        enemies = create_enemies(level)
        print(f"Level {level} starts with {len(enemies)} enemies!")

    player_rect = pygame.Rect(rect_x, rect_y, rect_size, rect_size)
    if any(pygame.Rect(bx, by, bullet_width, bullet_height).colliderect(player_rect) for bx, by in enemy_bullets):
        print("Player hit! Game Over!")
        pygame.quit()
        sys.exit()

    screen.fill(black)
    pygame.draw.rect(screen, green, player_rect)
    for enemy in enemies:
        pygame.draw.rect(screen, red, pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size))
    for bullet in bullets:
        pygame.draw.rect(screen, white, pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height))
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, red, pygame.Rect(enemy_bullet[0], enemy_bullet[1], bullet_width, bullet_height))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
