# author: Tokelo Maifo
# email : et.maifo@phyrebotcentral.com
# date  : 

import pygame
from pygame.locals import *  
from worldobject import *
from constants import *


class Player(Moveable):
    def __init__(self, x, y, width, height, image):
        Moveable.__init__(self, x, y, width, height, image)
        self.target_pos = BLOCK.width/2
        self.receivePoint = False
        self.collided = False
        self.timeout = 0
        self.power_timer = 0
        self.bonus_points = 0
        self.power = POWERUP.normal
        self.dead = False
        self.debris = Debris(self.rect.x, self.rect.y)
        self.debris.spawn(25)
        self.powerup_group = pygame.sprite.RenderUpdates()
        self.points_group = pygame.sprite.Group()
        self.temp_group = pygame.sprite.Group()


    def handleEvents(self, event, grid):
        if not self.collided:
            if event.type == KEYUP:
                if event.key == K_a:
                    self.hspeed = 0
                elif event.key == K_d:
                    self.hspeed = 0

            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > SCREEN.width/2:                    
                    self.rect.x += BLOCK.width #self.rect.x = self.rect.x + BLOCK.width    
                    for particle in self.debris.particles:
                        particle.rect.x = self.rect.x + BLOCK.width/2  
                else:
                    self.rect.x -= BLOCK.width
                    for particle in self.debris.particles:
                        particle.rect.x = self.rect.x + BLOCK.width/2


    def update(self):
        if self.collided:
            self.animate_death()
        else:
            key = pygame.key.get_pressed()
            if key[K_a]:
                self.hspeed = -PLAYER.speed
            elif key[K_d]:
                self.hspeed = PLAYER.speed

            self.detectCollision()
            self.detectPowerup()                        
            self.detectPoint()
            self.consumePower()


    def animate_death(self):
        self.timeout += 1
        self.debris.update()
        if self.timeout >= 2*GAME.fps:
            self.dead = True


    def checkBounds(self, width):
        if self.rect.left < 0:
            self.rect.x = 0
        elif self.rect.right > width:
            self.rect.right = width


    def move(self, dx, dy):
        if dx != 0:
            self.detectCollision(dx, 0)
        if dy != 0:
            self.detectCollision(0, dy)


    def detectCollision(self):
        tempRect = pygame.Rect(self.rect)
        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                self.collided = True

                return

        self.rect = pygame.Rect(tempRect)


    def detectPowerup(self):
        tempRect = pygame.Rect(self.rect)
        for sprite in self.powerup_group:
            if tempRect.colliderect(sprite.rect):
                self.powered = True
                self.power = sprite.power
                self.power_timer = 0
                sprite.kill()
                return
        self.rect = pygame.Rect(tempRect)


    def detectPoint(self):
        temprect = pygame.Rect(self.rect)
        for sprite in self.points_group:
            if sprite.rect.bottom <= temprect.bottom:
                if sprite.givePoint:
                    self.receivePoint = True
                    sprite.givePoint = False
                return


    def consumePower(self):
        if self.power == POWERUP.immortal:
            self.temp_group = self.collision_group.copy()
            self.collision_group.empty()
            self.power_timer += 1
            if self.power_timer >= 4*GAME.fps:
                self.power_timer = 0
                self.power = POWERUP.normal

        elif self.power == POWERUP.points:
            self.power_timer += 1
            bonus = [2, 3, 5, 15]
            self.bonus_points = choice(bonus)
            self.receivePoint = True
            if self.power_timer >= self.bonus_points:
                self.power_timer = 0
                self.bonus_points = 0
                self.receivePoint = False
                self.power = POWERUP.normal                              