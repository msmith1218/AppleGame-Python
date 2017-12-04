import pygame
from pygame.locals import *
from random import *



class Life(pygame.sprite.Sprite):

    def __init__(self, surf, size):

        pygame.sprite.Sprite.__init__(self)
        self.SURF = surf
        self.SIZE = size

        self.image = pygame.Surface((self.SIZE, self.SIZE), flags=SRCALPHA, depth = 32)

        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

        self.met = pygame.image.load('metra.jpg').convert_alpha()
        self.met = pygame.transform.scale(self.met, (self.SIZE, self.SIZE))


    def __drawLife(self):
        self.image.blit(self.met, (0, 0))


    def displayLife(self):
        self.__drawLife()
        self.SURF.blit(self.image, (randrange(0,500), randrange(0,200)))