import pygame

class Ship():
	def __init__(self, ai_settings, screen):
	
		self.screen = screen
		self.ai_settings = ai_settings

		# load返回一个表示飞船的surface
		self.image = pygame.image.load('images/level-1.bmp')
		self.rect = self.image.get_rect()
		# 表示屏幕的矩形
		self.screen_rect = screen.get_rect()

		# 将每艘新飞船放置在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		self.moving_right = False
		self.moving_left = False

		self.center = float(self.rect.centerx)  # 这个center当做临时变量用用的吧？

	def center_ship(self):
		self.center = self.screen_rect.centerx

	def blitme(self):
		''' 在指定位置绘制飞船 '''
		self.screen.blit(self.image, self.rect)

	def update(self):
		if self.moving_right and self.rect.right < self.screen_rect.right:
			#self.rect.centerx += 1
			self.center += self.ai_settings.ship_speed_factor
		elif self.moving_left and self.rect.left > 0:
			#self.rect.centerx -= 1
			self.center -= self.ai_settings.ship_speed_factor

		self.rect.centerx = self.center

