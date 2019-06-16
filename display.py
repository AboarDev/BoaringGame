import pygame


class Display:

    def __init__(self):
        pygame.init()
        self.size = [600, 450]
        self.color = [255, 255, 255]
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(self.color)
        # py game.draw.rect(self.screen, [000, 000, 000], [20, 20, 20, 20], 1)
        pygame.display.flip()
        pygame.display.set_caption('Test')


if __name__ == '__main__':
    new = Display()
