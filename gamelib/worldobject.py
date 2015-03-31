import pygame
from constants import *
from random import randrange, choice



class WorldObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.vspeed = 0
        self.hspeed = 0				



    def update(self):
        pass


    def handleEvents(self):
        pass


    def draw(self):
        pass

    def reset_rect(self):
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height


class HudObject(WorldObject):
    def __init__(self, x, y, width, height, image):
        WorldObject.__init__(self, x, y, width, height, image)
        self.counter = 0
        self.scale = RIPPLE.scaleRate
        self.visible = False
        self.pos = [0, 0]

    def handleEvents(self, event, grid):
        self.counter = 0
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.image = pygame.transform.smoothscale(RIPPLE.img, (RIPPLE.width, RIPPLE.height))
            self.reset_rect()
            for cell in grid:
                if cell.rect.collidepoint(pos):
                    self.rect.centerx = cell.rect.centerx
                    self.rect.centery = cell.rect.centery
                    self.pos[0] = cell.rect.centerx
                    self.pos[1] = cell.rect.centery


    def animate_ripple(self, timeout):
        self.counter += 1
        scale = ""
        if self.counter < timeout:
            self.visible = True
            scale = (self.width + self.scale, self.height + self.scale)
            self.image = pygame.transform.smoothscale(RIPPLE.img, scale)
            #self.rect = self.image.get_rect()
            self.reset_rect()
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]
        else:
            self.visible = False

    def update(self):
        self.animate_ripple(RIPPLE.timeout)
        #self.visible = True

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
            #print self.rect



class BgObject(WorldObject):
    def __init__(self, x, y, width, height, image):
        WorldObject.__init__(self, x, y, width, height, image)


    def update(self):
        pass


class Moveable(WorldObject):
	def __init__(self, x, y, width, height, image):
		WorldObject.__init__(self, x, y, width, height, image)

		self.assets = ""
		self.scanned_frame = 0
		self.distance_moved = 0
		self.jumping = False
		self.direction = 'right'
		self.idle = True	

		self.collision_group = pygame.sprite.Group()


	def update(self):
		pass

	def move(self, dx, dy):
		if dx != 0:
			self.detect_collision(dx, 0)
		if dy != 0:
			self.detect_collision(0, dy)


	def detect_collision(self, dx, dy):
		tempRect = pygame.Rect(self.rect)
		tempRect.x += dx
		tempRect.y += dy

		for sprite in self.collision_group:
			if tempRect.colliderect(sprite.rect):
				# Check x-axis
				self.rect.x += sprite.hspeed
				if dx > 0 and sprite.vspeed == 0:
					self.rect.right = sprite.rect.left
				elif dx < 0 and sprite.vspeed == 0:
					self.rect.left = sprite.rect.right

				# Check y-axis
				if dy > 0:
					self.rect.bottom = sprite.rect.top
					self.rect.y += sprite.vspeed

					# Land on something
					self.vspeed = 0

				elif dy < 0:
					self.rect.top = sprite.rect.bottom
					self.vspeed = 0

				return

		self.rect = pygame.Rect(tempRect)


	def reset_rect(self):
		self.rect.width = self.image.get_rect()[2]
		self.rect.height = self.image.get_rect()[3]


	def get_distance(self, frames):
		pass

		#return self.distance_moved


	def animate_movement(self, frames, direction):
		self.get_distance(frames)
		if self.jumping:
			self.image = self.frames[0]
			if direction == 'left':
				self.image = pygame.transform.flip(self.image, True, False)
				self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

			self.image = pygame.transform.smoothscale(self.image, (self.width, self.height)) 
		else:
			if self.scanned_frame >= len(frames):
				self.scanned_frame = 0

			if direction == 'left':
				self.image = frames[self.scanned_frame]
				self.image = pygame.transform.flip(self.image, True, False)
				self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
			elif direction == 'right':
				self.image = frames[self.scanned_frame]
				self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))

			self.scanned_frame += 1
				

	def animate_idle(self, direction):
		if self.scanned_frame >= len(self.idle_frames):
			self.scanned_frame = 0

		self.image = self.idle_frames[self.scanned_frame]
		self.scanned_frame += 1

		if self.direction == 'left':
			self.image = pygame.transform.flip(self.image, True, False)
		
		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
		self.reset_rect()

	def animate_jump(self, direction):
		self.get_jump_image()
		if self.direction == 'left':
			self.image = pygame.transform.flip(self.image, True, False)

		self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))


	def load_frames(self):
		self.frames = self.assets.get_walk_frames(self.color_code)


	def load_idle_frames(self):
		self.idle_frames = self.assets.get_idle_frames(self.color_code)


	def load_jump_image(self):
		self.jump_frames = self.assets.get_jump_frames(self.color_code)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((width, height))
        self.image = image
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hspeed = 0
        self.vspeed = 0
        self.givePoint = True

    def update(self):
        self.rect.y -= self.vspeed


    def get_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()


class Particle(Block):
    def __init__(self, x, y, width, height, image):
        Block.__init__(self, x, y, width, height, image)
        self.image = pygame.transform.smoothscale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vspeed = randrange(-13, -3)
        self.hspeed = randrange(-3, 4, 1)
        

    def update(self):
        self.vspeed += 0.5 #WORLD.gravity        

        self.rect.x += self.hspeed
        self.rect.y += self.vspeed

class Debris(object):
    def __init__(self, x, y):
        self.particles = pygame.sprite.RenderUpdates()
        self.x = x
        self.y = y
        self.spawned = False

    def spawn(self, number):
        self.particles.empty()
        for i in xrange(number):
            particle = Particle(self.x, self.y, DEBRIS.width, DEBRIS.height, DEBRIS.image)
            self.particles.add(particle)
           

    def update(self):
        self.particles.update()

    def draw(self, screen):
        self.particles.draw(screen)


class Enemy(object):
    def __init__(self, number):
        self.number = number
        self.blocks = pygame.sprite.RenderUpdates()
        self.givePoint = True
        self.hide = False

        self.spawn(4)

    def spawn(self, speed):
        randomNumbers = [i for i in range(6)]
        for i in range(self.number):
            mult = choice(randomNumbers)        
            block = Block(mult*BLOCK.width, SCREEN.height, BLOCK.width, BLOCK.height, BLOCK.block_sprite.image)
            block.vspeed = speed
            randomNumbers.remove(mult)
            self.blocks.add(block)

    def update(self):
        for block in self.blocks:
            block.update()
            
            if block.rect.y < -BLOCK.height:
                block.kill()
                self.hide = True


   
