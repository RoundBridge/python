#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pygame
import game_functions as gf
from info import Login
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button

def run_game():	

	login = Login()

	gf.process_login(login)

	pygame.init()
	
	ai_settings = Settings()
	# 创建一个名为screen的显示窗口
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	
	pygame.display.set_caption("Alien Invasion")

	play_button = Button(ai_settings, screen, "Play")

	stats = GameStats(ai_settings)

	sb = Scoreboard(ai_settings, screen, stats)

	ship = Ship(ai_settings, screen)
	
	bullets = Group()

	aliens = Group()

	gf.create_fleet(ai_settings, screen, ship, aliens)

	while True:		
		gf.check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()
