from pygame.math import Vector2
from pygame import Rect
from collections import namedtuple
from itertools import permutations
from math import hypot
from sys import float_info

def clamp(lower, x, upper):
	return min(max(x, lower), upper)

MAX_SPEED = 2

class Particles(list):
	"""Particles list"""
	
	def collisions(self, surface):
		for particle_0, particle_1 in permutations(self, 2):
			particle_0.collide(particle_1)
		for particle in self:
			particle.collide(surface)

	def update(self):
		"""Update particle nature"""
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
		self.vector.x = clamp(-MAX_SPEED, self.vector.x, MAX_SPEED)
		self.vector.y = clamp(-MAX_SPEED, self.vector.y, MAX_SPEED)
		self.pos.x += self.vector.x
		self.pos.y += self.vector.y


	def collide(self, body):
		"""collision physics"""
		if not isinstance(body, type(self)):
			if body.top > self.pos.y or self.pos.y > body.bottom:
				self.vector.y *= -1
			elif body.left > self.pos.x or self.pos.x > body.right:
				self.vector.x *= -1
			self.pos.x = clamp(body.left, self.pos.x, body.right)
			self.pos.y = clamp(body.top, self.pos.y, body.bottom)
			return
			
		delta_x, delta_y = self.pos.x - body.pos.x, self.pos.y - body.pos.y
		delta = hypot(delta_x, delta_y)

		if delta < self.radius.outer + body.radius.outer:
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

