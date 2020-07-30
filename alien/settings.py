# -*- coding: utf-8 -*-
class Settings():
	def __init__(self):
		""" screen settings """
		self.screen_width = 1200
		self.screen_height= 680
		self.bg_color = (250, 250, 250)
		""" ship settings """
		self.ship_limit = 2
		""" bulet settings """
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 10
		""" alien settings """
		self.fleet_drop_speed = 0.2

		self.speedup_scale = 1.1  # 以什么样的速度加快游戏节奏
		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		'''初始化随游戏进行而变化的设置'''
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1  # 外星人的移动方向，1向右，-1向左


	def increase_speed(self):
		'''提高速度设置'''
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

