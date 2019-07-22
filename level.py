import pygame


class Level:

    def __init__(self, plan):
        self.scale = 24
        self.rows = plan.rstrip().split('\n')
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.actors = []
        self.offset_y = 0
        self.offset_x = 0
        self.spawn = 1
        self.player = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()

    def test(self):
        pass

    def get_offset(self):
        return self.offset_x

    def create_offset(self, display_size):
        # x = display_size[0]
        y = display_size[1]
        i = y/self.scale
        i = self.height - i
        i = i*self.scale
        self.offset_y = i

    def set_offset(self, offset):
        self.offset_x = offset
        self.objects.update()

    def update_offset(self, player):
        initial_offset = self.offset_x
        self.offset_x += 6
        self.objects.update()
        if player.rect.x - initial_offset > 450:
            print('time')

    def create_objects(self, key):
        entities = pygame.sprite.Group()
        lvl_rw = 0
        for row in self.rows:
            # print(row)
            lvl_clm = 0
            while lvl_clm < self.width:
                if row[lvl_clm] in key:
                    con_str = key[row[lvl_clm]]
                    a_object = con_str(self.scale, self.scale, (lvl_clm*self.scale), (lvl_rw*self.scale)-self.offset_y,
                                       self.get_offset)
                    entities.add(a_object)
                    if a_object.is_player is True:
                        self.player = a_object
                        self.player.set_offset = self.set_offset
                    else:
                        self.objects.add(a_object)
                lvl_clm += 1

            lvl_rw += 1
        return entities
