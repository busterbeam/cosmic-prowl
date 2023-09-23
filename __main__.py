#!/bin/venv python
""" Cosmic Prowl entry """

import sys

from collections import namedtuple
from random import randint
from sys import float_info

from pygame import (
	display,
	sprite,
	Surface,
	key,
	init,
	time,
	quit as game_quit,
	transform,
	image,
	Rect,
	event as event_queue,
)
from pygame.locals import (
	K_LEFT,
	K_RIGHT,
	K_UP,
	K_DOWN,
	K_w,
	K_a,
	K_s,
	K_d,
	K_LSHIFT,
	QUIT,
)

from particles import Particles, Particle

Size = namedtuple("Size", "width height")
SCREEN = Size(600, 600)
MINIMUM = Size(400, 400)
PLAYER_SPEED = 4
TILE_SIZE = 16

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
	"""Object Sprite"""

	def __init__(self, image_path, frame_size, init_position):
		"""Initializer"""
		super().__init__()
		surface = image.load(image_path).convert_alpha()
		self.image = surface.subsurface(
			3 * frame_size, 2 * frame_size, frame_size, frame_size
		)
		self.rect = Rect(init_position, self.image.get_rect()[2:])


class Player(sprite.Sprite):
	"""Player Sprite"""

	def __init__(self, image_path, origin):
		"""Initializer"""
		super().__init__()
		self.sprite_sheet = image.load(image_path).convert_alpha()
		self.cone = Rect(0, 0, TILE_SIZE, TILE_SIZE)
		self.current_frame = 0
		self.state = RIGHT_IDLE
		self.run = (1, 0)
		self.update_frames()
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.centerx = origin[0]
		self.rect.centery = origin[1]
		self.set_cone()
	
	def set_cone(self):
		if (self.state % 4) == RIGHT_IDLE:
			self.cone.centerx = self.rect.centerx + TILE_SIZE
			self.cone.centery = self.rect.centery
		elif (self.state % 4) == LEFT_IDLE:
			self.cone.centerx = self.rect.centerx - TILE_SIZE
			self.cone.centery = self.rect.centery
		elif (self.state % 4) == DOWN_IDLE:
			self.cone.centerx = self.rect.centerx
			self.cone.centery = self.rect.centery + TILE_SIZE
		elif (self.state % 4) == UP_IDLE:
			self.cone.centerx = self.rect.centerx
			self.cone.centery = self.rect.centery - TILE_SIZE

	def update_frames(self):
		"""Change what frames are being used for the animation"""
		self.frames = []
		subsurface = self.sprite_sheet.subsurface
		for i in range(4):
			self.frames.append(
				subsurface(
					Rect(
						i * TILE_SIZE,
						self.state * TILE_SIZE,
						TILE_SIZE, TILE_SIZE,
					)
				)
			)

	def update(self):
		"""Overwrite of Sprite updating"""
		keys = key.get_pressed()
		if any(keys):
			if keys[K_LSHIFT]:
				self.run = (2, 4)
			if keys[K_RIGHT] or keys[K_d]:
				self.rect.x += PLAYER_SPEED * self.run[0]
				self.state = RIGHT_WALKING + self.run[1]
			elif keys[K_LEFT] or keys[K_a]:
				self.rect.x -= PLAYER_SPEED * self.run[0]
				self.state = LEFT_WALKING + self.run[1]
			elif keys[K_DOWN] or keys[K_s]:
				self.rect.y += PLAYER_SPEED * self.run[0]
				self.state = DOWN_WALKING + self.run[1]
			elif keys[K_UP] or keys[K_w]:
				self.rect.y -= PLAYER_SPEED * self.run[0]
				self.state = UP_WALKING + self.run[1]
			else:
				self.run = (1, 0)
				if self.state >= 4:
					self.state = max(0, self.state - 4)
			self.update_frames()
			self.set_cone()
		elif self.state >= 8:
			self.run = (1, 0)
			self.state = max(0, self.state - 8)
			self.update_frames()
		elif self.state >= 4:
			self.state = max(0, self.state - 4)
			self.update_frames()
		self.current_frame = (self.current_frame + 1) % 4
		self.image = self.frames[self.current_frame]



def main():
	"""main function"""
	init()
	screen = display.set_mode(SCREEN)
	display.set_caption("Wolf Tracking Game")
	game_surface = Surface((200, 200))
	all_sprites = sprite.Group()
	player = Player("Wolf.png", (30, 30))
	all_sprites.add(player)
	for _ in range(10):
		all_sprites.add(
			Shroom(
				"GrassNDirt.png",
				TILE_SIZE,
				(randint(0, 10) * TILE_SIZE, randint(0, 10) * TILE_SIZE),
			)
		)
	particles = Particles()
	for _ in range(350):
		particles.append(
			Particle(
				(randint(0, 200), randint(0, 200)),
				(randint(-1, 1), randint(-1, 1)),
				(2, 16), "cyan"
			)
		)
	clock = time.Clock()
	event_queue.pump()
	event = event_queue.wait(1)
	while event.type != QUIT:
		all_sprites.update()
		particles.collisions(game_surface.get_bounding_rect(), player)
		particles.update()
		game_surface.fill("black")
		all_sprites.draw(game_surface)
		particles.draw(game_surface)
		frame = transform.scale(game_surface, SCREEN)
		screen.blit(frame, (0, 0))
		display.flip()
		clock.tick(15)
		event_queue.pump()
		event = event_queue.wait(1)
	game_quit()


if __name__ == "__main__":
	main()
	sys.exit()
