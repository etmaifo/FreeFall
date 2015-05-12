import pygame, os

pygame.init()


class GAME:
    fps = 30

class FilesPath(object):
	def __init__(self):
		self.path = ''

	def get_path(self, absolute_path, filename):
		return os.path.join(absolute_path, filename)

FILES = FilesPath()

class SCREEN:
    width = 192
    height = 288
    video_mode = pygame.display.set_mode((width, height))
    

class MENU:
    width = 180
    height = 288
    image = pygame.image.load(FILES.get_path("img", "gameover.png"))
    image = pygame.transform.smoothscale(image,(width, height))

class STATE:
    game = "game"
    menu = "menu"
    title_screen = "title_screen"
    pause = "pause"
    gameover = "game_over"
    start_game = "start_game"

class HUD:
    width = 190
    height = 288
    title = pygame.image.load(FILES.get_path("img", "gametitle.png"))
    title = pygame.transform.smoothscale(title, (153, 56))
    howtoplay = pygame.image.load(FILES.get_path("img", "howtoplay.png"))
    ripple = pygame.image.load(FILES.get_path("img", "ripple.png"))
    overlay = pygame.image.load(FILES.get_path("img", "overlay1.png"))


class BUTTON:
    width = 80
    height = 25
    retry = pygame.image.load(FILES.get_path("img", "retry_button.png"))
    retry_pressed = pygame.image.load(FILES.get_path("img", "retry_button_pressed.png"))
    quit = pygame.image.load(FILES.get_path("img", "quit_button.png"))
    quit_pressed = pygame.image.load(FILES.get_path("img", "quit_button_pressed.png"))


class BG:
    grid = pygame.image.load(FILES.get_path("img", "grid.png"))
    grid = pygame.transform.smoothscale(grid, (192, 422))
    image = pygame.image.load(FILES.get_path("img", "background.jpg"))



class COLOR:
    black = (0, 0, 0)
    gray = (128, 129, 129)
    dark_gray = (51, 51, 51)
    green = (129, 211, 5)
    purple = (153, 0, 153)
    white = (255, 255, 255)
    orange = (204, 51, 0)

class WORLD:
    gravity = 1

class POWERUP:
    slow = "slow"
    reverse = "reverse"
    immortal = "immortal"
    points = "points"
    normal  = "normal"

class PLAYER:
    speed = 10
    width = 32
    height = 32
    player_sprite = pygame.sprite.Sprite()
    #player_sprite.image = pygame.Surface((width, height)).convert()
    player_sprite.image = pygame.image.load(FILES.get_path("img", "blue_block.png"))
    #player_sprite.image.fill(COLOR.green)
    player_sprite.rect = player_sprite.image.get_rect()
    

class BLOCK:
    width = 32
    height = 32
    block_sprite = pygame.sprite.Sprite()
    #block_sprite.image = pygame.Surface((width, height)).convert()
    block_sprite.image = pygame.image.load(FILES.get_path("img", "orange_block.png"))
    #block_sprite.image.fill(COLOR.purple)
    block_sprite.rect = block_sprite.image.get_rect()

    immortal_image = pygame.image.load(FILES.get_path("img", "immortal.png"))
    time_image = pygame.image.load(FILES.get_path("img", "time.png"))
    reverse_image = pygame.image.load(FILES.get_path("img", "reverse.png"))
    points_image = pygame.image.load(FILES.get_path("img", "points.png"))
    normal_image =  pygame.image.load(FILES.get_path("img", "orange_block.png"))

    point_frames = [pygame.image.load(FILES.get_path("img", "point%d.png" %i)) for i in range(1, 6, 1)]




class DEBRIS:
    width = 8
    height = 8
    image = PLAYER.player_sprite.image
    image = pygame.transform.smoothscale(image, (width, height))
    rect = image.get_rect()

class RIPPLE:
    width = 8
    height = 8
    timeout = 6 #seconds
    scaleRate = 3
    img = pygame.image.load(FILES.get_path("img", "ripple.png"))


class Asset(object):
    def __init__(self):
        self.name = "assets"

    
    def get_image(self, asset):
        if asset == 'player':
            return PLAYER.player_sprite.image

        elif asset == 'block':
            return BLOCK.block_sprite.image

        elif asset == 'grid':
            return pygame.image.load(FILES.get_path("img", "grid.png"))

        elif asset == 'hud':
            image = pygame.image.load(FILES.get_path("img", "gametitle.png"))
            image = pygame.transform.smoothscale(image, (HUD.width, HUD.height))
            return image