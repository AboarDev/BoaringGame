import pygame


class GameObject:
    pass


class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plus(self, inputs):
        return Vec(self.x + inputs.x, self.y + inputs.x)

    def times(self, inputs):
        return Vec(self.x * inputs, self.y * inputs)


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#000000""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = False
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x - self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x + self.offset_x


class Coin(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#ffb700""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = False
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x - self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x + self.offset_x


class Lava(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#FF0000""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = False
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x - self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x + self.offset_x


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#00FF00""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = True
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset
        self.set_offset = ''
        self.grounded = True

    def collide(self, x, y, rect, level_objects):
        if x > 1:
            i = -1
        else:
            i = 1
        if pygame.sprite.spritecollide(self, level_objects, False):
            x = x + i
            self.rect = rect
            self.rect = self.rect.move([x, 0])
            self.collide(x, 0, rect, level_objects)

    def move(self, level_objects, x=0, y=0):
        self.offset_x = self.get_offset()
        # if self.rect.x >= 450 + self.offset_x * 1 and x > 0:
        if self.rect.x >= 445 and x > 0:
            print(self.rect.x, self.offset_x, (self.offset_x * -1) + 450)
            base_rect = self.rect
            self.rect = self.rect.move([x, 0])
            if not pygame.sprite.spritecollide(self, level_objects, False):
                self.set_offset(self.offset_x - (x))
            self.rect = base_rect
        else:
            base_rect = self.rect
            self.rect = self.rect.move([x, y])
            self.collide(x, y, base_rect, level_objects)

    def update(self, *args):
        pass


class Mob(GameObject):
    def __init__(self):
        self.speed = 0

