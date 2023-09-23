from pygame.math import Vector2
from pygame import Rect
from collections import namedtuple
from itertools import permutations
from math import hypot

class Particles(list):
	"""Particles list"""

	def update(self):
		"""Update particle nature"""
		for particle_0, particle_1 in permutations(self, 2):
			particle_0.collide(particle_1)
		for particle in self:
			particle.update()

	def draw(self, surface):
		"""Draw particles to surface"""
		for particle in self:
			surface.fill("green", particle)


class Particle:
	"""Point pixel with inner and outer boundaries"""

	def __init__(self, position, vector, radius):
		self.pos = Vector2(*position)
		self.vector = Vector2(*vector)
		self.radius = namedtuple("radius", "inner outer")(*radius)

	def rect(self):
		"""rectangle"""
		return Rect(self.pos, (1, 1))

	def update(self):
		"""position update based on velocity"""
		self.pos.x += self.vector.x
		self.pos.y += self.vector.y

	def collide(self, body):
		"""collision physics"""
		delta_x, delta_y = self.pos.x - body.pos.x, self.pos.y - body.pos.y
		delta = hypot(delta_x, delta_y)

		if delta < self.radius.outer + body.radius.outer:
			delta_vector_x = self.vector.x - body.vector.x
			delta_vector_y = self.vector.y - body.vector.y
			if delta > 0:
				_sin = delta_x / delta, delta_y / delta
				magnitude = (
					delta_x * delta_vector_x + delta_y * delta_vector_y
				) / delta
			else:
				_sin, _cos = float_info.min, float_info.min
				magnitude = float_info.min
			new_delta_vector_x = -magnitude * _sin
			new_delta_vector_y = -magnitude * _cos
			if delta < self.radius.inner + body.radius.inner:
				self.vector.x -= new_delta_vector_x
				self.vector.y -= new_delta_vector_y
				body.vector.x += new_delta_vector_x
				body.vector.y += new_delta_vector_y
			else:
				self.vector.x += new_delta_vector_x
				self.vector.y += new_delta_vector_y
				body.vector.x -= new_delta_vector_x
				body.vector.y -= new_delta_vector_y

