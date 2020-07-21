#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pygame
import game_functions as gf

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien

def run_game():	

	pygame.init()
	
	ai_settings = Settings()
	# 创建一个名为screen的显示窗口
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	
	pygame.display.set_caption("Alien Invasion")

	ship = Ship(ai_settings, screen)

	alien = Alien(ai_settings, screen)
	
	bullets = Group()

	aliens = Group()

	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	while True:		
		gf.check_events(ai_settings, screen, ship, bullets)
		ship.update()
		gf.update_bullets(bullets)		
		gf.update_screen(ai_settings, screen, ship, aliens, bullets)

run_game()
