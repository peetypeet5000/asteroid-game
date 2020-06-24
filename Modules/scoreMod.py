import pygame, os, sys

class Score:
	def __init__(self, screen, mode):
		self.svalue = 0
		self.isDead = 0
		self.rocks = 0
		self.extra = 0
		self.level = 1
		self.mode = mode
		self.screen = screen
		
	def add_rnum(self, rnum): #keeps track of rocks for score
		self.rocks = rnum
		
	def add_extra(self):#for adding score when collide with green rock
		if self.mode == 0:
			self.extra = 1000 * self.level
			self.svalue = self.svalue + self.extra
		elif self.mode == 1:
			self.extra = 300 * self.rocks
			self.svalue = self.svalue + self.extra
		
	def score_tracker(self, level, isDead): #main score tracking function
		self.isDead = isDead
		if self.isDead == 0 and self.mode == 0:#if classic mode and not dead
			if self.level != 5:
				self.svalue = self.svalue + (self.rocks / 3)#adds score each time
				self.svalue = round(self.svalue, 1)
				self.score_draw()#draws counter
				return self.svalue
			else:#for final level
				self.svalue = self.svalue + 25
				self.svalue = round(self.svalue, 1)
				self.score_draw()
				return self.svalue
		elif self.mode != 0 and self.isDead == 0:#for endless mode
			self.svalue = self.svalue + (self.rocks * 3)
			return self.svalue
		else:
			return self.svalue#if dead
			
	def save_high_score(self):
		if self.mode == 0:
			file = open((os.path.join(sys.path[0], 'Resources\hs.txt')), "r")#opens file and reads old high score
		elif self.mode == 1:
			file = open((os.path.join(sys.path[0], 'Resources\hs2.txt')), "r")
		else:
			file = open((os.path.join(sys.path[0], 'Resources\hs3.txt')), "r")
		oldHS = float(file.read())
		file.close()
		if self.svalue > oldHS: #if new score is higher, replace high score
			if self.mode == 0:
				file = open((os.path.join(sys.path[0], 'Resources\hs.txt')), "w")#opens file and reads old high score
			elif self.mode == 1:
				file = open((os.path.join(sys.path[0], 'Resources\hs2.txt')), "w")#
			else:
				file = open((os.path.join(sys.path[0], 'Resources\hs3.txt')), "w")#
			file.write(str(self.svalue))
			file.close()
	
	def get_high_score(self):
		if self.mode == 0:
			file = open((os.path.join(sys.path[0], 'Resources\hs.txt')), "r")#opens file and reads old high score
		elif self.mode == 1:
			file = open((os.path.join(sys.path[0], 'Resources\hs2.txt')), "r")
		else:
			file = open((os.path.join(sys.path[0], 'Resources\hs3.txt')), "r")
		score = file.read()
		return score
			
	def score_draw(self):
		#define counter/win text and blit both of them
		counterText = pygame.font.Font('freesansbold.ttf', 25)
		counter = counterText.render("Score:", True, (255, 255, 255))
		self.screen.blit(counter,(1375,800))
		score = int(self.svalue)
		wincounter = counterText.render(str(score), True, (255, 255, 255))
		self.screen.blit(wincounter,(1375,830))