import pygame
from worldobject import *
from constants import *

class Stage(object):
    def __init__(self, player):
        self.player = player
        self.level = 2
        self.entities = pygame.sprite.RenderUpdates()
        self.grid = []
        self.level_speed = 4
        self.level_blocks = 2
        self.enemy = Enemy(self.level_blocks, self.level_speed)
        self.reset = False
        self.bonus_points = 0
        self.bonus_total = 0
        
        self.assemble()

    def update(self, score):
        self.enemy.update()
        self.updateLevel(score)
        if self.enemy.hide:
            self.entities.remove(self.enemy.blocks)
            self.enemy = Enemy(self.level_blocks, self.level_speed, True)
            self.entities.add(self.enemy.blocks)
            self.player.collision_group.add(self.enemy.blocks)
            self.player.points_group.add(self.enemy.blocks)
            for block in self.enemy.blocks:
                if not block.deadly:
                    self.player.collision_group.remove(block)
                    self.player.points_group.remove(block)
                    self.player.powerup_group.add(block)
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
        self.player.points_group.add(self.enemy.blocks)
        self.entities.add(self.enemy.blocks)

        for block in self.enemy.blocks:
            if not block.deadly:
                self.player.collision_group.remove(block)
                self.player.points_group.remove(block)
                self.player.powerup_group.add(block)


    def restart(self):
        self.reset = True

    def spawn(self):
        self.blocks = ChainBlock(4)
        
    def updateLevel(self, score):
        if score < 10:
            self.level_speed = 4
        elif score < 50:
            self.level_blocks = 3
        elif score < 100:
            self.level_speed = 5
        elif score < 130:
            self.level_blocks = 4
        elif score < 150:
            self.level_speed = 6
        elif score < 200:
            self.level_blocks = 5
        elif score < 500:
            self.level_speed = 7
        elif score < 550:
            self.level_speed = 8
        elif score < 600:
            self.level_speed = 9
        elif score < 1001:
            self.level_speed = 10