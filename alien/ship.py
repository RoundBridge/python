import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# load返回一个表示飞船的surface
		self.image = pygame.image.load('images/level-1.png')
		self.mask = pygame.mask.from_surface(self.image)
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
		# 及时更新飞船的rect，防止发生ship_hit后没有更新（update）飞船的位置就去画飞船
		# 这样的话，子弹就始终是从飞船前方发射的，而不是飞船已移到中间，而子弹却还是在其他
		# 位置发射出来。屏幕上绘制飞船的位置最终是由rect决定的，而不是center决定的
		self.rect.centerx = self.screen_rect.centerx
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


class Icon_Ship(Sprite):
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# 屏幕左上角表示剩余飞船数的图标
		self.image = pygame.image.load('images/level-1-icon.png')
		self.mask = pygame.mask.from_surface(self.image)
		self.rect = self.image.get_rect()

		# 表示屏幕的矩形
		self.screen_rect = screen.get_rect()
		# 表示图标的顶部位置
		self.rect.top = self.screen_rect.top
