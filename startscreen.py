import random  
import pygame  
import sys  
from pygame.locals import *



Window_Width = 900  
Window_Height = 600
White = (255, 255, 255)  
Black = (0, 0, 0)  
Red = (255, 0, 0)   
Green = (0, 255, 0)  
DARKGreen = (0, 155, 0)  
DARKGRAY = (40, 40, 40)     
YELLOW = (255, 255, 0)  
Red_DARK = (150, 0, 0)  
BLUE = (0, 0, 255)  
BLUE_DARK = (0, 0, 150)  
  
  
BGCOLOR = White  

def checkForKeyPress():  
    if len(pygame.event.get(QUIT)) > 0:  
        terminate()  
    keyUpEvents = pygame.event.get(KEYUP)  
    if len(keyUpEvents) == 0:  
        return None  
    if keyUpEvents[0].key == K_ESCAPE:  
        terminate()  
    return keyUpEvents[0].key

def terminate():  
    pygame.quit()  
    sys.exit()

def showStartScreen():
    __screen_size = (900, 600) 
    screen=pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    icon=pygame.image.load('pic2/bg.jpg').convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('消消乐')      
    background=pygame.image.load("pic2/bg.jpg").convert_alpha()
    screen.blit(background,(0,0))
    pygame.display.update()
    while True:
     if checkForKeyPress():  
            pygame.event.get()  
            return  
     pygame.display.update()  

def introduceScreen():
    __screen_size = (900, 600) 
    screen=pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    icon=pygame.image.load('pic2/rules.jpg').convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('消消乐')      
    background=pygame.image.load("pic2/rules.jpg").convert_alpha()
    screen.blit(background,(0,0))
    pygame.display.update()
    while True:
     if checkForKeyPress():  
            pygame.event.get()  
            return  
     pygame.display.update()  
