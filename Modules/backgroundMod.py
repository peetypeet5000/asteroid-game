import pygame, os, sys, random
from Modules import rock

class Background:
	def __init__(self, screen, mode, freq):
		self.bgs = [(pygame.image.load(os.path.join(sys.path[0], 'Resources\space.jpg')).convert()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\space2.jpg')).convert()),(pygame.image.load(os.path.join(sys.path[0], 'Resources\space3.jpg')).convert()),(pygame.image.load(os.path.join(sys.path[0], 'Resources\space4.jpg')).convert()),(pygame.image.load(os.path.join(sys.path[0], 'Resources\space5.jpg')).convert())]
		self.hyperspace = pygame.image.load(os.path.join(sys.path[0], 'Resources\hpy.png')).convert_alpha()
		self.warp_speed = pygame.mixer.Sound(os.path.join(sys.path[0], 'Resources\warp_speed.wav'))
		self.iterate = 0
		self.screen = screen
		self.mode = mode
		self.activeBG = self.bgs[self.iterate]
		self.freq = freq
		self.fade = 0
		self.alpha = 255
		self.fakeRocks = []
		self.rocks = -1
		self.time = pygame.time.get_ticks()
		
	def draw_background(self, difficulty):#blits active bg, once time is reached start trans to next bg
		now = pygame.time.get_ticks()
		self.screen.blit(self.activeBG, (0, 0))
		if (self.time + self.freq)  < now and self.iterate != 5 and self.mode == 0:
			self.transition(difficulty)
	
	def transition(self, difficulty):#the hyperspace transition, only trigger in classic mode
		if self.fade == 0:#for fade out
			self.alpha = self.alpha - 1
			self.activeBG.set_alpha(self.alpha)
			self.screen.blit(self.hyperspace, (550, 120))
			if self.alpha == 0:
				self.switch_background(difficulty)
				self.fade = 2
			elif self.alpha == 254:
				difficulty.switch_is_active(0)
		elif self.fade == 1:#for fade in
			self.rock_movement()
			self.alpha = self.alpha + 1
			self.activeBG.set_alpha(self.alpha)
			if self.alpha == 255:
				self.fade = 0
				self.delete_rocks()
				difficulty.switch_is_active(1)#calls difficulty funtion
				self.time = pygame.time.get_ticks()
				if self.iterate == 4:
					self.iterate = 5
		else:
			self.rock_transition()
		
	def switch_background(self, difficulty):#switches the actual bg photo
		if self.iterate < 3:
			self.iterate = self.iterate + 1	
		elif self.iterate == 3:
			self.iterate = self.iterate + 1
			difficulty.final()
		self.warp_speed.play()
		self.activeBG = self.bgs[self.iterate]
		self.activeBG.set_alpha(self.alpha)
		
	def rock_transition(self):#spawns rocks for the cool transition effect
		angle = random.randint(0, 360)
		self.fakeRocks.append(rock.Rock(10, angle, 6, True, self.screen))
		self.rocks = self.rocks + 1
		self.rock_movement()
		if self.rocks > 300:
			self.fade = 1
			
	def rock_movement(self):#makes the spawned rocks move
		slow = 1
		for i in range(self.rocks):
			self.fakeRocks[i].move(slow)
			self.fakeRocks[i].draw()
	
	def delete_rocks(self):
		del self.fakeRocks[:]
		self.rocks = -1