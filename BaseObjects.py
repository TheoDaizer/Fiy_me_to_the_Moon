import pygame, random
from Globals import WINDOWWIDTH, WINDOWHEIGHT

class Sprite:
    sprites = []

    def __init__(self,
                 parent,
                 coordinates: tuple,
                 scale: float,
                 randscale: tuple,
                 ticker: int = 0,
                 sprite_n: int = 0,
                 random_sprite: bool = False
                 ):
        # Работа с масштабированием
        self.scale = scale if scale else 1
        if randscale:
            self.scale *= random.randint(*randscale) / 100
        self.scale = round(self.scale, 2)

        if random_sprite:
            sprite_n = random.randint(0, self.sprites_len()-1)
        size = [dem * self.scale for dem in self.get_sprite(sprite_n).get_size()]

        self.parent = parent
        self.__rect = pygame.Rect(coordinates, size)
        self.sprite = pygame.transform.scale(self.get_sprite(sprite_n), size)
        self.base_value = ticker
        self.ticker = 0

    @property
    def rect(self):
        return self.__rect

    @classmethod
    def set_sprites(cls, dir: str, n=1):
        cls.sprites = [(pygame.image.load(f'{dir[:-5]}{i}{dir[-4:]}')) for i in range(n)]

    @classmethod
    def get_sprite(cls, n=0):
        return cls.sprites[n]

    @classmethod
    def resize_sprites(cls, x_y: tuple = (1, 1), scale=None):
        for i in range(len(cls.sprites)):
            if scale:
                cls.sprites[i] = pygame.transform.scale(cls.sprites[i],
                                                        (cls.sprites[i].get_width()*scale,
                                                         cls.sprites[i].get_height()*scale))
            else:
                cls.sprites[i] = pygame.transform.scale(cls.sprites[i], x_y)

    @classmethod
    def sprites_len(cls):
        return len(cls.sprites)

    def blit_sprite(self):
        self.parent.blit(self.sprite, self.rect)
        return False

    def get_ticker(self):
        if self.ticker == 0:
            self.ticker = self.base_value
            return True
        self.ticker -= 1
        return False


class MovingSprite(Sprite):
    def __init__(self,
                 parent,
                 coordinates: tuple = (0, 0),
                 scale: float = None,
                 randscale: tuple = None,
                 ticker: int = 0,
                 sprite_n: int = 0,
                 random_sprite: bool = False,
                 speed_y: float = 0,
                 speed_x: float = 0,
                 random_speed: list = None,
                 outher: str = '',
                 random_pos: str = '',
                 cyclic_move: bool = False
                 ):
        super().__init__(parent, coordinates, scale, randscale, ticker, sprite_n, random_sprite)
        self.speed_y = speed_y
        self.speed_x = speed_x
        self.cyclic_move = cyclic_move

        if random_speed: self.__random_speed(random_speed)
        if outher: self.__outher(outher)
        if random_pos: self.__random_pos(random_pos)

    def __random_speed(self, random_speed):
        if 'x' in random_speed[0]:
            self.speed_x = random.randint(*random_speed[1])
        if 'y' in random_speed[0]:
            self.speed_y = random.randint(*random_speed[1])

    def __outher(self, outher):
        if 'n' in outher:
            self.rect.bottom = 0
        if 's' in outher:
            self.rect.top = WINDOWHEIGHT
        if 'w' in outher:
            self.rect.right = 0
        if 'e' in outher:
            self.rect.left = WINDOWWIDTH

    def __random_pos(self, random_pos):
        if 'x' in random_pos:
            self.rect.left = random.randint(-int(self.rect.width) // 2, WINDOWWIDTH - int(self.rect.width) // 2)
        if 'y' in random_pos:
            self.rect.top = random.randint(-int(self.rect.height) // 2, WINDOWHEIGHT - int(self.rect.height) // 2)

    @property
    def speed(self):
        return self.speed_x, self.speed_y

    def move_sprite(self, move=None):
        if move:
            self.rect.move_ip(*move)
        else:
            self.rect.move_ip(*self.speed)
        if not self.cyclic_move:
            if self.rect.bottom < 0 or \
                    self.rect.top > WINDOWHEIGHT or \
                    self.rect.right < 0 or \
                    self.rect.left > WINDOWWIDTH:
                return True
            return False


class AnimatedSprite(Sprite):
    def __init__(self,
                 parent,
                 coordinates: tuple = (0, 0),
                 scale: float = None,
                 randscale: tuple = None,
                 ticker: int = 0,
                 sprite_n: int = 0,
                 random_sprite: bool = False,
                 frame: int = 0,
                 start_frame: int = 0,
                 cyclic: bool = False,
                 trigger: bool = True,
                 sfx: bool = False
                 ):
        if start_frame:
            sprite_n = start_frame
            frame = start_frame
        super().__init__(parent, coordinates, scale, randscale, ticker, sprite_n, random_sprite)
        self.frame = frame
        self.start_frame = start_frame
        self.cyclic = cyclic
        self.trigger = trigger
        self.sfx = sfx

    def get_frame(self):
        self.sprite = (self.get_sprite(self.frame))
        if self.scale != 1:
            self.sprite = pygame.transform.scale(self.sprite,
                                                 (self.sprite.get_width() * self.scale,
                                                  self.sprite.get_height() * self.scale))

    def next_frame(self):
        if self.frame + 1 < self.sprites_len():
            self.frame += 1
        elif self.cyclic:
            self.frame = self.start_frame
        elif not self.sfx:
            return False
        else:
            return True
        self.get_frame()
        return False

    def prev_frame(self):
        if self.frame - 1 >= 0:
            self.frame -= 1
        elif self.cyclic:
            self.frame = self.sprites_len()
        elif not self.sfx:
            return False
        else:
            return True
        self.get_frame()
        return False

    def blit_sprite(self):
        if self.get_ticker():
            if self.cyclic or self.sfx:
                if self.next_frame():
                    return True
        self.parent.blit(self.sprite, self.rect)

        return False


class StickerMixin:
    def init_sticker(self, owner: Sprite, point):
        self.owner = owner.rect
        self.owner_point = point

    def move_sprite(self):
        if self.owner_point == 'center':
            self.rect.center = self.owner.center
        if self.owner_point == 'midtop':
            self.rect.center = self.owner.midtop


class CollisionMixin:
    def collision_object(self, obj):
        return self.rect.colliderect(obj.rect)

    def collision_check(self, obj_list):
        for obj in obj_list:
            if self.rect.colliderect(obj.rect):
                return obj
        return None


class SoundMixin:
    sounds = []

    @classmethod
    def set_sound(cls, dir: str, n=1):
        cls.sounds = [(pygame.mixer.Sound(f'{dir[:-5]}{i}{dir[-4:]}')) for i in range(n)]

    @classmethod
    def get_sound(cls, n=0):
        return cls.sounds[n]

    def play_sound(self, n=0):
        self.get_sound(n).play()


class HPMixin:
    def init_hp(self, hp=None):
        if hp:
            self.hp = hp
        else:
            self.hp = self.scale

    def get_hit(self, damage=1):
        self.hp -= damage
        if self.hp > 0:
            return False
        return True


if __name__ == '__main__':
    pass
