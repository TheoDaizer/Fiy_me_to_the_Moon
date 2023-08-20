import sys

import pygame.font

from GameObjects import *
from Enemies import *
from SFX import *
from pygame.locals import *

def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Нажатие ESC осуществляет выход.
                    terminate()
                return


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

if __name__ == '__main__':
    # Настройка pygame, окна и указателя мыши.
    pygame.init()
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Fly Me to the Moon')
    pygame.mouse.set_visible(False)
    baddieAddCounter = 0

    # Настройка звуков.
    gameOverSound = pygame.mixer.Sound('sounds/effects/gameover.mp3')
    engineSound = pygame.mixer.Sound('sounds/effects/engine.mp3')
    pygame.mixer.music.load('sounds/music/16-voyager.mp3')

    # Настройка шрифтов.
    font = pygame.font.Font('fonts/Rafiquell.ttf', 30)
    font60 = pygame.font.Font('fonts/Rafiquell.ttf', 60)

    # Вывод начального экрана.
    windowSurface.fill(BACKGROUNDCOLOR)

    MainMenu.set_sprites('sprites/main/main_menu0.jpg')
    main_menu = MainMenu(windowSurface, coordinates=(-200, 0))

    Land.set_sprites('sprites/land/land0.png')
    lands = [Land.getLand(windowSurface)]

    Cloud.set_sprites('sprites/clouds/cloud0.png', 1)
    clouds = []
    b_clouds = []

    Rocket.set_sprites('sprites/enemies/bomb0.png')
    Rocket.resize_sprites((15, 31))
    enemies = []

    EnemySmallPlane.set_sprites('sprites/enemies/MedGray0.png')

    PlayerPlane.set_sprites('sprites/plane2/plane0.png', 7)
    PlayerPlane.resize_sprites(scale=SPRITESCALE)
    plane = PlayerPlane.getPlayerPlane(windowSurface)
    player_plane = [plane]

    Bullet.set_sprites('sprites/bullsets/bullet0.png')
    Bullet.set_sound('sounds/effects/shoot0.mp3')
    bullets = []

    Ammo.set_sprites('sprites/bonuses/ammo0.png')
    Ammo.set_sound('sounds/effects/get_bonus0.mp3')
    ammo = []

    Explosion.set_sprites('sprites/explosions/eb0.png', 8)
    Explosion.set_sound('sounds/effects/explosion2.mp3')
    explosions = []

    HitBullet.set_sprites('sprites/hits/shootBullet0.png', 4)
    HitBullet.set_sound('sounds/effects/explosion1.mp3')

    StickyExplosion.set_sprites('sprites/explosions/eb0.png', 8)
    StickyExplosion.set_sound('sounds/effects/big_expl0.mp3')
    stick_expls = []

    ShootFire.set_sprites('sprites/shots/shot0.png', 6)
    shoots = []

    movable = [lands, b_clouds, clouds, ammo, bullets, shoots, stick_expls, enemies]
    to_draw = [lands, b_clouds, enemies, ammo, shoots, player_plane, bullets, explosions, stick_expls, clouds]

    # Подготовка начального экрана
    pygame.mixer.music.play(-1, 0.0)
    lands[0].blit_sprite()
    main_menu.blit_sprite()
    drawText('Fly Me to the Moon', font60, windowSurface, (WINDOWWIDTH / 10), (WINDOWHEIGHT / 4))
    drawText('Press any key', font, windowSurface, (WINDOWWIDTH / 3),
             (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    score_timer = 0
    score = 0
    topScore = 0
    while True:
        pygame.mixer.music.load('sounds/music/04-wicked-child.mp3')
        #Начало новой игры
        enemies.clear()
        clouds.clear()
        bullets.clear()
        stick_expls.clear()
        plane.rect.midtop = (WINDOWWIDTH / 2, WINDOWHEIGHT - 150)
        moveLeft = moveRight = moveUp = moveDown = False
        lands[0].blit_sprite()
        plane.blit_sprite()
        Bullet.set_ammo(AMMOCAP)

        reverseCheat = slowCheat = False
        shoot = False
        game_over = False
        pause = False
        baddieAddCounter = 0
        sprite_state_x = [0, 0]
        sprite_state_y = [0, 0]

        engineSound.set_volume(0.1)
        engineSound.play(-1)
        pygame.mixer.music.play(-1, 0.0)

        if score > topScore:
            topScore = score
        score_timer = 0
        score = 0
        while True:
            score_timer += 1
            if score_timer == FPS//2:
                score += 1
                score_timer = 0
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

            lands[0].shiftLand(moveLeft, moveRight)

            if random.random() >= 0.999:
                ammo.append(Ammo.getAmmo(windowSurface))

            if len(clouds + b_clouds) < 1 and random.random() >= 0.995:
                c = random.choice([clouds, b_clouds])
                c.append(Cloud.getCloud(windowSurface))

            Bullet.tick_cooldown()
            if shoot:
                bullet = Bullet.shootBullet(windowSurface, (plane.rect.centerx, plane.rect.top - 5))
                if bullet:
                    if not shoots:
                        shoots.append(ShootFire.getShootFire(windowSurface, plane))
                    bullets.append(bullet)

            #places for cheats
            baddieAddCounter += 1
            if baddieAddCounter == ADDNEWBADDIERATE:
                baddieAddCounter = 0
                enemy = random.choice([Rocket.getRocket, EnemySmallPlane.getEnemySmallPlane])
                enemies.append(enemy(windowSurface))

            windowSurface.fill(BACKGROUNDCOLOR)
            for object, group in ((obj, group) for group in movable for obj in group):
                to_del = object.move_sprite()
                if to_del:
                    group.remove(object)

            plane.move_player_sprite(moveLeft, moveRight, moveUp, moveDown)

            for object, group in ((obj, group) for group in to_draw for obj in group):
                to_del = object.blit_sprite()
                if to_del:
                    group.remove(object)

            # Отображение количества очков и лучшего результата.
            drawText('Scote: {}'.format(score), font, windowSurface, 10, 10)
            drawText('Top scort: {}'.format(topScore), font, windowSurface, 10, 50)
            drawText('Ammo {}'.format(Bullet.get_ammo()), font, windowSurface, 450, 10)

            if pause:
                waitForPlayerToPressKey()
                pause = False

            pygame.display.update()
            for enemy in enemies[:]:
                bullet = enemy.collision_check(bullets)
                if bullet:
                    if enemy.get_hit(1.25):
                        explosions.append(Explosion.getExplosion(windowSurface, enemy))
                        enemies.remove(enemy)
                        score += 100
                    else:
                        explosions.append(HitBullet.getHitBullet(windowSurface, bullet, scale=0.7))
                    bullets.remove(bullet)
                    continue
                if not game_over and enemy.collision_object(plane):
                    game_over = True
                    stick_expls.append(StickyExplosion.getStickyExplosion(windowSurface, plane))
                    enemies.remove(enemy)
                    break

            for amm in ammo:
                if amm.collision_object(plane):
                    Bullet.change_ammo(25)
                    amm.play_sound()
                    ammo.remove(amm)
                    score += 100

            if game_over and stick_expls[0].frame == 3:
                break

            mainClock.tick(FPS)

        # Отображение игры и вывод надписи 'Игра окончена'.
        engineSound.stop()
        pygame.mixer.music.stop()
        gameOverSound.play()

        drawText('Game  Over', font60, windowSurface, (WINDOWWIDTH / 3)-40, (WINDOWHEIGHT / 4))
        drawText('press any key to start new game', font, windowSurface, (WINDOWWIDTH / 8) + 20,
                 (WINDOWHEIGHT / 3) + 100)
        pygame.display.update()
        waitForPlayerToPressKey()

        gameOverSound.stop()