#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime
import pygame.font
from pygame.sprite import Group
from ship import Ship, Icon_Ship

class Scoreboard():
    """显示得分信息的类"""
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        """显示得分信息时使用的字体设置"""
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 32)

        """准备读取分数记录"""
        self.read_record()
        """准备初始得分图像"""
        self.prep_score()
        """准备最高得分图像"""
        self.prep_record_score()
        """准备等级"""
        self.prep_level()
        """准备余下的飞机数"""
        self.prep_ships()



    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        score_str = "Score:" + "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        """将得分放在屏幕右上角"""
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.width * 4 / 5
        self.score_rect.top = self.screen_rect.top

    def prep_record_score(self):
        if self.stats.score_record > self.stats.high_score:
            score = self.stats.score_record
        else:
            score = self.stats.high_score
        high_score_str = "Score Record:" + "{:,}".format(score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        self.level_image = self.font.render("Level:" + str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        # 将等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right
        self.level_rect.top = self.screen_rect.top

    def prep_ships(self):
        self.icon_ships = Group()
        for ship_number in range(self.stats.ships_left):
            icon_ship = Icon_Ship(self.ai_settings, self.screen)
            icon_ship.rect.x = 4 + ship_number * icon_ship.rect.width
            icon_ship.rect.y = 4
            self.icon_ships.add(icon_ship)

    def show_score(self):
        """在屏幕上显示当前得分和最高得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.icon_ships.draw(self.screen)

    def store_record(self):
        # [{"winner":"XXX", "password":"XXX", "time":"XXX", "score":"XXX"},...]
        find = False
        t = datetime.now()
        moment = str(t.year)+'-'+str(t.month)+'-'+str(t.day)+' '+str(t.hour)+':'+str(t.minute)+':'+str(t.second)
        dict_new_record = {}
        with open('./misc/record.json', 'r', encoding='utf8') as f_obj:
            list_record = json.load(f_obj)

        for dict_record in list_record[1:]:
            if dict_record['name'] == self.stats.player:
                i = list_record.index(dict_record)
                # 即使没有产生新纪录，但是如果比该用户之前的最高分要高，则更新该用户的最高分
                if list_record[i]['score'] < self.stats.score:
                    list_record[i]['score'] = self.stats.score
                    list_record[i]['time'] = moment
                find = True
                break

        if not find:
            dict_new_record['name'] = self.stats.player
            dict_new_record['score'] = self.stats.score
            dict_new_record['time'] = moment
            list_record.append(dict_new_record)

        if self.stats.score_record < self.stats.score:  # 有新纪录诞生
            list_record[0]['winner'] = self.stats.player
            list_record[0]['score'] = self.stats.score
            list_record[0]['time'] = moment
        with open('./misc/record.json', 'w', encoding='utf8') as f_obj:
            json.dump(list_record, f_obj, ensure_ascii=False)

    def read_record(self):
        try:
            with open('./misc/record.json', 'r', encoding='utf8') as f_obj:
                list_record = json.load(f_obj)
        except:
            if not os.path.exists('./misc/'):
                os.makedirs('./misc/')
            with open('./misc/record.json', 'w', encoding='utf8') as obj:
                list_new = []
                dict_new_record = {}
                dict_new_record['winner'] = ''
                dict_new_record['password'] = ''
                dict_new_record['score'] = 0
                dict_new_record['time'] = ''
                self.stats.score_record = 0
                list_new.append(dict_new_record)
                json.dump(list_new, obj, ensure_ascii=False)
                print("record.json created OK!")
        else:
            self.stats.score_record = list_record[0]['score']
            print("prep_record OK, score_record=", self.stats.score_record)


if __name__ == '__main__':
    pass