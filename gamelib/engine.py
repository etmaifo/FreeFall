import pygame, sys
from pygame.locals import *
from constants import *
from stage import *
from player import *
from hud import *
from menu import *
from worldobject import *


try:
    import android
except ImportError:
    android = None

# Load assets once
assets = Asset()
player_image = assets.get_image("player")
block_image = assets.get_image("block")
grid_image = assets.get_image("grid")
bg = BG.grid
hud_image = assets.get_image("hud")

player = Player(PLAYER.width*2, BLOCK.height*2, PLAYER.width, PLAYER.height, player_image)

class GameEngine(object):
    def __init__(self, width, height):
        pygame.init()
        pygame.font.init()
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)

        self.width = width
        self.height = height
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.display.set_caption("Freefall")
        self.screen = SCREEN.video_mode
        #self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | FULLSCREEN)

        self.fpsClock = pygame.time.Clock()
        self.state = STATE.title_screen
        self.score = 0
        self.best = 0
        self.retries = 0
        self.avg = 0
        self.total = 0

        #self.bg = grid_image
        self.bg = bg

        self.stage = Stage(player)
        self.hud = Hud(0, 0, HUD.width, HUD.height)
        self.menu = Menu(0, 0, SCREEN.width, SCREEN.height)
        self.gameover = GameOverScreen(0, 0, MENU.width, MENU.height)
        self.ripple = HudObject(64, 120, RIPPLE.width, RIPPLE.height, HUD.ripple)        
        self.overlay = Overlay(0, 0, SCREEN.width/2, SCREEN.height, HUD.overlay)
        


    def reset(self):
        player = Player(PLAYER.width*2, BLOCK.height*2, PLAYER.width, PLAYER.height, player_image)
        self.best = self.getBestScore()
        self.score = 0
        self.retries += 1
        self.stage = Stage(player)
        self.hud = Hud(0, 0, HUD.width, HUD.height)
        self.menu = Menu(0, 0, SCREEN.width, SCREEN.height)
        self.gameover = GameOverScreen(0, 0, MENU.width, MENU.height)
        self.ripple = HudObject(64, 120, RIPPLE.width, RIPPLE.height, RIPPLE.img)

        self.state = STATE.title_screen
        
 

    def handleEvents(self):
        if android:
            if android.check_pause():
                android.wait_for_resume()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_q:
                pygame.image.save(self.screen, FILES.get_path("screenshots", "screen01.jpg"))
            
            if self.state == STATE.game:
                self.stage.player.handleEvents(event, self.stage.grid)
                self.overlay.handleEvents(event)

            if self.state == STATE.title_screen:
                self.hud.handleEvents(event)
            if self.state == STATE.gameover:
                self.gameover.handleEvents(event)
                if self.gameover.retry:
                    self.reset()
                elif self.gameover.quit:
                    pygame.quit()
                    sys.exit()
        if self.hud.active:
            self.state = STATE.title_screen       
        else:
            self.state = STATE.game


    def update(self):     
        if self.stage.reset:
            self.state = STATE.gameover
            self.gameover.show()
            if self.retries == 0:
                self.avg = self.score
            else:
                self.avg = self.getAverageScore()
            self.best = self.getBestScore()   
            self.gameover.update(self.score, self.best, self.retries, self.avg)         
            return
        if self.state != STATE.gameover:
            self.state = self.hud.state
        if self.state == STATE.game:
            #self.menu.update(self.score)
            self.overlay.update()
            self.stage.update(self.score)
            self.stage.player.checkBounds(self.width)
            if self.stage.player.receivePoint:
                self.score += 1
                self.total += 1
                self.stage.player.receivePoint = False

            self.menu.update(self.score)
            self.ripple.update()

        elif self.state == STATE.start_game or self.state == STATE.title_screen:
            self.hud.update()
        

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.bg, self.screen.get_rect())
        if self.state == STATE.title_screen:
            self.hud.draw(self.screen)
            self.hud.show()
        elif self.state == STATE.start_game:
            self.hud.draw(self.screen)
            self.hud.hide()
        elif self.state == STATE.game:  
            self.overlay.draw(self.screen)  
            self.stage.draw(self.screen)
            self.menu.draw(self.screen)
            self.hud.draw(self.screen)            
        elif self.state == STATE.gameover:
            self.gameover.draw(self.screen)
        

    def getBestScore(self):
        if self.best < self.score:
            self.best = self.score
        return self.best

    def getAverageScore(self):
        avg = int(round(self.total/float(self.retries + 1))) # divide by replays
        return avg

    def runGame(self, fps):
        self.fps = fps
        while True:
            self.handleEvents()
            self.update()
            self.draw()
        
            pygame.display.update()
            pygame.display.set_caption("FPS:" + str(int(self.fpsClock.get_fps())))
            self.fpsClock.tick(self.fps)