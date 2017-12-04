import pygame, sys
from pygame.locals import *
from vector2 import vector2
from math import *

class bullet(pygame.sprite.Sprite):

    def __init__(self, pos, surf, vector, speed, size):
        # call parent class (sprite) constructor

        pygame.sprite.Sprite.__init__(self)

        self.SURF = surf
        self.SIZE = size
        self.POS = pos
        self.VECTOR = vector
        self.SPEED = speed

        self.image = pygame.Surface((self.SIZE,self.SIZE), flags=SRCALPHA, depth=32)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos.vX
        self.rect.y = pos.vY

        self.HSIZE = self.SIZE//2

        ######################
        ## get image for bullet
        self.bul = pygame.image.load("gbeam.jpg").convert_alpha()
        self.bul = pygame.transform.scale(self.bul, (self.SIZE, self.SIZE))

    def resizeSQ(self, x, y, xPOS, yPOS):
        # Resizes a Square on x-width and y-height sides
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()
        self.rect.x = xPOS
        self.rect.y = yPOS

    def __drawBullet(self):

        self.image.blit(self.bul, (0, 0))


    def __getRotation(self, vec1):

        vec2 = vector2(0.0, -1.0)
        angle = acos(vec2.dotProductV2(vec1))

        return angle


    def __moveBullet(self, pos, vec, speed):

        pos += vec * speed

        return pos


    def  __changePOS(self, pos):

        self.POS = vector2(pos.vX, pos.vY)
        self.rect.x = pos.vX
        self.rect.y = pos.vY


    def displayBullet(self):

        self.__changePOS(self.__moveBullet(self.POS, self.VECTOR, self.SPEED))
        self.__drawBullet()
        self.SURF.blit(self.image, (self.POS.vX - self.HSIZE, self.POS.vY - self.HSIZE))