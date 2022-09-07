from BaseObjects import *
from Globals import *
from random import choice


class Rocket(MovingSprite, CollisionMixin, HPMixin):
    @staticmethod
    def getRocket(parent):
        rocket = Rocket(parent,
                        randscale=(BADDIEMINSIZE, BADDIEMAXSIZE),
                        random_speed=['y', (BADDIEMINSPEED, BADDIEMAXSPEED)],
                        outher='n',
                        random_pos='x')
        rocket.init_hp()
        return rocket


class EnemySmallPlane(MovingSprite, CollisionMixin, HPMixin):
    @staticmethod
    def getEnemySmallPlane(parent):
        plane = EnemySmallPlane(parent,
                                scale=0.25,
                                speed_y=BADDIEMINSPEED*1.25,
                                speed_x=BADDIEMINSPEED*0.5*choice((-1, 1)),
                                outher='n',
                                random_pos='x',
                                ticker=120)
        plane.init_hp(3)
        return plane

    def move_sprite(self, move=None):
        if self.get_ticker():
            self.speed_x *= -1
        return super().move_sprite()

