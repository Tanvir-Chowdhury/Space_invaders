import pygame
import random
import math
from pygame import mixer

# Initialize
pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load(r"background.png")

# background sound
mixer.music.load(r'background.wav')
mixer.music.play(-1)

# title
pygame.display.set_caption("Space Invaders")

# icon
icon = pygame.image.load(r"ufo.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load(r'battleship.png')
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemy = 7

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load(r'enemy.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(6)
    enemyy_change.append(40)

# bullet
bulletImg = pygame.image.load(r'bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 10
bullet_state = 'ready'

# score
score = 0
scorex = 10
scorey = 10
font = pygame.font.Font('freesansbold.ttf', 32)

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score_show = font.render('Score : ' + str(score), True, (255, 255, 255))
    screen.blit(score_show, (x, y))


def game_over_text():
    over_show = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_show, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # changing background colors
    screen.fill((0, 255, 255))
    # changing background picture
    screen.blit(background, (0, 0))

    # capturing the  key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound(r'laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerx_change = 0

    playerx += playerx_change

    # player movement
    if playerx <= 1:
        playerx = 1
    elif playerx >= 735:
        playerx = 735

    # enemy movement
    for i in range(num_of_enemy):

        # game over
        if enemyy[i] > 420:
            for j in range(num_of_enemy):
                enemyy[j] = 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 1:
            enemyx_change[i] = 6
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 735:
            enemyx_change[i] = -6
            enemyy[i] += enemyy_change[i]

        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            collision_sound = mixer.Sound(r'explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score += 5
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(scorex, scorey)
    pygame.display.update()
