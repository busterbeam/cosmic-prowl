from pygame import (
	display, sprite, Surface, key, init, time,
	quit, transform, image, Rect, event as event_queue)
from pygame.locals import (
	K_LEFT, K_RIGHT, K_UP, K_DOWN, QUIT)
from sys import exit
from collections import namedtuple

size = namedtuple("size", "width height")
SCREEN = size(600, 600)
MINIMUM = size(400, 400)
PLAYER_SPEED = 15

SCALER = 4

# dog directions
RIGHT = 0
LEFT = 1
DOWN = 2
UP = 3

class Player(sprite.Sprite):
	def __init__(self, image_path, frame_size):
		super().__init__()
		self.sprite_sheet = image.load(image_path).convert_alpha()
		width, height = self.sprite_sheet.get_size()
		self.sprite_sheet = transform.scale(
			self.sprite_sheet, (int(width * SCALER), int(height * SCALER)))
		self.current_frame = 0
		self.frame_size = frame_size * SCALER
		self.update_frames(RIGHT)
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()

	def update_frames(self, orientation):
		self.frames = list()
		subsurface = self.sprite_sheet.subsurface
		for i in range(4):
			self.frames.append(subsurface(Rect(
				i * self.frame_size,
				orientation * self.frame_size,
				self.frame_size, self.frame_size
			)))

	def update(self):
		keys = key.get_pressed()
		if keys[K_RIGHT]:
			self.rect.x += PLAYER_SPEED
			self.update_frames(RIGHT)
		elif keys[K_LEFT]:
			self.rect.x -= PLAYER_SPEED
			self.update_frames(LEFT)
		elif keys[K_DOWN]:
			self.rect.y += PLAYER_SPEED
			self.update_frames(DOWN)
		elif keys[K_UP]:
			self.rect.y -= PLAYER_SPEED
			self.update_frames(UP)
		self.current_frame = (self.current_frame + 1) % 4
		self.image = self.frames[self.current_frame]


if __name__ == "__main__":
	init()
	screen = display.set_mode(SCREEN)
	display.set_caption("Wolf Tracking Game")

	all_sprites = sprite.Group()
	player = Player("Wolf.png", 16)
	all_sprites.add(player)
	clock = time.Clock()

	while True:
		event_queue.pump()
		event = event_queue.wait(1)
		if event.type == QUIT:
			break

		all_sprites.update()
		screen.fill("black")
		all_sprites.draw(screen)
		display.flip()
		clock.tick(15)
	quit()
	exit()

