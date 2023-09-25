"""particles"""
from itertools import permutations
from math import hypot
from pygame.math import Vector2
from pygame import Rect
from random import randint


def collider(particles):
	particles[0].collide(particles[1])


def surface_collder(particle_surface):
	particle_surface[0].collide(particle_surface[1])


def updator(particle):
	particle.update()


def clamp(lower, x, upper):
	return min(max(x, lower), upper)


MAX_SPEED = 2


class Particles(list):
	"""Particles list"""

	def collisions(self, surface, player):
		"""collisions"""
		for particle_0, particle_1 in permutations(self, 2):
			particle_0.collide(particle_1)
		for particle in self:
			particle.collide(surface)
			particle.smell_range(player)

	def update(self):
		"""Update particle nature"""
		for particle in self:
			if particle.decay == 0:
				self.remove(particle)
			particle.update()

	def draw(self, surface):
		"""Draw particles to surface"""
		for particle in self: # filter(lambda x: x.visible, self):
			surface.fill(particle.color, particle)


class Particle:
	"""Point pixel with inner and outer boundaries"""

	def __init__(self, position, vector, radius, color, decay=-1):
		self.pos = Vector2(*position)
		self.vector = Vector2(randint(-vector[0], vector[0]), randint(-vector[1], vector[1]))
		self.radius = radius
		self.visible = False
		self.color = color
		self.decay = decay

	def rect(self):
		"""rectangle"""
		return Rect(self.pos, (1, 1))

	def update(self):
		"""position update based on velocity"""
		self.vector.x = clamp(-MAX_SPEED, self.vector.x, MAX_SPEED)
		self.vector.y = clamp(-MAX_SPEED, self.vector.y, MAX_SPEED)
		self.pos.x += self.vector.x
		self.pos.y += self.vector.y
		self.decay -= 1

	def smell_range(self, player):
		"""Yes this should be in character code"""
		if player.cone.top > self.pos.y or self.pos.y > player.cone.bottom:
			self.visible = False
		elif player.cone.left > self.pos.x or self.pos.x > player.cone.right:
			self.visible = False
		else:
			self.visible = True

	def collide(self, body):
		"""collision physics"""
		if not isinstance(body, type(self)):
			if body.top > self.pos.y or self.pos.y > body.bottom:
				self.vector.y *= -1
			if body.left > self.pos.x or self.pos.x > body.right:
				self.vector.x *= -1
			self.pos.x = clamp(body.left, self.pos.x, body.right)
			self.pos.y = clamp(body.top, self.pos.y, body.bottom)
			return

		delta_x, delta_y = self.pos.x - body.pos.x, self.pos.y - body.pos.y
		delta = hypot(delta_x, delta_y)

		if delta < self.radius[1] + body.radius[1]:
			delta_vector_x = self.vector.x - body.vector.x
			delta_vector_y = self.vector.y - body.vector.y
			if delta > 0:
				_sin, _cos = delta_x / delta, delta_y / delta
				magnitude = (
					delta_x * delta_vector_x + delta_y * delta_vector_y
				) / delta
			else:
				_sin, _cos, magnitude = (0,) * 3
			new_delta_vector_x = -magnitude * _sin
			new_delta_vector_y = -magnitude * _cos
			if delta < self.radius[0] + body.radius[0]:
				self.vector.x -= new_delta_vector_x
				self.vector.y -= new_delta_vector_y
				body.vector.x += new_delta_vector_x
				body.vector.y += new_delta_vector_y
			else:
				self.vector.x += new_delta_vector_x
				self.vector.y += new_delta_vector_y
				body.vector.x -= new_delta_vector_x
				body.vector.y -= new_delta_vector_y
