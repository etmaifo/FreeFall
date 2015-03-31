import pygame
from pygame.locals import *
from constants import *
from worldobject import *

class Hud(object):
    def __init__(self, x, y, width, height):
        self.title = WorldObject(20, 0, 154, 46, HUD.title)
        self.howtoplay = WorldObject(HUD.width - 40, HUD.height - 59, 85, 33, HUD.howtoplay)
        self.ripple = WorldObject(64, 120, RIPPLE.width, RIPPLE.height, HUD.ripple)
        self.rect = pygame.Rect(0, 0, HUD.width, HUD.height)
        

        self.active = True
        self.state = STATE.title_screen

        self.assemble()


    def draw(self, screen):
        screen.blit(self.title.image, self.title.rect)
        screen.blit(self.howtoplay.image, self.howtoplay.rect)
        #screen.blit(self.ripple.image, self.ripple.rect)


    def assemble(self):
        self.howtoplay.rect.bottom = HUD.height
        self.howtoplay.rect.y -= 20
        self.howtoplay.rect.left = HUD.width
        
        self.title.rect.bottom = 0


    def handleEvents(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.state = STATE.start_game

            
    
    def update(self):
        self.howtoplay.rect.x += self.howtoplay.hspeed
        self.title.rect.y += self.title.vspeed


    def show(self):
        #self.ad.vspeed = -6
        self.howtoplay.hspeed = -6
        self.title.vspeed = 6

        if self.howtoplay.rect.right <= HUD.width:
            self.howtoplay.rect.right = HUD.width
        if self.title.rect.top >= 0:
            self.title.rect.top = 0


    def hide(self):
        #self.ad.vspeed = 6
        self.howtoplay.hspeed = -9
        self.title.vspeed = -6
        if self.howtoplay.rect.right <= 0:
            self.howtoplay.hspeed = 0
            self.howtoplay.rect.right = 0
            
            self.state = STATE.game
