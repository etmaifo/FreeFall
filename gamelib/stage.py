import pygame
from worldobject import *
from constants import *

class Stage(object):
    def __init__(self, player):
        self.player = player
        self.level = 2
        self.entities = pygame.sprite.RenderUpdates()
        self.grid = []
        self.enemy = Enemy(2)
        self.reset = False
        
        self.assemble()

    def update(self):
        self.enemy.update()
        if self.enemy.hide:
            self.entities.remove(self.enemy.blocks)
            self.enemy = Enemy(2)
            self.entities.add(self.enemy.blocks)
            self.player.collision_group.add(self.enemy.blocks)
        if self.player.collided:
            self.entities.remove(self.player)
            self.entities.add(self.player.debris.particles)
            self.player.animate_death()
            if self.player.dead:
                self.restart()
                self.player.collided = False
            return

        self.entities.update()

    def draw(self, screen):
        self.entities.draw(screen)


    def assemble(self):        
        self.entities.add(self.player)
        self.player.collision_group.add(self.enemy.blocks)
        self.entities.add(self.enemy.blocks)


    def restart(self):
        self.reset = True

    def spawn(self):
        self.blocks = ChainBlock(4)
        