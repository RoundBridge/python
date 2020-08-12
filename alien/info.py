#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import pygame
import sys

VALID_CHAR = string.ascii_letters+string.digits+string.punctuation+" "
KEY_REPEAT_SETTING = (200, 50)
SCREEN_W = 500
SCREEN_H = 300
SCREEN_COLOR = (100, 100, 100)

class TextBox():
    def __init__(self, rect, **kwargs):
        self.rect = pygame.Rect(rect)  # Rect(left, top, width, height) -> Rect or Rect((left, top), (width, height)) -> Rect
        self.buffer = []
        self.final = None
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)
        self.make_box_label()


    def process_kwargs(self, kwargs):
        defaults = {"msg" : " ",
                    "bg_color" : pygame.Color("white"),
                    "label_font_color": (150, 150, 150),
                    "font_color" : pygame.Color("black"),
                    "font" : pygame.font.Font(None, self.rect.height+4)}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def make_box_label(self):
        message = self.msg
        self.font = pygame.font.SysFont("arial", 16)
        self.box_label = self.font.render(message, True, self.label_font_color)
        self.box_label_rect = self.box_label.get_rect()
        self.box_label_rect.left = self.rect.left
        self.box_label_rect.top = self.rect.top
        self.screen.fill(self.bg_color, self.rect)  # 先绘制一个用颜色填充的输入框
        self.screen.blit(self.box_label, self.box_label_rect)  # 再将标签提示文字绘制到输入框左端


class Login():
    def __init__(self):
        self.screen = self.prep_screen()
        self.done = False
        self.user = TextBox((SCREEN_W//2, 10, 150, 20), msg="User", screen=self.screen)
        self.password = TextBox((SCREEN_W//2, 60, 150, 20), msg="Password", screen=self.screen)
        self.register = TextBox((SCREEN_W//2, 110, 150, 20), msg="Register", screen=self.screen)
        self.anonymous = TextBox((SCREEN_W//2, 160, 150, 20), msg="Anonymous", screen=self.screen)
        self.login = TextBox((SCREEN_W//2, 210, 150, 20), msg="Login", screen=self.screen)
        # pg.key.set_repeat(*KEY_REPEAT_SETTING)  #加*号可以去掉KEY_REPEAT_SETTING外面的括号

    def prep_screen(self):
        pygame.init()
        pygame.display.set_caption("Welcome to Alien Invasion")
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        screen.fill(SCREEN_COLOR)
        return screen

    # def get_event(self, event):
    #     if event.type == pygame.KEYDOWN and self.active:
    #         if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
    #             self.execute()
    #         elif event.key == pygame.K_BACKSPACE:
    #             if self.buffer:
    #                 self.buffer.pop()
    #         elif event.unicode in VALID_CHAR:
    #             self.buffer.append(event.unicode)
    #     elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  #鼠标左键按下
    #         self.active = self.rect.collidepoint(event.pos)


if __name__ == '__main__':
    login = Login()
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

