import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()
# create a screen
screen = pygame.display.set_mode((800, 600))  # width and height of screen in pixels
# background image
background = pygame.image.load("galaxy.jpg")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # here -1 means its gonna play music on loop
# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)

# player
PlayerImg = pygame.image.load("space.png")
PlayerX = 370
PlayerY = 480
PlayerX_Change = 0
PlayerY_Change = 0
# enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_Change = []
EnemyY_Change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_Change.append(1)  # don't need to append with these cause these are constants
    EnemyY_Change.append(40)

# bullet
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletX_Change = 0
BulletY_Change = 3
bullet_state = "ready"  # ready state you can't see the bullet yet but at fire you can

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
# game over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True,
                        (128, 128, 128))  # true is for yes you can show text then rgb
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (0, 128, 128))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(PlayerImg, (x, y))  # blit = draw


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def iscollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt((math.pow(EnemyX - BulletX, 2)) + (math.pow(EnemyY - BulletY, 2)))
    if distance < 27:  # 27 came through trial and testing
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 128, 128))  # rgb = red green blue value goes from 0 to 255
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:  # keydown is pressing of button while keyup is releasing
            if event.key == pygame.K_LEFT:
                PlayerX_Change = -2
            if event.key == pygame.K_RIGHT:
                PlayerX_Change = +2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")  # sound cause its very short music is long
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    BulletX = PlayerX
                    fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                PlayerX_Change = 0

    # checking for boundaries so it doesn't go out of screen
    PlayerX += PlayerX_Change
    if PlayerX <= 0:
        PlayerX = 0
    elif PlayerX >= 736:
        PlayerX = 736
    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if EnemyY[i] > 400:
            for j in range(num_of_enemies):
                EnemyY[j] = 2000
            game_over_text()
            break

        EnemyX[i] += EnemyX_Change[i]
        if EnemyX[i] <= 0:
            EnemyX_Change[i] = 1
            EnemyY[i] += EnemyY_Change[i]
        elif EnemyX[i] >= 736:
            EnemyX_Change[i] = -1
            EnemyY[i] += EnemyY_Change[i]
        # collision
        collision = iscollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            BulletY = 480
            bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)
        enemy(EnemyX[i], EnemyY[i], i)  #?????
    # bullet movement
    if BulletY <= 0:
        BulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_Change
    show_score(textX, textY)
    player(PlayerX, PlayerY)
    pygame.display.update()  # always add this at the end
