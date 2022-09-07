#!/usr/bin/env python
import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (180, 180, 255)
BACKGROUNDSPEED = 1
FPS = 50
BADDIEMINSIZE = 100
BADDIEMAXSIZE = 300
BADDIEMINSPEED = 3
BADDIEMAXSPEED = 5
ADDNEWBADDIERATE = 30

BULLETSIZE = 4
BULLETSPEED = 8
SHOOTDELAY = 7


CLOUDMINSIZE = 85
CLOUDMAXSIZE = 125
CLOUDMINSPEED = 2
CLOUDMAXSPEED = 4

PLAYERMOVERATE = 4
ANIMATIONSPEED = 4
EXPLOSIVEANIMATIONSPEED = 2
SPRITESCALE = 3

animation_dict = {-3: '_l3', -2: '_l2', -1: '_l1', 0: '', 1: '_r1', 2: '_r2', 3: '_r3'}


def add_land(lands, prepare=False):
    if prepare:
        land_x, land_y = 0, 0
    else:
        land_x, land_y = lands[-1]['rect'].topleft
        land_y -= landImage.get_height()
    new_land = {'rect': pygame.Rect(land_x, land_y, landImage.get_width(), landImage.get_height()),
                'speed': BACKGROUNDSPEED,
                'surface': landImage
                }
    lands.append(new_land)

def add_clouds(clouds, prepare=False):
    cloudImage = random.choice(cloudImages)
    cloudSize = random.randint(CLOUDMINSIZE, CLOUDMAXSIZE) / 100
    cloudWidth = int(cloudImage.get_width() * cloudSize)
    cloudHeight = int(cloudImage.get_height() * cloudSize)
    if prepare:
        cloud_y = WINDOWHEIGHT
    else:
        cloud_y = 0 - cloudHeight
    newCloud = {'rect': pygame.Rect(random.randint(0 - cloudWidth, WINDOWWIDTH), cloud_y,
                                    cloudWidth, cloudHeight),
                'speed': random.randint(CLOUDMINSPEED, CLOUDMAXSPEED),
                'surface': pygame.transform.scale(cloudImage, (cloudWidth, cloudHeight)),
                }

    clouds.append(newCloud)

def add_bullet(bullets):
    newBullet = {'rect': pygame.Rect(*shotsRect.center, BULLETSIZE, BULLETSIZE),
                 'speed': BULLETSPEED,
                 'surface': bulletImage
                 }
    bullets.append(newBullet)

def add_ammo(ammo):
    newAmmo = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - ammoImage.get_width()), 0 - ammoImage.get_height(),
                                     *ammoImage.get_size()),
               'speed': BADDIEMAXSPEED,
               'surface': pygame.transform.scale(ammoImage, [int(x / 2) for x in ammoImage.get_size()])
               }
    ammo.append(newAmmo)

def add_baddie(baddies):
    baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE) / 100
    baddieWidth = int(baddieImage.get_width() * baddieSize)
    baddieHeight = int(baddieImage.get_height() * baddieSize)
    newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieWidth), 0 - baddieHeight,
                                     baddieWidth, baddieHeight),
                 'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                 'surface': pygame.transform.scale(baddieImage, (baddieWidth, baddieHeight)),
                 'size': baddieSize, 'hp': baddieSize
                 }

    baddies.append(newBaddie)

def add_explosion(b):
    e_size = round(b['size'] / 2, 2)
    explWidth = int(explImages[0].get_width() * e_size)
    explHeight = int(explImages[0].get_height() * e_size)
    newExplosion = {'rect': pygame.Rect(0, 0, explWidth, explHeight),
                    'surface': pygame.transform.scale(explImages[0], (explWidth, explHeight)),
                    'frame': 0, 'timer': EXPLOSIVEANIMATIONSPEED, 'size': e_size
                    }
    newExplosion['rect'].center = b['rect'].center
    explosions.append(newExplosion)

def explosion_next_frame(e):
    explWidth = int(explImages[e['frame']].get_width() * e['size'])
    explHeight = int(explImages[e['frame']].get_height() * e['size'])
    e['surface'] = pygame.transform.scale(explImages[e['frame']], (explWidth, explHeight))

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Нажатие ESC осуществляет выход.
                    terminate()
                return

def playerHasHitObject(playerRect, objects: list):
    for o in objects:
        if playerRect.colliderect(o['rect']):
            return True
    return False

def bulletHasHitBaddie(baddies, bullet):
    for b in baddies[:]:
        if bullet['rect'].colliderect(b['rect']):
            b['hp'] -= 1.5
            if b['hp'] <= 0:
                add_explosion(b)
                baddies.remove(b)
            else:
                add_explosion({'rect': bullet['rect'], 'size': 0.5})
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def get_player_sprite(frame: int):
    playerImage = pygame.transform.scale(playerImages[frame],
                                         (int(playerImages[frame].get_width()/SPRITESCALE),
                                          int(playerImages[frame].get_height()/SPRITESCALE)))
    return playerImage

def get_shoot_sprite(frame):
    return shotsImages[frame]

def change_player_sprite(state, state_change):
    if state_change == 0:
        if state[0] < 0:
            state_change = 1
        elif state[0] > 0:
            state_change = -1

    state = [state[0] + state_change, ANIMATIONSPEED]
    return get_player_sprite(state[0]), state



# Настройка pygame, окна и указателя мыши.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Полет Оружейного Барона')
pygame.mouse.set_visible(False)

# Настройка шрифтов.
font = pygame.font.SysFont(None, 35)

# Настройка звуков.
gameOverSound = pygame.mixer.Sound('sounds/effects/gameover.mp3')
explosionSound = pygame.mixer.Sound('sounds/effects/explosion1.mp3')
explbigSound = pygame.mixer.Sound('sounds/effects/big_expl0.mp3')
shootSound = pygame.mixer.Sound('sounds/effects/shoot0.mp3')
getAmmoSound = pygame.mixer.Sound('sounds/effects/get_bonus0.mp3')
engineSound = pygame.mixer.Sound('sounds/effects/engine.mp3')
pygame.mixer.music.load('sounds/music/Flight of the Valkyries (Wrestling Theme) (8 Bit Version) (128 kbps).mp3')

# Настройка изображений.
playerImages = {key: pygame.image.load(f'sprites/plane/plane{value}.png') for key, value in animation_dict.items()}
playerImage = get_player_sprite(0)
playerRect = playerImage.get_rect()

shotsImages = [pygame.image.load(f'sprites/shots/shot{i}.png') for i in range(6)]
shotsImage = get_shoot_sprite(0)
shotsRect = pygame.Rect(shotsImage.get_rect())

landImage = pygame.image.load('sprites/land/land2.png')
bulletImage = pygame.image.load('sprites/bullsets/bullet0.png')
baddieImage = pygame.image.load('sprites/enemies/bomb0.png')
baddieImage = pygame.transform.scale(baddieImage, (15, 31))
cloudImages = [pygame.image.load(f'sprites/clouds/cloud{i}.png') for i in range(1)]
explImages = [pygame.image.load(f'sprites/explosions/eb{i}.png') for i in range(8)]
ammoImage = pygame.image.load('sprites/bonuses/ammo0.png')


# Вывод начального экрана.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Полет Оружейного Барона', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Нажмите клавишу для начала игры', font, windowSurface, (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    # Настройка начала игры.
    baddies = []
    bullets = []
    clouds_f = []
    clouds_b = []
    lands = []
    explosions = []
    ammo = []

    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    shoot = False
    gamover = False
    shoot_delay = 0
    shootFrame = 0
    shoot_frame_delay = 0
    player_ammo = 100
    pause = False
    baddieAddCounter = 0
    sprite_state_x = [0, 0]
    sprite_state_y = [0, 0]

    playerImage = get_player_sprite(0)
    shotsImage = get_shoot_sprite(0)

    engineSound.set_volume(0.1)
    engineSound.play(-1)
    pygame.mixer.music.play(-1, 0.0)


    add_clouds(clouds_b, prepare=True)
    add_land(lands, prepare=True)
    add_land(lands)

    while True: # Игровой цикл выполняется, пока игра работает.
        score += 1 # Увеличение количества очков.

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_p:
                    pause = True
                if event.key == K_SPACE:
                    shoot = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_SPACE:
                    shoot = False
                    getAmmoSound.stop()
                if event.key == K_ESCAPE:
                        terminate()


                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            # if event.type == MOUSEMOTION:
            #     # Если мышь движется, переместить игрока к указателю мыши.
            #     playerRect.centerx = event.pos[0]
            #     playerRect.centery = event.pos[1]
        if pause:
            waitForPlayerToPressKey()
            pause = False

        # Выстрелы пулемета
        if shoot_delay > 0: shoot_delay -= 1
        if shoot and shoot_delay == 0 and player_ammo:
            if not shootFrame: shootFrame = 1
            shoot_delay = SHOOTDELAY
            add_bullet(bullets)
            player_ammo -= 1
            shootSound.play()
        # Ящик с патронами
        if random.random() > 0.999 and not ammo:
            add_ammo(ammo)
        # Добавление облаков
        if random.random() > 0.996 and len(clouds_b + clouds_f) < 5:
            clouds = random.choice([clouds_b, clouds_f])
            add_clouds(clouds)
        # Если необходимо, добавить новых злодеев в верхнюю часть экрана.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            add_baddie(baddies)

        # Смена кадра\удаление взрывов
        for expl in explosions:
            if expl['timer'] == 0:
                expl['timer'] = EXPLOSIVEANIMATIONSPEED
                expl['frame'] += 1
                if expl['frame'] == 8:
                    explosions.remove(expl)
                else:
                    explosion_next_frame(expl)
            else:
                expl['timer'] -= 1

        # Проверка попаданий пуль в злодеев
        for b in bullets[:]:
            hit = bulletHasHitBaddie(baddies, b)
            if hit:
                explosionSound.play()
                bullets.remove(b)


        # Анимация спрайта
        if moveLeft and sprite_state_x[0] != -3:
            if sprite_state_x[1] == 0:
                playerImage, sprite_state_x = change_player_sprite(sprite_state_x, -1)
                playerRect.width = playerImage.get_width()
            else:
                sprite_state_x[1] -= 1
        if moveRight and sprite_state_x[0] != 3:
            if sprite_state_x[1] == 0:
                playerImage, sprite_state_x = change_player_sprite(sprite_state_x, 1)
                playerRect.width = playerImage.get_width()
            else:
                sprite_state_x[1] -= 1
        if not moveLeft and not moveRight and sprite_state_x[0] != 0:
            if sprite_state_x[1] == 0:
                playerImage, sprite_state_x = change_player_sprite(sprite_state_x, 0)
                playerRect.width = playerImage.get_width()
            else:
                sprite_state_x[1] -= 1

        # Перемещение игрока по экрану.
        if sprite_state_x[0] < 0 and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if sprite_state_x[0] > 0 and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Перемещение анимации выстрела
        shotsRect.center = playerRect.midtop

        # Перемещение взрыва самолета
        if gamover:
            playerExpl['rect'].center = playerRect.center

        # Анимация выстрела
        if shoot_frame_delay: shoot_frame_delay -= 1
        if shootFrame != 0:
            shoot_frame_delay = SHOOTDELAY*3
            shootFrame += 1
            if shootFrame == len(shotsImages):
                shootFrame = 0
            shotsImage = get_shoot_sprite(shootFrame)
        # Перемещение земли вниз
        for land in lands:
            land['rect'].move_ip(0, land['speed'])

        # Перемещение злодеев вниз.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Перемещение пуль
        for b in bullets:
            b['rect'].move_ip(0, -b['speed'])

        # Перемещение облаков
        for c in clouds_b + clouds_f:
            c['rect'].move_ip(0, c['speed'])

        # Перемещение амуниции
        for a in ammo:
            a['rect'].move_ip(0, a['speed'])

        # Удаление земли, ушедшей за экран
        if lands[0]['rect'].top > WINDOWHEIGHT:
            del lands[0]
            add_land(lands)

        # Удаление злодеев, упавших за нижнюю границу экрана.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Удаление пуль, улетевших за экран
        for b in bullets[:]:
            if b['rect'].bottom < 0:
                bullets.remove(b)

        # Удаление облаков, улетевших за экран
        for clouds in [clouds_b, clouds_f]:
            for c in clouds[:]:
                if c['rect'].top > WINDOWHEIGHT:
                    clouds.remove(c)

        # Перемещение амуниции
        for a in ammo[:]:
            if a['rect'].top > WINDOWHEIGHT:
                ammo.remove(a)

        # Отображение в окне игрового мира.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Отрисовка земли:
        for land in lands:
            windowSurface.blit(land['surface'], land['rect'])

        # Отображение количества очков и лучшего результата.
        drawText('Счет: %s' % (score), font, windowSurface, 10, 10)
        drawText('Рекорд: %s' % (topScore), font, windowSurface, 10, 50)
        drawText('AMMO %s' % (player_ammo), font, windowSurface, 450, 10)

        # Отрисовка облаков заднего плана
        for c in clouds_b:
            windowSurface.blit(c['surface'], c['rect'])

        # Отображение каждого злодея.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        # Отрисовка пуль
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])

        # Отображение анимации выстрела
        windowSurface.blit(shotsImage, shotsRect)

        # Отображение прямоугольника игрока
        windowSurface.blit(playerImage, playerRect)

        # Отрисовка взрывов
        for expl in explosions:
            windowSurface.blit(expl['surface'], expl['rect'])
        # Отрисовка ящиков с патронами
        for a in ammo:
            windowSurface.blit(a['surface'], a['rect'])
        # Отрисовка облаков переднего плана
        for c in clouds_f:
            windowSurface.blit(c['surface'], c['rect'])

        pygame.display.update()

        # Проверка подбора аммуниции
        for a in ammo[:]:
            if playerHasHitObject(playerRect, ammo):
                player_ammo += 25
                if player_ammo > 100: player_ammo = 100
                ammo.remove(a)
                getAmmoSound.play()

        # Проверка, попал ли в игрока какой-либо из злодеев.
        if not gamover and playerHasHitObject(playerRect, baddies):
            gamover = True
            explbigSound.play()
            add_explosion({'rect': playerRect, 'size': 2})
            playerExpl = explosions[-1]
            player_end_pos = playerRect.center
        if gamover and playerExpl['frame'] == 4:
            if score > topScore:
                topScore = score # установка нового рекорда
            break

        mainClock.tick(FPS)

    # Отображение игры и вывод надписи 'Игра окончена'.
    engineSound.stop()
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('ИГРА ОКОНЧЕНА!', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Нажмите клавишу для начала новой игры', font, windowSurface, (WINDOWWIDTH / 3) - 120, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
