import random
import sys
import pygame
from pygame.locals import *

# Global Variables For Game
FPS = 40
SCREENWIDTH = 289
SCREEHEIGHTT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREEHEIGHTT))
GROUNDY = SCREEHEIGHTT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen() :
    """
    welcom image for game
    """
    playerx = int(SCREENWIDTH / 6)
    playery = int((SCREEHEIGHTT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREEHEIGHTT * 0.5)
    basex = 0
    while(True) :
        for event in pygame.event.get() :

            # for quiting game 

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()

            # to start game

            elif(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) :
                return

            else :
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

        



def mainScreen() :
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREEHEIGHTT / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x' : SCREENWIDTH + 200, 'y' : newPipe1[0]['y']},
        {'x' : SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y' : newPipe2[0]['y']}
    ]

    lowerPipes = [
       {'x' : SCREENWIDTH + 200, 'y' : newPipe1[1]['y']},
       {'x' : SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y' : newPipe2[1]['y']}
    ]

    pipVelX = -4
    playerVely = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapvel = -8
    playerFlapped = False

    while True : 
        for event in pygame.event.get() :
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()
            
            elif(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) :
                if playery > 0 :
                    playerVely = playerFlapvel
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if(crashTest) :
            return

        playerMidPos = playerx + (GAME_SPRITES['player'].get_width() / 2)
        for pipe in upperPipes :
            pipeMidPos = pipe['x'] + (GAME_SPRITES['pipe'][0].get_width() / 2)

            if pipeMidPos <= playerMidPos <= pipeMidPos + 4 :
                score += 1
                print(f"score is {score}")
                GAME_SOUNDS['point'].play()
        
        if playerVely < playerMaxVelY and not playerFlapped:
            playerVely += playerAccY
        
        if playerFlapped :
            playerFlapped = False
        
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playerHeight - playery)
        # playery = playery + 10


        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes) :
            upperPipe['x'] += pipVelX
            lowerPipe['x'] += pipVelX

        if 0 < upperPipes[0]['x'] < 5 :
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width() :
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes) :
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits :
            width += GAME_SPRITES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits :
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREEHEIGHTT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes) :
    if playery > GROUNDY - 25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe() :
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEHEIGHTT / 3
    y2 = offset + random.randrange(0, int(SCREEHEIGHTT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x' : pipex, 'y' : -y1}, # upper Pipe
        {'x' : pipex, 'y' : y2} # lower Pipe
    ]

    return pipe


if __name__ == "__main__" :
    successes, failures = pygame.init()
    print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))    
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Monster')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()    
    )

    # GAME IAMGES 
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha() 
    )

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # GAME SOUNDS

    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


    while(True) :
        welcomeScreen()
        mainScreen()




