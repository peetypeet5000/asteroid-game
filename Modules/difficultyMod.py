import pygame, os, sys

class Difficulty:
	def __init__(self):
		self.level = 1
		self.active = 1
		self.isFinal = 0
		self.clock = 0
		self.clockBase = 0
		self.rockFreq = 5000
		
	def switch_is_active(self, num):#function to set gameActive true or false
		self.active = num
		if num == 1:
			self.level_up()
			
	def level_up(self):#if called, simply advances level
		self.level = self.level + 1
			
	def get_active(self):
		return self.active
	
	def adjusted_rock_freq(self):
		self.clock = pygame.time.get_ticks()
		if self.level == 4 and self.isFinal == 0:
			self.clockBase = pygame.time.get_ticks()
		elif self.level == 5 and self.isFinal == 1:
			timeChange = (self.clock - self.clockBase) / 200 
			self.rockFreq = 100 - timeChange
			if self.rockFreq <= 0:
				self.rockFreq = 1
		else:
			self.rockFreq = 5000 / (self.level)
		#print(self.rockFreq)
		return self.rockFreq
	
	def final(self):
		self.adjusted_rock_freq()
		if self.isFinal == 0:
			music = pygame.mixer.music.load(os.path.join(sys.path[0], 'Resources\music2.mp3'))
			pygame.mixer.music.play(loops=-1)
			self.isFinal = 1