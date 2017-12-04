import pygame
from pygame.locals import *
from vector2 import vector2




class Enemy(pygame.sprite.Sprite):

    def __init__ (self, pos, surf, vector, speed, size):

        pygame.sprite.Sprite.__init__(self)
        self.SURF = surf
        self.SIZE = size
        self.POS = pos
        self.VECTOR = vector
        self.SPEED = speed


        self.image = pygame.Surface((self.SIZE, self.SIZE), flags = SRCALPHA, depth = 32)

        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos.vX
        self.rect.y = pos.vY

        self.HSIZE = self.SIZE//2

        self.met = pygame.image.load("spikeball.png").convert_alpha()
        self.met = pygame.transform.scale(self.met, (self.SIZE, self.SIZE))



    def resizeSQ(self, x, y, xPOS, yPOS):
        # Resizes a Square on x-width and y-height sides
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()
        self.rect.x = xPOS
        self.rect.y = yPOS


    def __drawEnemy(self):

        self.image.blit(self.met, (0, 0))



    def __moveEnemy(self, pos, vec, speed):

        pos += vec * speed

        return pos


    def __changePOS(self, pos):

        self.POS = vector2(pos.vX, pos.vY)
        self.rect.x = pos.vX
        self.rect.y = pos.vY


    def displayEnemy(self):

        self.__changePOS(self.__moveEnemy(self.POS, self.VECTOR, self.SPEED))
        self.__drawEnemy()
        self.SURF.blit(self.image, (self.POS.vX - self.HSIZE, self.POS.vY - self.HSIZE))
