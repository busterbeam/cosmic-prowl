from pygame import sprite, Rect, image, key

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

class Character(sprite.Sprite):
	"""Player Sprite"""

	def __init__(self, image_path, origin):
		"""Initializer"""
		super().__init__()
		self.sprite_sheet = image.load(image_path).convert_alpha()
		self.cone = Rect(0, 0, TILE_SIZE, TILE_SIZE)
		self.current_frame = 0
		self.state = RIGHT_IDLE
		self.run = (1, 4)
		self.update_frames()
		self.image = self.frames[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.centerx = origin[0]
		self.rect.centery = origin[1]

	def update_frames(self):
		"""Change what frames are being used for the animation"""
		self.frames = []
		for i in range(4):
			self.frames.append(
				self.sprite_sheet.subsurface(
					Rect(
						i * TILE_SIZE,
						self.state * TILE_SIZE,
						TILE_SIZE, TILE_SIZE,
					)
				)
			)
	
	def right(self):
		self.rect.x += PLAYER_SPEED * self.run[0]
		self.state = RIGHT_WALKING + self.run[1]
	
	def left(self):
		self.rect.x -= PLAYER_SPEED * self.run[0]
		self.state = LEFT_WALKING + self.run[1]
	
	def up(self):
		self.rect.y -= PLAYER_SPEED * self.run[0]
		self.state = UP_WALKING + self.run[1]
	
	def down(self):
		self.rect.y += PLAYER_SPEED * self.run[0]
		self.state = DOWN_WALKING + self.run[1]
	
	def idle(self):
		self.run = (1, 0)
		if self.state >= 4:
			self.state = max(0, self.state - 4)

class Player(Character):
	"""Player Sprite"""

	def __init__(self, image_path, origin):
		"""Initializer"""
		super().__init__(image_path, origin)
		self.particle = ((0, 0), (2, 16), "pink", 20)
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

	def update(self):
		"""Overwrite of Sprite updating"""
		keys = key.get_pressed()
		if any(keys):
			if keys[K_LSHIFT]:
				self.run = (2, 4)
			if keys[K_RIGHT] or keys[K_d]:
				self.right()
			elif keys[K_LEFT] or keys[K_a]:
				self.left()
			elif keys[K_DOWN] or keys[K_s]:
				self.down()
			elif keys[K_UP] or keys[K_w]:
				self.up()
			else:
				self.idle()
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

