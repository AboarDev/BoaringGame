import pygame
from pygame import *
import display
import gameobjects
import level
import asyncio
import sys
import time as py_time


class Game:
    def __init__(self, levels):
        self.display = display.Display()
        self.levels = levels
        self.keys = ['up', 'down', 'left', 'right']
        self.jump = 'ALLOWED'

    def handle_input(self, keys, move_func, collide):
        if self.keys[0] in keys:
            if self.jump == 'ALLOWED':
                # move_func(collide, 0, -16)
                self.jump = 'JUMPING'
        if self.keys[2] in keys and self.keys[3] not in keys:
            move_func(collide, -3)
        if self.keys[3] in keys and self.keys[2] not in keys:
            move_func(collide, 3)

    def handle_jumps(self, increment, collide, move_func):
        if increment > 0:
            print(self.jump)
            move_func.move(collide, 0, -24)
            return increment - 1
        else:
            self.jump = 'TRACKED'
            move_func.grounded = False
            print(self.jump)
    # Runs the level itself and returns a status message, statuses are PLAYING, WON, LOST, and QUIT

    async def run_level(self, lvl):
        lvl = level.Level(lvl)
        lvl.create_offset(self.display.size)
        objects = lvl.create_objects({'#': gameobjects.Platform, 'o': gameobjects.Coin, '+': gameobjects.Lava,
                                      '@': gameobjects.Player})
        objects.draw(self.display.screen)
        pygame.display.flip()
        status = 'PLAYING'
        keys_down = []
        a_jump = 6
        while status == 'PLAYING':
            for an_event in pygame.event.get():
                if an_event.type == QUIT:
                    status = 'QUIT'
                if an_event.type == KEYUP and str(pygame.key.name(an_event.key)) in keys_down:
                    keys_down.remove(pygame.key.name(an_event.key))
                if an_event.type == KEYDOWN and str(pygame.key.name(an_event.key)) in self.keys:
                    keys_down.append(pygame.key.name(an_event.key))
                    # lvl.player.move(6)
            if len(keys_down) > 0:
                self.handle_input(keys_down, lvl.player.move, lvl.objects)
            # lvl.update_offset(lvl.player)
            if self.jump == 'JUMPING':
                a_jump = self.handle_jumps(a_jump, lvl.objects, lvl.player)
            elif self.jump == 'TRACKED':
                lvl.player.update()
                if lvl.player.grounded is True:
                    self.jump = 'ALLOWED'
                    a_jump = 6
            objects.draw(self.display.screen)
            pygame.display.update()
            self.display.screen.fill([255, 255, 255])
            py_time.sleep(0.016)

        if status == 'QUIT':
            sys.exit()
        return status

    # Runs every level in order by waiting on a status
    async def run_levels(self):
        i = 0
        while i < len(self.levels):
            status = await self.run_level(self.levels[i])
            # print(i)
            if status == 'WON':
                i += 1


if __name__ == '__main__':
    new = Game(["""................................................................................
................................................................................
................................................................................
................................................................................
................................................................................
................................................................................
..................................................................###...........
...................................................##......##....##+##..........
....................................o.o......##..................#+++#..........
..............................##.................................##+##..........
...................................#####..........................#v#...........
............................................................................##..
..###.....................................o.o................................#..
..#.....................o....................................................#..
..#......................................#####.............................o.#..
..#.....................o....................................................#..
..#..@...........................................................#####.......#..
..##########....###############...####################.....#######...#########..
...........#++++#.............#...#..................#.....#....................
...........######.............#+++#..................#+++++#....................
..............................#+++#..................#+++++#....................
..............................#####..................#######....................
................................................................................
................................................................................""", 'a', 'a'])
    asyncio.run(new.run_levels())
