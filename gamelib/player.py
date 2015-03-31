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
        self.dead = False
        self.debris = Debris(self.rect.x, self.rect.y)
        self.debris.spawn(25)


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

            self.detect_collision()
            self.detect_point()

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
            self.detect_collision(dx, 0)
        if dy != 0:
            self.detect_collision(0, dy)

    def detect_collision(self):
        tempRect = pygame.Rect(self.rect)
        for sprite in self.collision_group:
            if tempRect.colliderect(sprite.rect):
                self.collided = True

                return

        self.rect = pygame.Rect(tempRect)

    def detect_point(self):
        temprect = pygame.Rect(self.rect)
        for sprite in self.collision_group:
            if sprite.rect.bottom <= temprect.bottom:
                if sprite.givePoint:
                    self.receivePoint = True
                    sprite.givePoint = False
                return