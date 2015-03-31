import pygame
from constants import *


class GameText(object):
    def __init__(self, font, size, color):
        self.font = pygame.font.Font(FILES.get_path("fonts", font), size)     
        self.bold = False
        self.text = self.font.render("0", True, COLOR.gray) 
        self.rect = self.text.get_rect()
        self.color = color


    def update(self, text, x, y):
        self.text = self.font.render(str(text), True, self.color)
        self.rect = self.text.get_rect()
        self.rect.centerx = x
        self.rect.y = y


    def set_bold(self, bold):
        self.font.set_bold(bold)
           