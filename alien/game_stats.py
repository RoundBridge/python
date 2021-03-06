#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class GameStats():
    '''跟踪游戏的统计信息'''
    def __init__(self, ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.player = 'administrator'
        self.game_active = False
        self.game_pause = False
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.high_score = 0
        self.score_record = 0
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

