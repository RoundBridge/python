# -*- coding: utf-8 -*-
class Settings():
	def __init__(self):
		""" screen settings """
		self.screen_width = 1200
		self.screen_height= 640
		self.bg_color = (250, 250, 250)
		""" ship settings """
		self.ship_speed_factor = 1.5
		self.ship_limit = 2
		""" bulet settings """
		self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 10
		""" alien settings """
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 0.2
		self.fleet_direction = 1  # 外星人的移动方向，1向右，-1向左

