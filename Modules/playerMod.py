import pygame, math, os, sys, time

class Player:
	def __init__(self, screen):
		self.health = 3
		self.screen = screen
		self.playerSprites = [(pygame.image.load(os.path.join(sys.path[0], 'Resources\ship.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\shipm.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\shipl.png')).convert_alpha())]
		self.x = 100
		self.y = 100
		self.dx = 0
		self.dy = 0
		self.gun_angle = 0
		self.dead = 0
		self.psprite = self.playerSprites[0]
		self.unpause = pygame.image.load(os.path.join(sys.path[0], 'Resources\sunpause.png')).convert()
		self.rect = pygame.Rect(self.x, self.y, 16, 16)
		self.boostTime = 0 
		self.boost = 1
	
	def move(self):
		#adds slowing force
		if self.dx > -6 and self.dx < 0:
			self.dx = self.dx + .1
		if self.dx < 6 and self.dx > 0:
			self.dx = self.dx - .1
		if self.dy > -6 and self.dy < 0:
			self.dy = self.dy + .1
		if self.dy < 6 and self.dy > 0:
			self.dy = self.dy - .1
		#when wasd is pressed, add speed
		key = pygame.key.get_pressed()
		if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.dx < 5:
			self.dx = self.dx + .9
		if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.dx > -5:
			self.dx = self.dx - .9
		if (key[pygame.K_w] or key[pygame.K_UP]) and self.dy > -5:
			self.dy = self.dy - .9
		if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.dy < 5:
			self.dy = self.dy + .9
		if key[pygame.K_p]: #runs pause def
			self.pause()
		self.collision()#runs wall collision check
		if self.boost == 2:
			self.boost_counter()
		#adds/sub speed from sprite coordinates
		self.x = (self.x + (self.boost * self.dx))
		self.y = (self.y + (self.boost * self.dy))
		return (self.x, self.y)
		
	def collision(self):#if player is hitting a wall, bounce them off of it.
		#top wall
		if self.rect.colliderect((0, -100, 1500, 110)) == True:
			self.dy = self.dy + 2
		#bottom wall
		elif self.rect.colliderect(0, 890, 1500, 110) == True:
			self.dy = self.dy - 2
		#right wall
		elif self.rect.colliderect((1490, 0, 110, 900)) == True:
			self.dx = self.dx - 2
		#left wall
		elif self.rect.colliderect((-100, 0, 110, 900)) == True:
			self.dx = self.dx + 2
						
	
	def change_health(self, change, score):
		self.health = self.health + change
		if self.health == 3:
			self.psprite = self.playerSprites[0]
		elif self.health == 2:
			self.psprite = self.playerSprites[1]
		elif self.health == 1:
			self.psprite = self.playerSprites[2]
		elif self.health > 3:
			self.health = 3
		else:
			self.die(score)
			self.dead = 1

	def check_health(self):
			return self.health

	def die(self, score):
		if self.dead == 0:#does all death activites but only once
			game_over = pygame.mixer.music.load(os.path.join(sys.path[0], 'Resources\game_over.mp3'))
			pygame.mixer.music.play(loops=1)
			score.save_high_score()#records score if its the best
		
	def boost_mode(self):
		self.boost = 2
		self.boostTime = 300#sets to five seconds bc 60 fps

	def boost_counter(self):
		self.boostTime = (self.boostTime - 1)
		if self.boostTime == 0:
			self.boost = 1
		
	def draw(self, pos):
		self.rect = self.screen.blit(self.psprite, pos)
		
	def pause(self):
		print("Paused")
		paused = True
		self.screen.blit(self.unpause, (650, 400))
		pygame.display.flip()
		time.sleep(.5)
		while paused == True:
			for event in pygame.event.get():
				#if user presses quit, quit
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					#push any button to unpause
					paused = False