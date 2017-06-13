#!/usr/bin/env python3
'''
Documentation, License etc.

@package pong
'''


import sys, pygame, math
from math import pi as pi
import time

pygame.init()
pygame.font.init()


size = screenWidth, screenHeight = 1280, 720
screen = pygame.display.set_mode(size)
black = 0,0,0
playerScore = 0
cpuScore = 0

def signof(x):
    if x >= 0:
        return 1
    else:
        return -1



class Paddle:

    def __init__(self, prectangle):
        self.color = pygame.Color(255, 255, 255, 255)
        self.rectangle = prectangle
        self.speed = [0, 0]
    
    def move(self):
        self.rectangle = self.rectangle.move(self.speed)
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > screenWidth:
            self.rectangle.right = screenWidth
        
    
class Ball:
    def __init__(self, px, py, pradius, pcolor):
        self.x = int(px)
        self.y = int(py)
        self.radius = pradius
        self.color = pcolor
        self.speed = [-2, -1]
        
        
    def move(self):
        
        if self.left() < 0 or self.right() > screenWidth:
            self.speed[0] *= -1
        self.x += self.speed[0]
        self.y += self.speed[1]
        
        

    def top(self):
        return self.y - self.radius
    def left(self):
        return self.x - self.radius
    def right(self):
        return self.x + self.radius
    def bottom(self):
        return self.y + self.radius




maxPaddleSpeed = 2
    


paddleWidth = int( screenWidth / 6.4)
paddleHeight = int( screenHeight / 72)
paddleEdgeThick = int( screenHeight / 72)

playerPaddle = Paddle(
    pygame.Rect( 
        
    (screenWidth / 2) - paddleWidth / 2, 
    
    screenHeight - paddleHeight - (0.05 * screenHeight),
    
    paddleWidth, 
    
    paddleHeight
    )
)


cpuPaddle = Paddle(
    pygame.Rect( 
        
    (screenWidth / 2) - paddleWidth / 2, 
    
    0.05 * screenHeight,
    
    paddleWidth, 
    
    paddleHeight
    )
)

radiusb = 10
balli = Ball(
            int ( screenWidth / 2),
            playerPaddle.rectangle.top - radiusb, 
            radiusb, pygame.Color(255, 255, 255, 255)
)


scoreFontSize = 60
playerScoreRect = pygame.Rect(0.9 * screenWidth, 0.9 * screenHeight, 0.1 * screenWidth, 1.1 * scoreFontSize) 
cpuScoreRect = pygame.Rect( 0.9 * screenWidth, 0.1 * screenHeight - 1.1 * scoreFontSize, 0.1 * screenWidth, 1.1 * scoreFontSize)
inputTimer = time.time()


def resetGame(lastWin):
    playerPaddle.__init__(
    pygame.Rect( 
        
    (screenWidth / 2) - paddleWidth / 2, 
    
    screenHeight - paddleHeight - (0.05 * screenHeight)  ,
    
    paddleWidth, 
    
    paddleHeight
    )
        
    )
    cpuPaddle.__init__(
    pygame.Rect( 
        
    (screenWidth / 2) - paddleWidth / 2, 
    
    0.05 * screenHeight  ,
    
    paddleWidth, 
    
    paddleHeight
    )
        
    )
    
    if lastWin == "player":
        balli.__init__(
            int ( screenWidth / 2),
            int( playerPaddle.rectangle.top - radiusb), 
            radiusb, pygame.Color(255, 255, 255, 255)
        )
    else:
        balli.x = int( screenWidth / 2)
        balli.y = int( cpuPaddle.rectangle.bottom + balli.radius)
        balli.speed = [-2, 1]






while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
    
    
    
    if balli.top() <= 0:
            playerScore += 1
            resetGame("player")
            
    
    if balli.bottom() >= screenHeight:
            cpuScore += 1
            resetGame("cpu")
            
            
    keyboard = pygame.key.get_pressed()
    if keyboard[pygame.K_LEFT]:
        
        playerPaddle.speed[0] = -2
        inputTimer = time.time()
    elif keyboard[pygame.K_RIGHT]:
        playerPaddle.speed[0] = 2
        inputTimer = time.time()
    else:
        if time.time() - inputTimer > 0.1:
            playerPaddle.speed[0] = 0
    
    if balli.speed[1] < 0:  #ai will act
        sep = balli.x - (cpuPaddle.rectangle.left + cpuPaddle.rectangle.right) / 2
        cpuPaddle.speed[0] = 2 * signof(sep)
    else:
        cpuPaddle.speed[0] = 0
 
    
    
      
    if(
        0 < cpuPaddle.rectangle.bottom - balli.top() < paddleHeight
        and 
        cpuPaddle.rectangle.left < balli.x < cpuPaddle.rectangle.right
    ):
          #balli.speed[0] += cpuPaddle.speed[0]
          balli.speed[1] *= -1
            
    
     
    if(  
        0 < balli.bottom() - playerPaddle.rectangle.top < paddleHeight 
        and 
        playerPaddle.rectangle.left < balli.x < playerPaddle.rectangle.right
    ):
        #balli.speed[0] += playerPaddle.speed[0]
        balli.speed[1] *= -1
        

 

    playerPaddle.move()    
    balli.move()
    cpuPaddle.move()
    
    
    
    screen.fill(black)
    pygame.draw.rect(screen, playerPaddle.color, playerPaddle.rectangle, paddleEdgeThick)
    pygame.draw.rect(screen, cpuPaddle.color, cpuPaddle.rectangle, paddleEdgeThick)
    pygame.draw.circle(screen, balli.color, (balli.x, balli.y), balli.radius, 0)
    
    
    
    playerScoreSurface = pygame.font.Font(None, scoreFontSize).render(str(playerScore), True, (255, 255, 255) )
    screen.blit(playerScoreSurface, playerScoreRect)
    
    cpuScoreSurface = pygame.font.Font(None, scoreFontSize).render(str(cpuScore), True, (255, 255, 255) )
    screen.blit(cpuScoreSurface, cpuScoreRect)

    pygame.display.flip()
    
    
