import pygame, math, os, sys

class Rock:
	def __init__(self, speed, direction, type, fake, screen):
		self.WHITE = (255, 255, 255)
		self.GREEN = (0, 255, 0)
		self.speed = speed
		self.screen = screen
		self.color = self.WHITE
		self.direct = direction
		self.type = type
		self.fake = fake
		self.dead = 0
		self.inv = False
		#0 is asteroid, 1 point, 2 health, 3 boost, 4 slow, 5 clear
		self.sprites = [(pygame.image.load(os.path.join(sys.path[0], 'Resources\srock.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\scoin.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\sheart.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\srockboost.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\srockslow.png')).convert_alpha()), (pygame.image.load(os.path.join(sys.path[0], 'Resources\srockclear.png')).convert_alpha())]
		self.hit = pygame.mixer.Sound(os.path.join(sys.path[0], 'Resources\hit.wav'))
		self.coin = pygame.mixer.Sound(os.path.join(sys.path[0], 'Resources\coin.wav'))
		self.x = 750
		self.y = 450
		self.slowFactor = 1
		self.deleteMode = False
		
	def move(self, slow):
		self.dx = 0
		self.dy = 0
		#rect = pygame.Rect((500, 500), (2, 2))
		#for each speed, move rock by one unit in direction of angle
		for i in range(self.speed):
			degree = 0
			degree = math.radians(self.direct)
			self.dx = self.dx + (math.cos(degree) / slow)
			self.dy = self.dy - (math.sin(degree) / slow)
		self.x = self.x + self.dx
		self.y = self.y + self.dy
				
		
	def draw(self):
		self.rect = pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), 12)#draws underlying circle for collision
		adjPos = ((int(self.x) - 15), (int(self.y) - 15))
		if self.type != 6:
			self.screen.blit(self.sprites[self.type], adjPos)#blits asteroid photo but only if its not the transition
		
	def collision(self, pos, isActive, gameLevel, player, score):
		#top wall
		if isActive == 1 and gameLevel != 5:
			if self.rect.colliderect((0, 0, 1500, 10)) == True:
				self.direct = -1 * self.direct
			#bottom wall
			elif self.rect.colliderect(0, 890, 1500, 10) == True:
				#in_angle = math.degrees(math.atan(self.y/self.x))
				self.direct =  -1 * self.direct
			#right wall
			elif self.rect.colliderect((1490, 0, 10, 900)) == True:
				self.direct = (self.direct * -1) + 180
			#left wall
			elif self.rect.colliderect((0, 0, 10, 900)) == True:
				self.direct = (self.direct * -1) - 180
		elif isActive == 0 and gameLevel != 5:#if the player is hit during hyperspace it dosen't count
			self.inv = True 
			self.inv_time = pygame.time.get_ticks()
		time_now = pygame.time.get_ticks()
		#checks if invincible, if so, check if collide
		if self.inv == False:
			self.hit_player(pos, player, score)
		else:
			if (time_now - 2000) > self.inv_time:
				self.inv = False
		
		
	def hit_player(self, pos, player, score):
		if self.rect.colliderect(pos[0], pos[1], 40, 40) == True and self.fake == False:
			if self.type == 0:
				#makes player sprite go down by one health
				change = -1
				player.change_health(change, score)
				change = 0
				self.hit.play()
				#turns on invincibility
				self.inv = True
				self.inv_time = pygame.time.get_ticks()
			elif self.type == 1:#coin collision, add score
				self.coin.play()
				score.add_extra()
			elif self.type == 2:#health collision, add health
				health = player.check_health()
				if health == 3:#if player health is full, add points instead
					score.add_extra()
				else:
					change = 1
					player.change_health(change, score)
					change = 0
			elif self.type == 3:
					player.boost_mode()
			elif self.type == 4:#for slowing asteroids
				self.slowFactor = 2
			elif self.type == 5:#for deleting rocks
				self.deleteMode = True
			if type != 0:
					self.dead = 1

				
	def is_dead_question_mark(self):
		return self.dead