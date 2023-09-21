from pygame import (
	display, sprite, Surface, key, init, time, quit, event as event_queue)
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, QUIT
from sys import exit

init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Wolf Tracking Game")

class Player(sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = Surface((30, 30))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
		self.x_speed = 0
		self.y_speed = 0

	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT]:
			self.x_speed = -PLAYER_SPEED
		elif keys[K_RIGHT]:
			self.x_speed = PLAYER_SPEED
		else:
			self.x_speed = 0
		if keys[K_UP]:
			self.y_speed = -PLAYER_SPEED
		elif keys[K_DOWN]:
			self.y_speed = PLAYER_SPEED
		else:
			self.y_speed = 0

		self.rect.x += self.x_speed
		self.rect.y += self.y_speed

all_sprites = sprite.Group()
player = Player()
all_sprites.add(player)

running = True
clock = time.Clock()

while running:
	for event in event_queue.get():
		if event.type == QUIT:
			running = False
	all_sprites.update()
	screen.fill(BLACK)
	all_sprites.draw(screen)
	display.flip()
	clock.tick(60)
quit()
exit()

