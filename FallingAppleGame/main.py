from ship import Ship
import pygame, sys
from pygame.locals import *
from vector2 import vector2
from EnemyObj import Yummy
from random import *
from Enemy import Enemy
from pygame import mixer
## from Bullet import bullet



FPS = 60
WINDOWWIDTH = 1280
WINDOWHEIGHT = 600



#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (255, 255, 255)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)

pygame.init()

splat = pygame.mixer.Sound('birdsplat.wav')
splat.set_volume(.5)

bomb = pygame.mixer.Sound('shoot.wav')
bomb.set_volume(.3)




enemyList = pygame.sprite.Group()
enemyLIST = pygame.sprite.Group()
yumLIST = pygame.sprite.Group()
lifeLIST = pygame.sprite.Group()
bulletLIST = pygame.sprite.Group()


global score, lives

pygame.init()

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    # initialize pygame and fps clock, displaysurf and set caption

FPSCLOCK = pygame.time.Clock()
    # set size of display surface using globals declared previously
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('APPLE DESTROYER')


def main():

    pygame.init()
    mixer.init()
    mixer.music.load('musiz.wav')
    mixer.music.play(loops = -1, start = 0)
    pygame.mixer.music.set_volume(.35)


    score = 0
    lives = 5
    tillNextLife = 1



    numEnemies = 1

    backgroundImageName = 'BG2.jpg'




    BGImage = pygame.image.load(backgroundImageName)


    BGImage = pygame.transform.scale(BGImage, (WINDOWWIDTH, WINDOWHEIGHT))

    ##### vector 1 creation
    ##TEMPvector = vector2.fromPoints(())


    shipx = WINDOWWIDTH // 2
    shipy = WINDOWHEIGHT -75

    check = True

    currentDirection = "left"

    makeYummys()
    makeEnemy()

    movex, movey = 0, 0

    # main game loop
    while True:



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RIGHT or event.key == K_d:
                    movex += 10
                    currentDirection = "right"
                elif event.key == K_LEFT or event.key == K_a:
                    movex -= 10
                    currentDirection = "left"
                elif event.key == K_UP or event.key == K_w:
                    movey -= 10
                    currentDirection = "up"
                elif event.key == K_DOWN or event.key == K_s:
                    movey += 10
                    currentDirection = "down"





            elif event.type == KEYUP:

                if event.key == K_DOWN or event.key == K_s:
                    movey -= 10

                elif event.key == K_UP or event.key == K_w:
                    movey += 10
                elif event.key == K_LEFT or event.key == K_a:
                   movex += 10
                elif event.key == K_RIGHT or event.key == K_d:
                    movex -= 10
                elif event.key == K_SPACE:
                    check = True
                    ##bulletLIST.add(bullet(ssPOS, DISPLAYSURF, vector1, 30, 30))

        DISPLAYSURF.blit(BGImage, (0, 0))
        shipx += movex
        shipy += movey

        ssPOS = vector2(shipx, shipy)

        playa = makePlayer(ssPOS)
        w = playa.WIDTH
        h = playa.HEIGHT

        if len(yumLIST) < 6:
            makeYummys()

        if len(enemyLIST) < numEnemies:
            makeEnemy()




        ## calculating how many till the next life
        if score < 50:
            tillNextLife = 50 - score
        elif score == 50:
            tillNextLife = 0
        elif score > 50 and score < 120:
            tillNextLife = 120 - score
        elif score == 120:
            tillNextLife = 0
        elif score > 120 and score < 200:
            tillNextLife = 200 - score
        elif score == 200:
            tillNextLife = 0





        ## defining the amount of enemies based on score
        if score > 20 and score < 50:
            numEnemies = 5

        if score > 50 and score < 100:
            numEnemies = 8

        if score > 100 and score < 120:
            numEnemies = 12

        if score > 120 and score < 150:
            numEnemies = 15

        if score > 150 and score < 180:
            numEnemies = 20

        if score > 180 and score < 220:

            numEnemies = 25

        if score > 220 and score < 250:
            numEnemies = 35

        if score > 250 and score < 280:
            numEnemies = 40

        if score > 280 and score < 300:
            numEnemies = 50

        if score > 300:
            numEnemies = 1






        ### boundaries
        if shipx <= w//2:
            shipx = w//2
        if shipy <= h//2:
            shipy = h//2
        if shipx >= WINDOWWIDTH - w//2:
            shipx = WINDOWWIDTH - w//2
        if shipy >= WINDOWHEIGHT - h//2:
            shipy = WINDOWHEIGHT - h//2




        meteorBulletHitList = pygame.sprite.groupcollide(bulletLIST, enemyLIST, True, True)
        for meteor in meteorBulletHitList:
            enemyLIST.remove(meteor)
            score += 1


        for x in meteorBulletHitList:
            bulletLIST.remove(x)



        for B in bulletLIST:
            if B.rect.x > 0 and B.rect.y > 0 and B.rect.x < WINDOWWIDTH and B.rect.y < WINDOWHEIGHT:
                B.displayBullet()
            elif check == True:
                bulletLIST.remove(B)


        ## delete yums and enemies if they are outside boundaries
        for yum in yumLIST:
            if yum.rect.x > WINDOWWIDTH or yum.rect.y > WINDOWHEIGHT:

                if check == True:
                    yumLIST.remove(yum)


        for enemy in enemyLIST:
            if enemy.rect.x > WINDOWWIDTH or enemy.rect.y > WINDOWHEIGHT:
                if check == True:
                    enemyLIST.remove(enemy)






        ## collision between player and apples
        if (pygame.sprite.spritecollide(playa, yumLIST, True)):
            score += 1
            splat.play()


        ## collision between player and enemy
        if (pygame.sprite.spritecollide(playa, enemyLIST, True)):
            lives -= 1
            bomb.play()



        ## return the score and exit main loop when all out of lives
        if lives <= 0:
            return (score, None, tillNextLife)

        if score >= 200:
            return (score, lives)


        ## give player lives based on their score
        if score >=50 and score <=52:
            if lifeUp50(score) == True:

                lives += 1
            lifeUpShow()

        if score >= 120 and score <= 122:
            if lifeUp120(score) == True:
                lives += 1
            lifeUpShow()


        if score >= 200 and score <= 202:
            if lifeUp200(score) == True:
                lives += 2
            lifeUpShow()



        ## desplay all the yums and the enemies
        for EX in yumLIST:
            EX.displayYum()



        for EX in enemyLIST:
            EX.displayEnemy()



        ### blitting
        displayscore(score, lives, tillNextLife)
        playa.displaySpaceShip()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main2(skore, livez):

    pygame.init()
    mixer.init()
    mixer.music.load('07-rounds-6-12-16.mp3')
    mixer.music.play(loops = -1, start = 0)
    pygame.mixer.music.set_volume(.35)

    score = skore
    lives = livez

    numEnemies = 2

    backgroundImageName = 'BG.jpg'




    BGImage = pygame.image.load(backgroundImageName)


    BGImage = pygame.transform.scale(BGImage, (WINDOWWIDTH, WINDOWHEIGHT))



    shipx = WINDOWWIDTH // 2
    shipy = WINDOWHEIGHT -75

    check = True



    makeYummys()
    makeEnemy()

    movex, movey = 0, 0

    # main game loop
    while True:



        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_RIGHT or event.key == K_d:
                    movex += 10
                elif event.key == K_LEFT or event.key == K_a:
                    movex -= 10
                elif event.key == K_UP or event.key == K_w:
                    movey -= 10
                elif event.key == K_DOWN or event.key == K_s:
                    movey += 10

            elif event.type == KEYUP:

                if event.key == K_DOWN or event.key == K_s:
                    movey -= 10

                elif event.key == K_UP or event.key == K_w:
                    movey += 10
                elif event.key == K_LEFT or event.key == K_a:
                    movex += 10
                elif event.key == K_RIGHT or event.key == K_d:
                    movex -= 10






        DISPLAYSURF.blit(BGImage, (0, 0))
        shipx += movex
        shipy += movey

        ssPOS = vector2(shipx, shipy)

        playa = makePlayer(ssPOS)
        w = playa.WIDTH
        h = playa.HEIGHT

        if len(yumLIST) < 6:
            makeYummys()

        if len(enemyLIST) < numEnemies:
            makeEnemy()



        ## defining the amount of enemies based on score


        if score > 200 and score < 250:
            numEnemies = 10

        if score > 250 and score < 280:
            numEnemies = 15

        if score > 280 and score < 300:
            numEnemies = 20

        if score > 300:
            numEnemies = 30






        ### boundaries
        if shipx <= w//2:
            shipx = w//2
        if shipy <= h//2:
            shipy = h//2
        if shipx >= WINDOWWIDTH - w//2:
            shipx = WINDOWWIDTH - w//2
        if shipy >= WINDOWHEIGHT - h//2:
            shipy = WINDOWHEIGHT - h//2





        ## delete yums and enemies if they are outside boundaries
        for yum in yumLIST:
            if yum.rect.x > WINDOWWIDTH or yum.rect.y > WINDOWHEIGHT:

                if check == True:
                    yumLIST.remove(yum)


        for enemy in enemyLIST:
            if enemy.rect.x > WINDOWWIDTH or enemy.rect.y > WINDOWHEIGHT:
                if check == True:
                    enemyLIST.remove(enemy)






        ## collision between player and apples
        if (pygame.sprite.spritecollide(playa, yumLIST, True)):
            score += 1
            splat.play()


        ## collision between player and enemy
        if (pygame.sprite.spritecollide(playa, enemyLIST, True)):
            lives -= 1
            bomb.play()



        ## return the score and exit main loop when all out of lives
        if lives <= 0:
            return (score, None)



        ## give player lives based on their score
        if score == 50:
            if lifeUp50(score) == True:

                lives += 1


        if score == 100:
            if lifeUp120(score) == True:
                lives += 1



        if score == 150:
            if lifeUp200(score) == True:
                lives += 2




        ## desplay all the yums and the enemies
        for EX in yumLIST:
            EX.displayYum()



        for EX in enemyLIST:
            EX.displayEnemy()



        ### blitting
        displayscore(score, lives)
        playa.displaySpaceShip()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def runGame():



    skore = (0, 5)
    showStartScreen(*skore)

    a = main()
    ## a holds a tuple that is the final score and lives.
    ## then it gets unpacked and inserted into gameover() as a parameter

    b = not all(a)

    if b == False:
        c = main2(*a)
        d = not all(c)

        if d != False:
            gameover(*c)

    else:
        gameover(*a)


def terminate():
    pygame.quit()
    sys.exit()


def displayscore(score, lives, tillNextLife):
    scoreSurf = BASICFONT.render('SCORE: %s' % score, True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH -170, 3)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    livesSurf = BASICFONT.render('LIVES: %s' % lives, True, WHITE)
    livesRect = livesSurf.get_rect()
    livesRect.topleft = (30 , 3)
    DISPLAYSURF.blit(livesSurf, livesRect)

    numTillLifeSurf = BASICFONT.render('Apples Till Next Life: %s' % tillNextLife, True, WHITE)
    numTillLifeRect = numTillLifeSurf.get_rect()
    numTillLifeRect.center = (WINDOWWIDTH / 2, 10)
    DISPLAYSURF.blit(numTillLifeSurf, numTillLifeRect)

def gameover(skore, livez, tillNum):
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10)


    while True:
        DISPLAYSURF.fill(DARKGRAY)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    terminate()
        displayscore(skore, livez, tillNum)
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        pygame.display.update()


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


@run_once
def lifeUp50(skore):
    if skore == 50:
        return True


@run_once
def lifeUp120(skore):
    if skore == 120:
        return True

@run_once
def lifeUp200(skore):
    if skore == 200:
        return True



def makePlayer(pos):
    size = (50, 50)
    graphic = 'gamenwatch.png'
    return Ship(pos, size, DISPLAYSURF, graphic)


def makeEnemy():
    enemys = 1
    enemyLIST.add(Enemy(vector2(randrange(100, 1300), 0), DISPLAYSURF, vector2(0, 1), 1.5, 50))

    while enemys > 0:
        randx = randrange(50, 1250)
        randy = randrange(-1000, 0)

        if randx > 10 and randx < WINDOWWIDTH -40:
            v1 = vector2(randx, randy)
            v2 = vector2.fromPoints((randx, randy), (randx, WINDOWHEIGHT -1))
            v2 = v2.normalizeV2()
            enemyLIST.add(Enemy(v1, DISPLAYSURF, v2, randint(1, 2), randint(35, 50)))
            enemys -= 1


def makeYummys():
    enemys = 10
    yumLIST.add(Yummy(vector2(randrange(100, 1300), 0), DISPLAYSURF, vector2(0, 1), 1.5, 30))

    while enemys > 0:
        randx = randrange(50, 650)
        randy = randrange(-1000, 0)

        if randx > 10 and randx < WINDOWWIDTH - 40:
            v1 = vector2(randx,randy)
            v2 = vector2.fromPoints((randx, randy), (randx, WINDOWHEIGHT-1))
            v2 = v2.normalizeV2()
            enemyList.add(Yummy(v1, DISPLAYSURF, v2, randint(1, 2), randint(35, 50)))
            enemys -= 1


def showStartScreen(score, lives):
    numz = 50
    while True:

        DISPLAYSURF.fill(DARKGREEN)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return


        displayscore(score, lives, numz)
        pygame.display.update()

        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    titlefont = pygame.font.Font('freesansbold.ttf', 60)

    pressKeySurf = BASICFONT.render('use WASD keys to navigate, or arrow keys'
                                    ',  press any key to play', True, DARKGRAY)

    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH // 4, WINDOWHEIGHT - 30)

    instructionsSurf = titlefont.render('move your player to collect falling apples', True, DARKGRAY)
    instructionsRect = instructionsSurf.get_rect()
    instructionsRect.topleft = (20, 200)

    instructionsSurf2 = titlefont.render('do not hit the falling bombs', True , DARKGRAY)
    instructions2Rect = instructionsSurf2.get_rect()
    instructions2Rect.topleft = (200, 300)

    DISPLAYSURF.blit(instructionsSurf2, instructions2Rect)
    DISPLAYSURF.blit(instructionsSurf, instructionsRect)


    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def lifeUpShow():
    titlefont = pygame.font.Font('freesansbold.ttf', 60)
    lifeUpSurf = titlefont.render('Life Up!', True, DARKGREEN)
    lifeUpRect = lifeUpSurf.get_rect()
    lifeUpRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    DISPLAYSURF.blit(lifeUpSurf, lifeUpRect)


def checkForKeyPress():


    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


if __name__ == '__main__': runGame()
