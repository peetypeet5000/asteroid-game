import pygame, os, sys

class Menu:
	def __init__(self, screen, clock):
		#loads all images and sets varaibles
		self.done = False
		self.screen = screen
		self.clock = clock
		self.WHITE = (255, 255, 255)
		self.bg = pygame.image.load(os.path.join(sys.path[0], 'Resources\spacemain.jpg')).convert()
		self.classic = pygame.image.load(os.path.join(sys.path[0], 'Resources\classic.jpg')).convert()
		self.endless = pygame.image.load(os.path.join(sys.path[0], 'Resources\endless.png')).convert()
		self.arcade = pygame.image.load(os.path.join(sys.path[0], 'Resources\sarcade.png')).convert()
		self.title = pygame.image.load(os.path.join(sys.path[0], 'Resources\logo.png')).convert()
		
	def get_scores(self):#reads high scores files and saves them to be printed
		file = open((os.path.join(sys.path[0], 'Resources\hs.txt')), "r")
		self.score1 = file.read()
		file = open((os.path.join(sys.path[0], 'Resources\hs2.txt')), "r")
		self.score2 = file.read()
		file = open((os.path.join(sys.path[0], 'Resources\hs3.txt')), "r")
		self.score3 = file.read()
		file.close()
		
	def start_music(self):
		music = pygame.mixer.music.load(os.path.join(sys.path[0], 'Resources\menumusic.mp3'))
		pygame.mixer.music.play(loops=-1)
		
	def main(self):
		self.get_scores()#gets info each time menu is called, resets some varaibles
		self.start_music()
		self.x = 0
		self.y = 0
		while not self.done:

		#checks for mouse and quit events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return 3#will quit main func
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y postions of the mouse click
					self.x, self.y = event.pos
					print(self.x, self.y)
			if self.x > 400 and self.x < 700 and self.y > 350 and self.y < 520:#checks which button mouse was on
				return 0#classic mode
			elif self.x > 500 and self.x < 900 and self.y > 650 and self.y < 800:
				return 1#endless mode
			elif self.x > 600 and self.x < 1100 and self.y > 350 and self.y < 520:
				return 2#arcade mode
		
			#drawing
			textBody = pygame.font.Font('freesansbold.ttf', 25)
			highScore = textBody.render(str(self.score1), True, self.WHITE)
			highScoreEndless = textBody.render(str(self.score2), True, self.WHITE)
			highScoreArcade = textBody.render(str(self.score3), True, self.WHITE)
			highScoreText = textBody.render("High Score:", True, self.WHITE)
			copyrightText = textBody.render("© 2019 Peter LaMontagne", True, self.WHITE)
			verText = textBody.render("Version: 1.1", True, self.WHITE)
			blit_list = [(self.bg, (0, 0)), (self.classic, (400, 350)), (verText,(1320, 820)), (copyrightText,(1175,860)), (highScore, (450, 590)), (highScoreText, (450, 550)), (highScoreText, (700, 840)), (self.endless, (600, 650)), (self.title, (400, 100)), (self.arcade, (800, 350)), (highScoreArcade, (875, 590)), (highScoreText, (875, 550)), (highScoreEndless, (725, 875))]
			self.screen.blits(blit_list)
			
			#set fps and update screen
			self.clock.tick(30)
			pygame.display.flip()
