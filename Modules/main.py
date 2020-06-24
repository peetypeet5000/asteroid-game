import pygame, os, sys, math, random, time
from Modules import *

class GameHandler:
	def __init__(self):
		# Setup
		pygame.init()
		pygame.font.init()
		size = WIDTH, HEIGHT = (1500, 900)
		self.screen = pygame.display.set_mode(size)
		self.clock = pygame.time.Clock()
		pygame.display.set_caption("Starblock")

		#load all images
		self.retry = pygame.image.load(os.path.join(sys.path[0], 'Resources\stry.png')).convert()
		self.btm = pygame.image.load(os.path.join(sys.path[0], 'Resources\sbtm.png')).convert()
		self.caution = pygame.image.load(os.path.join(sys.path[0], 'Resources\caution.png')).convert_alpha()
		self.rockPic = pygame.image.load(os.path.join(sys.path[0], 'Resources\srock.png')).convert_alpha()

		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.finished = False
		self.firstRun = 0
		
		self.menu = menu.Menu(self.screen, self.clock)#creates menu object
	
		
	def rock_generator(self):
		#sets all the parameters to a random value then adds the rock to the rock list
		angle = random.randint(0, 360)
		speed = random.randint(3, 10)
		#lists for the modes to determine probablility of spawning each type
		classicList = [0, 0, 0, 0 ,1]
		arcadeList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 3, 4, 4, 5]
		if self.mode == 0 or self.mode == 1:
			type = random.choice(classicList)
		elif self.mode == 2:
				type = random.choice(arcadeList)
		self.rocks.append(rock.Rock(speed, angle, type, False, self.screen))
		self.rnum = self.rnum + 1
		self.score.add_rnum(self.rnum)
		
	def side_draw(self):
		rects = [(0, 0, 10, 900), (0, 0, 1500, 10), (0, 890, 1500, 10), (1490, 0, 10, 900)]
		for i in range(4):
			pygame.draw.rect(self.screen, self.WHITE, rects[i])
			
	def caution_draw(self):
		self.screen.blit(self.caution, (725, 400))
		
	def death_screen(self):
		#rects and text for game over screen
		pygame.draw.rect(self.screen, self.BLACK, (500, 300, 500, 330), 0)
		pygame.draw.rect(self.screen, self.WHITE, (500, 300, 500, 330), 5)
		loseTextHeader = pygame.font.Font('freesansbold.ttf', 50)
		loseTextBody = pygame.font.Font('freesansbold.ttf', 25)
		losescreen = loseTextHeader.render("You Lost", True, self.WHITE, self.BLACK)
		losescreenbody = loseTextBody.render("Score:", True, self.WHITE, self.BLACK)
		losescreenscore = loseTextBody.render(str(self.svalue), True, self.WHITE, self.BLACK)
		loseScreenHigh = loseTextBody.render("High Score:", True, self.WHITE, self.BLACK)
		highScore = self.score.get_high_score()
		loseScreenHighScore = loseTextBody.render(str(highScore), True, self.WHITE, self.BLACK)
		blit_list = [(losescreenbody,(660,400)), (losescreenscore,(750,400)), (loseScreenHigh, (600, 450)), (loseScreenHighScore, (750, 450)), (losescreen,(645,320)), (self.retry, (525, 500)), (self.btm, (760, 500))]
		self.screen.blits(blit_list)
		
	def death(self):
		if self.isDead == 1:#if player is dead, draw lose screen and check if clicks retry
			self.death_screen()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos# Set the x, y postions of the mouse click
					if x > 525 and x < 725 and y > 300 and y < 600:#to retry exits back into outer loop
						self.done = True
					elif x > 760 and x < 960 and y > 300 and y < 600:#same thing but sets main menu to show up again
						self.firstRun = 0
						self.done = True
						
	def delete_powerup(self):
		numberToDelete = (self.rnum / 7 ) + 1
		print(numberToDelete)
		for i in range(int(numberToDelete)):
			rockToDelete = random.choice(self.rocks)
			del rockToDelete
			self.rnum = self.rnum - 1
		self.deleteMode = False
		
		
	def logic(self):
		for event in pygame.event.get():#checks if user presses quit
			if event.type == pygame.QUIT:
				pygame.quit()#quits game
				sys.exit()#exits prompt				
		self.isActive = self.difficulty.active
		self.isDead = self.player.dead
		self.gameLevel = self.difficulty.level
		self.rockFreq = self.difficulty.adjusted_rock_freq()
		if self.slowFactor == 2:#clock to reset rocks slowing
			self.slowCounter = self.slowCounter + 1
			if self.slowCounter == 600:#once ten seconds had passed, reset
				self.slowFactor = 1
				self.slowCounter = 0
		if self.isDead == 0: #if played died, ignore moving it and adding score
			self.pos = self.player.move()
			self.svalue = self.score.score_tracker(self.gameLevel, self.isDead)
		for i in range(self.rnum): #loops thru all rock objects to move them, check powerups
			self.rocks[i].move(self.slowFactor)
			self.rmValue = self.rocks[i].is_dead_question_mark()
			if self.rocks[i].slowFactor == 2:
				self.slowFactor = 2
			if self.rocks[i].deleteMode == True:
				self.deleteMode = True
			if self.rmValue == 1: #deletes a rock if its collected
				del self.rocks[i]
				self.rnum = self.rnum - 1
				break
		if self.deleteMode == True:
			self.delete_powerup()
				
	def drawing(self):
		self.background.draw_background(self.difficulty)#draws bg
		if self.isActive == 1 and self.gameLevel != 5:#draws the border only if the game is not in hyperspace
			self.side_draw()
		self.score.score_draw()#draws score & player
		self.player.draw(self.pos)
		for i in range(self.rnum):  #draw rocks, checks their collision
			self.rocks[i].draw()
			self.rocks[i].collision(self.pos, self.isActive, self.gameLevel, self.player, self.score)
			
		self.now = pygame.time.get_ticks()
		if (self.time_start + self.rockFreq) < self.now and self.isActive == 1: #create a new rock every rockFreq
			self.rock_generator()
			self.time_start = pygame.time.get_ticks()
			self.cautionTrig = 0
		elif (self.time_start + (self.rockFreq - 1000)) < self.now and self.isActive == 1:#draw caution sign
			if self.cautionTrig == 0: #a bunch of crap merely to draw the caution sign flashing
				self.cautionTime = pygame.time.get_ticks()
				self.cautionTrig = 1
			else:
				self.now = pygame.time.get_ticks()
				if (self.cautionTime + 100) > self.now:
					self.caution_draw()
				elif (self.cautionTime + 200) > self.now:
					self.cautionTrig = 0	
		
	def main(self):
		while not self.finished:
			#Run Main Menu/Setup
			if self.firstRun == 0:
				self.mode = self.menu.main()
				if self.mode == 3:
					pygame.quit()
					sys.exit()
				self.firstRun = 1


			#call player/score class
			self.player = playerMod.Player(self.screen)
			self.score = scoreMod.Score(self.screen, self.mode)
			self.background = backgroundMod.Background(self.screen, self.mode, 30000)#calls bg class, number is change freq
			self.difficulty = difficultyMod.Difficulty()
			self.done = False
			
			#variables
			self.rnum = 0
			self.done = False
			self.rocks = []
			self.rnum = 0
			self.time_start = 0
			self.rmValue = 0
			self.rockToRm = 0
			self.add = 0
			self.isDead = 0
			self.rockFreq = 5000
			self.cautionTrig = 0
			self.gameLevel = 1
			self.gameLevel = 1
			self.slowFactor = 1
			self.slowCounter = 0
			self.deleteMode = False

			#load and start music
			music = pygame.mixer.music.load(os.path.join(sys.path[0], 'Resources\music.mp3'))
			pygame.mixer.music.play(loops=-1)

			#main game function     
			while not self.done:
			
				'''''''''''''''
				*****LOGIC*****
				'''''''''''''''
				
				self.logic()
				
				'''''''''''''''
				****DRAWING***
				'''''''''''''''
				
				self.drawing()
				
				self.death()
									
									
				
				self.clock.tick(60)
				pygame.display.flip()
				#print(clock.get_fps())
				
			
