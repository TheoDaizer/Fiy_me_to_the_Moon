from BaseObjects import *
from Globals import *


class Explosion(AnimatedSprite, SoundMixin):
    @staticmethod
    def getExplosion(parent, obj: Sprite, scale: float = None):
        if not scale:
            scale = obj.scale//2
        Explosion.get_sound().play()
        return Explosion(parent,
                         coordinates=obj.rect.center,
                         scale=scale,
                         sfx=True,
                         ticker=EXPLOSIVEANIMATIONSPEED
                         )


class StickyExplosion(AnimatedSprite, SoundMixin, StickerMixin):
    @staticmethod
    def getStickyExplosion(parent, obj: Sprite, scale: float = None):
        if not scale:
            scale = obj.scale
        StickyExplosion.get_sound().play()
        expl = StickyExplosion(parent,
                               coordinates=obj.rect.center,
                               scale=scale,
                               sfx=True,
                               ticker=EXPLOSIVEANIMATIONSPEED
                               )
        expl.init_sticker(obj, 'center')
        return expl


class ShootFire(AnimatedSprite, StickerMixin):
    @staticmethod
    def getShootFire(parent, obj: Sprite):
        shoot = ShootFire(parent,
                          coordinates=obj.rect.center,
                          sfx=True,
                          ticker=EXPLOSIVEANIMATIONSPEED
                          )
        shoot.init_sticker(obj, 'midtop')
        return shoot


class HitBullet(AnimatedSprite, SoundMixin):
    @staticmethod
    def getHitBullet(parent, obj: Sprite, scale: float = None):
        if not scale:
            scale = obj.scale//2
        HitBullet.get_sound().play()
        return HitBullet(parent,
                         coordinates=obj.rect.center,
                         scale=scale,
                         sfx=True,
                         ticker=1
                         )
