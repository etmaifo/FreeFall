import pygame
from gamelib import engine 

def main():
    pygame.init()
    gameEngine = engine.GameEngine(192, 288)
    gameEngine.runGame(30)


if __name__ == '__main__':
    main()
