from pygame import (
	display, sprite, Surface, key, init, time, math,
	quit, transform, image, Rect, gfxdraw, event as event_queue)
from pygame.math import Vector2
from pygame.locals import (
	K_LEFT, K_RIGHT, K_UP, K_DOWN, K_w, K_a, K_s, K_d, K_LSHIFT, QUIT)
from sys import exit
from collections import namedtuple
from itertools import permutations
from math import hypot
from random import randint
from multiprocessing import Pool

size = namedtuple("size", "width height")
SCREEN = size(600, 600)
MINIMUM = size(400, 400)
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

class Particles(list):
	def update(self):
		for particle_0, particle_1 in permutations(self, 2):
			particle_0.collide(particle_1)
	
	def draw(self, surface):
		for particle in self:
			surface.fill("green", particle)

class Particle:
	def __init__(self, position, vector, radius):
		self.pos = Vector2(*position)
		self.vector = Vector2(*vector)
		self.radius = namedtuple("radius", "inner outer")(*radius)
	
	def rect(self):
		return Rect(self.pos, (1, 1))
	
	def update(self):
		pass
	
	def collide(self, body):
		delta_x, delta_y = self.pos.x - body.pos.x, self.pos.y - body.pos.y
		delta = hypot(delta_x, delta_y)
		
		if delta < self.radius.outer + body.radius.outer:
			delta_vector_x = self.vector.x - body.vector.x
			delta_vector_y = self.vector.y - body.vector.y
			try:
				_sin = delta_x / delta
			except ZeroDivisionError:
				_sin = 0
			try:
				_cos = delta_y / delta
			except ZeroDivisionError:
				_cos = 0
			delta_radius = (self.radius.outer + body.radius.outer - delta) / 2
			delta_x_2, delta_y_2 = _sin * delta_radius, _cos * delta_radius
			try:
				h = (delta_x * delta_vector_x + delta_y * delta_vector_y) / delta
			except ZeroDivisionError:
				h = 0
			new_delta_vector_x, new_delta_vector_y = -h * _sin, -h * _cos
			if delta < self.radius.inner + body.radius.inner:
				self.pos.x += delta_x_2
				self.pos.y += delta_y_2
				body.pos.x -= delta_x_2
				body.pos.y -= delta_y_2
				self.vector.x += new_delta_vector_x
				self.vector.y += new_delta_vector_y
				body.vector.x -= new_delta_vector_x
				body.vector.y -= new_delta_vector_y
			else:
				self.pos.x -= delta_x_2
				self.pos.y -= delta_y_2
				body.pos.x += delta_x_2
				body.pos.y += delta_y_2
				self.vector.x -= new_delta_vector_x
				self.vector.y -= new_delta_vector_y
				body.vector.x += new_delta_vector_x
				body.vector.y += new_delta_vector_y
		

class Shroom(sprite.Sprite):
	def __init__(self, image_path, frame_size, init_position):
		super().__init__()
		surface = image.load(image_path).convert_alpha()
		self.image = surface.subsurface(
			3 * frame_size, 2 * frame_size, frame_size, frame_size)
		self.rect = Rect(
			init_position, self.image.get_rect()[2:])


class Player(sprite.Sprite):
	def __init__(self, image_path, frame_size):
		super().__init__()
		self.sprite_sheet = image.load(image_path).convert_alpha()
		self.current_frame = 0
		self.state = RIGHT_IDLE
		self.run = False
		self.frame_size = frame_size
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

def main():
	init()
	screen = display.set_mode(SCREEN)
	display.set_caption("Wolf Tracking Game")
	game_surface = Surface((200, 200))
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
	particles = Particles()
	for _ in range(400):
		particles.append(
			Particle(
				(randint(0, 200), randint(0, 200)),
				(randint(0, 1), randint(0, 1)),
				(1, 2)
			)
		)
	clock = time.Clock()
	event_queue.pump()
	event = event_queue.wait(1)
	while event.type != QUIT:
		all_sprites.update()
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
	quit()
	exit()


if __name__ == "__main__":
	main()
