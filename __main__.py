from pygame import (
	display, sprite, Surface, key, init, time,
	quit, transform, image, Rect, event as event_queue)
from pygame.locals import (
	K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_a, K_s, K_d, K_LSHIFT, QUIT)
from sys import exit
from collections import namedtuple
from random import randint

size = namedtuple("size", "width height")
SCREEN = size(600, 600)
MINIMUM = size(400, 400)
PLAYER_SPEED = 16
TILE_SIZE = 16

SCALER = 4

# sprite state
RIGHT_IDLE = 0
LEFT_IDLE = 1
DOWN_IDLE = 2
UP_IDLE = 3
RIGHT_WALKING = 4
LEFT_WALKING = 5
DOWN_WALKING = 6
UP_WALKING = 7
RIGHT_RUNNING = 8
LEFT_RUNNING = 9
DOWN_RUNNING = 10
UP_RUNNING = 11


class Shroom(sprite.Sprite):
	def __init__(self, image_path, frame_size, init_position):
		super().__init__()
		surface = image.load(image_path).convert_alpha()
		surface = surface.subsurface(
			3 * frame_size, 2 * frame_size, frame_size, frame_size)
		width, height = surface.get_size()
		self.image = transform.scale(surface, (width * SCALER, height * SCALER))
		self.rect = Rect(
			(init_position[0]*SCALER, init_position[1]*SCALER),
			self.image.get_rect()[2:])


class Player(sprite.Sprite):
	def __init__(self, image_path, frame_size):
		super().__init__()
		self.sprite_sheet = image.load(image_path).convert_alpha()
		width, height = self.sprite_sheet.get_size()
		self.sprite_sheet = transform.scale(
			self.sprite_sheet, (width * SCALER, height * SCALER))
		self.current_frame = 0
		self.state = RIGHT_IDLE
		self.run = False
		self.frame_size = frame_size * SCALER
		self.update_frames()
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()

	def update_frames(self):
		self.frames = list()
		subsurface = self.sprite_sheet.subsurface
		for i in range(4):
			self.frames.append(subsurface(Rect(
				i * self.frame_size,
				self.state * self.frame_size,
				self.frame_size, self.frame_size
			)))

	def update(self):
		keys = key.get_pressed()
		print(end=f"\x1B[2K{'x'*any(keys)}\r")
		if any(keys):
			if keys[K_LSHIFT]:
				self.run = True
			if keys[K_RIGHT] or keys[K_d]:
				self.rect.x += PLAYER_SPEED * (2 if self.run else 1)
				self.state = RIGHT_WALKING + (4 if self.run else 0)
			elif keys[K_LEFT] or keys[K_a]:
				self.rect.x -= PLAYER_SPEED * (2 if self.run else 1)
				self.state = LEFT_WALKING + (4 if self.run else 0)
			elif keys[K_DOWN] or keys[K_s]:
				self.rect.y += PLAYER_SPEED * (2 if self.run else 1)
				self.state = DOWN_WALKING + (4 if self.run else 0)
			elif keys[K_UP] or keys[K_w]:
				self.rect.y -= PLAYER_SPEED * (2 if self.run else 1)
				self.state = UP_WALKING + (4 if self.run else 0)
			else:
				self.run = False
				self.state = max(0, self.state - 4)
			self.update_frames()
		elif self.state >= 8:
			self.run = False
			self.state = max(0, self.state - 8)
			self.update_frames()
		elif self.state >= 4:
			self.state = max(0, self.state - 4)
			self.update_frames()
		self.current_frame = (self.current_frame + 1) % 4
		self.image = self.frames[self.current_frame]


if __name__ == "__main__":
	init()
	screen = display.set_mode(SCREEN)
	display.set_caption("Wolf Tracking Game")

	all_sprites = sprite.Group()
	player = Player("Wolf.png", TILE_SIZE)
	all_sprites.add(player)
	for _ in range(10):
		all_sprites.add(Shroom(
			"GrassNDirt.png", TILE_SIZE,
			(
				randint(0, 10) * TILE_SIZE,
				randint(0, 10) * TILE_SIZE
			)
		))
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

