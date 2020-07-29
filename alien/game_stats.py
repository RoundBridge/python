#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GameStats():
    '''跟踪游戏的统计信息'''
    def __init__(self, ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.game_active = False
        self.ships_left = self.ai_settings.ship_limit

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit

