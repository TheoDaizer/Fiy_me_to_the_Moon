from BaseObjects import *
from Globals import *


class PlayerPlane(AnimatedSprite, MovingSprite):
    @staticmethod
    def getPlayerPlane(parent):
        s_frame = PlayerPlane.sprites_len()//2
        return PlayerPlane(parent,
                           start_frame=s_frame,
                           ticker=PLANEANIMATIONSPEED)

    def _change_player_sprite(self, left, right):
        if not left and not right:
            left = self.frame > self.start_frame
            right = self.frame < self.start_frame
        if left or right:
            if self.get_ticker():
                if left:
                    self.prev_frame()
                else:
                    self.next_frame()
                self.rect.width = self.sprite.get_width()

    def _player_move(self, u, d):
        if self.frame < self.start_frame and self.rect.left > 0:
            self.move_sprite((-1 * PLAYERMOVERATE, 0))
        if self.frame > self.start_frame and self.rect.right < WINDOWWIDTH:
            self.move_sprite((PLAYERMOVERATE, 0))
        if u and self.rect.top > 0:
            self.move_sprite((0, -1 * PLAYERMOVERATE))
        if d and self.rect.bottom < WINDOWHEIGHT:
            self.move_sprite((0, PLAYERMOVERATE))

    def move_player_sprite(self, l, r, u, d):
        self._change_player_sprite(l, r)
        self._player_move(u, d)


class Bullet(MovingSprite, SoundMixin):
    __cooldown = 0
    __ammo = 0
    @staticmethod
    def getBullet(parent, xy):
        return Bullet(parent,
                      coordinates=xy,
                      speed_y=-BULLETSPEED)

    @classmethod
    def get_cooldown(cls):
        return cls.__cooldown

    @classmethod
    def set_cooldown(cls, n):
        cls.__cooldown = n

    @classmethod
    def tick_cooldown(cls, n=1):
        if cls.__cooldown:
            cls.__cooldown -= n

    @classmethod
    def get_ammo(cls):
        return cls.__ammo

    @classmethod
    def change_ammo(cls, n=0):
        cls.__ammo += n
        if cls.__ammo < 0:
            cls.__ammo = 0
        if cls.__ammo > AMMOCAP:
            cls.__ammo = AMMOCAP

    @classmethod
    def set_ammo(cls, n):
        cls.__ammo = n

    @staticmethod
    def shootBullet(parent, xy):
        if Bullet.get_cooldown() or not Bullet.get_ammo():
            #Bullet.tick_cooldown()
            return None
        else:
            Bullet.set_cooldown(SHOOTDELAY)
            Bullet.change_ammo(-1)
            Bullet.get_sound().play()
            return Bullet.getBullet(parent, xy)


class Land(MovingSprite):
    @staticmethod
    def getLand(parent):
        land = Land(parent,
                    (0, -1),
                    speed_y=BACKGROUNDSPEED)
        land.rect.centerx = WINDOWWIDTH//2
        return land

    def shiftLand(self, moveLeft, moveRiht):
        if moveLeft and self.rect.left < 0:
            self.speed_x = BACKGROUNDSPEED
        elif moveRiht and self.rect.right > WINDOWWIDTH:
            self.speed_x = -BACKGROUNDSPEED
        else:
            self.speed_x = 0


    def move_sprite(self, move=None):
        super().move_sprite()
        if self.rect.top >= 0:
            self.rect.bottom = WINDOWHEIGHT


class Cloud(MovingSprite):
    @staticmethod
    def getCloud(parent):
        return Cloud(parent,
                     randscale=(CLOUDMINSIZE, CLOUDMAXSIZE),
                     random_speed=['y', (CLOUDMINSPEED, CLOUDMAXSPEED)],
                     outher='n',
                     random_pos='x',
                     random_sprite=True)


class Ammo(MovingSprite, CollisionMixin, SoundMixin):
    @staticmethod
    def getAmmo(parent):
        return Ammo(parent,
                    scale=AMMOSCALE,
                    speed_y=BADDIEMAXSPEED,
                    outher='n',
                    random_pos='x')

class MainMenu(MovingSprite):
    pass

if __name__ == '__main__':
    pass
