import pygame
from pygame.locals import *



class Ship(pygame.sprite.Sprite):

    ### size as a tuple
    def __init__(self, pos, size,  surf, graphic, health = 100, damage = 20, ):

        pygame.sprite.Sprite.__init__(self)


        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.xPOS = pos.vX
        self.yPOS = pos.vY
        self.POS = pos
        self.SURF = surf
        self.health = health
        self.damage = damage
        self.GRAPHIC = graphic
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT), flags = SRCALPHA, depth = 32)
        self.image.fill((0, 0, 0, 0))
        graphic1 = pygame.image.load(self.GRAPHIC).convert_alpha()
        graphic1 = pygame.transform.scale(graphic1, (self.WIDTH, self.HEIGHT))
        self.image.blit(graphic1, (0, 0))
        self.tempIMAGE = self.image



        self.rect = self.image.get_rect()
        self.rect.x = self.xPOS
        self.rect.y = self.yPOS


        self.image.blit(graphic1, (0,0))
        self.tempImage = self.image


        self.rect = self.image.get_rect()
        self.rect.x = self.xPOS
        self.rect.y = self.yPOS

        self.image.blit(graphic1, (0,0))
        self.tempImage = self.image





    def getDamage(self):
        return self.damage



    def getHealth(self):
        return self.health



    def minusHealth(self, minusHowMuch):
        self.health -= minusHowMuch



    def displaySpaceShip(self):
        self.SURF.blit(self.image, (self.rect.x, self.rect.y))

