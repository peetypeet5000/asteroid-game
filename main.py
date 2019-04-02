
import pygame, os, sys, math, random
from pygame.locals import *

# Setup
pygame.init()
pygame.font.init()
size = WIDTH, HEIGHT = (1500, 900)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption("Untitled Game")
done = False
lines = []
rocks = []
player_sprite = pygame.image.load(os.path.join(sys.path[0], 'Resources\ship.png'))
player_sprite2 = pygame.image.load(os.path.join(sys.path[0], 'Resources\shipm.png'))
player_sprite3 = pygame.image.load(os.path.join(sys.path[0], 'Resources\shipl.png'))
player_mask = pygame.mask.from_surface(player_sprite)

#sets timer to be used to spawn rocks
pygame.time.set_timer(USEREVENT+1 , 5000)

# this is where the images are
player_rect = player_sprite.get_rect()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


'''''''''''''''
CLASS DEFINITIONS
'''''''''''''''
class Player:
	def __init__(self):
		self.health = 3
		self.x = 100
		self.y = 100
		self.dx = 0
		self.dy = 0
		self.psprite = player_sprite
		self.rect = pygame.Rect(self.x, self.y, 16, 16)
	
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
		if key[pygame.K_d] and self.dx < 5:
			self.dx = self.dx + .9
		if key[pygame.K_a] and self.dx > -5:
			self.dx = self.dx - .9
		if key[pygame.K_w] and self.dy > -5:
			self.dy = self.dy - .9
		if key[pygame.K_s] and self.dy < 5:
			self.dy = self.dy + .9
		#adds/sub speed from sprite coordinates
		self.x = (self.x + self.dx)
		self.y = (self.y + self.dy)
		return (self.x, self.y)
				
	
	def change_health(self, change):
		self.health = self.health + change
		if self.health == 3:
			self.psprite = player_sprite
		elif self.health == 2:
			self.psprite = player_sprite2
		elif self.health == 1:
			self.psprite = player_sprite3
		else:
			print('you died')
		
	
	def draw(self, pos):
		screen.blit(self.psprite, pos)
		#pygame.draw.rect(screen, WHITE, self.rect, 0)
		
class rock:
	def __init__(self, speed, direction, good):
		self.speed = speed
		self.friendly = good
		self.direct = direction
		self.inv = False
		self.x = 700
		self.y = 500
		
	def move(self):
		self.dx = 0
		self.dy = 0
		rect = pygame.Rect((500, 500), (2, 2))
		for i in range(self.speed):
			degree = 0
			degree = math.radians(self.direct)
			self.dx = self.dx + math.cos(degree)
			self.dy = self.dy - math.sin(degree)
		self.x = self.x + self.dx
		self.y = self.y + self.dy
				
		
	def draw(self):
		self.rect = pygame.draw.rect(screen, WHITE, (self.x, self.y, 15, 15))
		
	def collision(self, pos):
		#top wall
		if self.rect.colliderect((0, 0, 1500, 10)) == True:
			self.direct = -1 * self.direct
		#bottom wall
		elif self.rect.colliderect(0, 890, 1500, 10) == True:
			self.direct =  -1 * self.direct
		#right wall
		elif self.rect.colliderect((1490, 0, 10, 900)) == True:
			self.direct = (self.direct * -1) + 180
		#left wall
		elif self.rect.colliderect((0, 0, 10, 900)) == True:
			self.direct = self.direct * .3
		time = pygame.time.get_ticks()
		if self.inv == False:
			self.hit_player(pos)
		else:
			if (time - 2000) > self.inv_time:
				self.inv = False
		
		
	def hit_player(self, pos):
		if self.rect.colliderect(pos[0], pos[1], 50, 50) == True:
			print('oh no')
			change = -1
			player.change_health(change)
			change = 0
			self.inv = True
			self.inv_time = pygame.time.get_ticks()

'''''''''
FUNCTION DEFINITONS
'''''''''	

def rock_generator():
	global rnum
	angle = random.randint(0, 360)
	rocks.append(rock(6, angle, 1))
	rnum = rnum + 1
	print(rnum)
	return rocks
	
	
def side_draw():
	rects = [(0, 0, 10, 900), (0, 0, 1500, 10), (0, 890, 1500, 10), (1490, 0, 10, 900)]
	for i in range(4):
		pygame.draw.rect(screen, WHITE, rects[i])
	
		
#call player class
player = Player()
rnum = 0


#main game function	
while not done:
	#checks if some input
	for event in pygame.event.get():
		#if user presses quit, quit
		if event.type == pygame.QUIT:
			done = True
		if event.type == USEREVENT+1:
			rocks = rock_generator()
				
	#place all logic here
	pos = player.move()
	for i in range(rnum):
		rocks[i].move()
	
	
	#place all drawing here
	screen.fill(BLACK)
	side_draw()
	player.draw(pos)
	for i in range(rnum):
		rocks[i].draw()
		rocks[i].collision(pos)
	
	clock.tick(60)
	pygame.display.flip()
	#print(clock.get_fps())
	
''''

'''
	