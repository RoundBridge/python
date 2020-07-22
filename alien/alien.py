import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# pygame.image.save(screen, image_name)  # 可以保存screen上的图片到image_name中
		self.image = pygame.image.load('images/Alien-1.png')
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(0)
		self.y = float(0)

	def blitme(self):
		self.screen.blit(self.image, self.rect)

		# 重写基类Sprite中的update方法
	def update(self):
		self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
		self.rect.x = self.x
		self.y += self.ai_settings.fleet_drop_speed  # 让外星人在移动的过程中一直缓慢下降，而不是碰到边缘才下降
		self.rect.y = self.y

	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:  # reach the right side of the screen
			return True
		elif self.rect.left <= screen_rect.left:  # reach the left side of the screen
			return True
		else:
			return False


