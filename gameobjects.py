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
        self.has_collide = False
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x + self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x - self.offset_x


class Coin(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#ffb700""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = False
        self.has_collide = True
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x + self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x - self.offset_x


class Lava(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#FF0000""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = False
        self.has_collide = True
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset

    def update(self, *args):
        x = self.rect.x + self.offset_x
        self.offset_x = self.get_offset()
        self.rect.x = x - self.offset_x


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, get_offset, color=pygame.Color("""#00FF00""")):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_player = True
        self.has_collide = False
        self.offset_y = 0
        self.offset_x = 0
        self.get_offset = get_offset
        self.set_offset = ''
        self.grounded = True
        self.level = None

    def collide_x(self, x, rect, level_objects, depth=0, i=None):
        if not i:
            if x > 0:
                i = -1
            elif x < 0:
                i = 1
            else:
                i = 0
        if pygame.sprite.spritecollide(self, level_objects, False):
            x = x + i
            self.rect = rect.move([x, 0])
            if depth < 4:
                self.collide_x(x, rect, level_objects, depth+1, i)
            else:
                print('depth', depth)
                # self.grounded = False

    def collide_y(self, y, rect, level_objects):
        if y == 0:
            self.grounded = True
            self.rect = self.rect.move([0,0])
            return
        if y > 1:
            i = -2
        else:
            i = 1
        if pygame.sprite.spritecollide(self, level_objects, False):
            y = y + i
            self.rect = rect.move([0, y])
            self.collide_y(y, rect, level_objects)

    def move(self, level_objects, x=0, y=0):
        if not self.level:
            self.level = level_objects
        self.offset_x = self.get_offset()
        # print(self.offset_x)
        # if self.rect.x >= 450 + self.offset_x * 1 and x > 0:
        if x is not 0:
            if self.rect.x >= 450 and x > 0:
                # print(self.rect.x, self.offset_x, (self.offset_x * -1) + 450)
                base_rect = self.rect
                self.rect = self.rect.move([x, 0])
                if not pygame.sprite.spritecollide(self, level_objects, False):
                    self.set_offset(self.offset_x + (x))
                self.rect = base_rect

            elif self.rect.x <= 150 and x < 0 and self.offset_x > 0:
                base_rect = self.rect
                self.rect = self.rect.move([x, 0])
                if not pygame.sprite.spritecollide(self, level_objects, False):
                    self.set_offset(self.offset_x + (x))
                self.rect = base_rect

            else:
                base_rect = self.rect
                self.rect = self.rect.move([x, y])
                self.collide_x(x,base_rect,level_objects)

            base_rect = self.rect
            self.rect = self.rect.move([0,6])
            self.collide_y(6,base_rect,level_objects)
            if self.rect != base_rect:
                self.grounded = False
            self.rect = base_rect
        elif y is not 0:
            base_rect = self.rect
            self.rect = self.rect.move([x, y])
            self.collide_y(y,base_rect,level_objects)

    def update(self, *args):
        base_rect = self.rect
        if self.grounded is True:
            self.image.fill(pygame.Color("""#00FF00"""))
        elif self.grounded is False:
            self.image.fill(pygame.Color("""#00FFFF"""))
            self.rect = self.rect.move([0,6])
            self.collide_y(6, base_rect, self.level)


class Mob(GameObject):
    def __init__(self):
        self.speed = 0

