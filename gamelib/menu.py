import pygame
from pygame.locals import *
from constants import *
from asset import *
from worldobject import *

class Menu(object):
    def __init__(self, x, y, width, height):
        self.score = GameText("hoog0553.ttf", 24, COLOR.gray)
        self.score.set_bold(True)


    def update(self, score):
        self.score.update(str(score), SCREEN.width/2, BLOCK.height/4)


    def draw(self, screen):
        screen.blit(self.score.text, self.score.rect)


class GameOverScreen(object):
    def __init__(self, x, y, width, height):
        self.bg = BgObject(0, 0, MENU.width, MENU.height, MENU.image)
        self.retry_button = WorldObject(0, 0, BUTTON.width, BUTTON.height, BUTTON.retry)
        self.quit_button = WorldObject(0, 0, BUTTON.width, BUTTON.height, BUTTON.quit)
        self.score_label = GameText("hoog0553.ttf", 14, COLOR.dark_gray)
        self.score = GameText("hoog0553.ttf", 14, COLOR.gray)
        self.best_label = GameText("hoog0553.ttf", 14, COLOR.dark_gray)
        self.best = GameText("hoog0553.ttf", 14, COLOR.gray)
        self.retries_label = GameText("hoog0553.ttf", 14, COLOR.dark_gray)
        self.retries = GameText("hoog0553.ttf", 14, COLOR.gray)

        self.retry = False
        self.quit = False
        
        self.gameover_group = pygame.sprite.OrderedUpdates()
        self.font_group = []
        self.assemble()


    def handleEvents(self, event):
        if (event.type == MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            if self.retry_button.rect.collidepoint(pos):
                self.retry = True
            elif self.quit_button.rect.collidepoint(pos):
                self.quit = True

    def set_positions(self):
        self.bg.rect.centerx = SCREEN.width/2
        menuRect = self.bg.rect

        self.score_label.rect.x = 10
        self.score_label.rect.y = menuRect.y + 100
        self.score.rect.right = menuRect.right - 10
        self.score.rect.y = menuRect.y + 100

        self.best_label.rect.x = 10
        self.best_label.rect.y = menuRect.y + 120
        self.best.rect.right = menuRect.right - 10
        self.best.rect.y = menuRect.y + 120

        self.retries_label.rect.x =  10
        self.retries_label.rect.y = menuRect.y + 140
        self.retries.rect.right = menuRect.right - 10
        self.retries.rect.y = menuRect.y + 140

        self.retry_button.rect.left = 10
        self.retry_button.rect.bottom = menuRect.bottom - 15
        self.quit_button.rect.right = menuRect.right - 10
        self.quit_button.rect.bottom = menuRect.bottom - 15

    def assemble(self):
        self.bg.rect.bottom = 0
        self.set_positions()

        self.score_label.set_bold(True)
        self.best_label.set_bold(True)
        self.retries_label.set_bold(True)

        self.gameover_group.add(self.bg)
        self.gameover_group.add(self.retry_button)
        self.gameover_group.add(self.quit_button)
        self.font_group.append(self.score_label)
        self.font_group.append(self.score)
        self.font_group.append(self.best_label)
        self.font_group.append(self.best)
        self.font_group.append(self.retries_label)
        self.font_group.append(self.retries)


    def update(self, score, best, retries):        
        self.gameover_group.update()
        
        self.score_label.update("Score", self.score_label.rect.x, self.score_label.rect.y)
        self.score.update(score, self.score.rect.x, self.score.rect.y)
        self.best_label.update("Best", self.best_label.rect.x, self.best_label.rect.y)
        self.best.update(best, self.best.rect.x, self.best.rect.y)
        self.retries_label.update("Retries", self.retries_label.rect.x, self.retries_label.rect.y)
        self.retries.update(retries, self.retries.rect.x, self.retries.rect.y)

        self.set_positions()
        

        
    def draw(self, screen):
        for entity in self.gameover_group:
            screen.blit(entity.image, entity.rect)
        for font in self.font_group:
            screen.blit(font.text, font.rect)

    def show(self):
        if self.bg.rect.y < 0:
            for entity in self.gameover_group:
                entity.rect.y += 10
            for font in self.font_group:
                font.rect.y += 10
        else:
            self.bg.rect.y = 0

    def hide(self):
        if self.bg.rect.y >= 0:
            for entity in self.gameover_group:
                entity.rect.y -= 10
            for font in self.font_group:
                font.rect.y -= 10
        