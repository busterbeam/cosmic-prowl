#!/bin/venv python
""" Cosmic Prowl entry """

import sys

from collections import namedtuple
from random import randint

from pygame import (
	display,
	sprite,
	Surface,
	init,
	time,
	quit as game_quit,
	transform,
	image,
	Rect,
	event as event_queue,
)
from pygame.locals import QUIT

from particles import Particles, Particle
from characters import Player, Bear

Size = namedtuple("Size", "width height")
SCREEN = Size(600, 600)
MINIMUM = Size(400, 400)
PLAYER_SPEED = 4
TILE_SIZE = 16


class Shroom(sprite.Sprite):
	"""Object Sprite"""

	def __init__(self, image_path, origin):
		"""Initializer"""
		super().__init__()
		surface = image.load(image_path).convert_alpha()
		self.image = surface.subsurface(
			3 * TILE_SIZE, 2 * TILE_SIZE, TILE_SIZE, TILE_SIZE
		)
		self.rect = Rect(origin, self.image.get_rect()[2:])
		self.particle = ((10, 10), (1, 2), "green", 2)


LAST_GENERATE = time.get_ticks()
def generate(particles, sprites):
	"""Get all sprites to emit particles"""
	global LAST_GENERATE
	if time.get_ticks() - LAST_GENERATE > 150:
		for sprite in sprites:
			particles.append(
				Particle((sprite.rect.centerx, sprite.rect.centery), *sprite.particle)
			)
		LAST_GENERATE = time.get_ticks()
		


def main():
	"""main function"""
	init()
	screen = display.set_mode(SCREEN)
	display.set_caption("Wolf Tracking Game")
	game_surface = Surface(MINIMUM)
	all_sprites = sprite.Group()
	player = Player("Wolf.png", (30, 30))
	all_sprites.add(player)
	for _ in range(10):
		all_sprites.add(
			Shroom(
				"GrassNDirt.png",
				(randint(0, 25) * TILE_SIZE, randint(0, 25) * TILE_SIZE),
			)
		)
	particles = Particles()
	bear = Bear("Bear.png", (200, 200), game_surface, particles)
	all_sprites.add(bear)
	clock = time.Clock()
	event_queue.pump()
	event = event_queue.wait(1)
	while event.type != QUIT:
		all_sprites.update()
		particles.collisions(game_surface.get_bounding_rect(), player)
		generate(particles, all_sprites)
		particles.update()
		game_surface.fill("black")
		all_sprites.draw(game_surface)
		particles.draw(game_surface)
		frame = transform.scale(game_surface, SCREEN)
		screen.blit(frame, (0, 0))
		display.flip()
		clock.tick(15)
		event_queue.pump()
		event = event_queue.wait(5)
	game_quit()


if __name__ == "__main__":
	main()
	sys.exit()
