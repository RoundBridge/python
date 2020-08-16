#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import string
import pygame
import json
import sys
import os

VALID_CHAR = string.ascii_letters+string.digits+string.punctuation+" "
KEY_REPEAT_SETTING = (200, 50)
SCREEN_W = 500
SCREEN_H = 300
SCREEN_COLOR = (100, 100, 100)

class TextBox():
    def __init__(self, rect, **kwargs):
        # Rect(left, top, width, height) -> Rect
        # Rect((left, top), (width, height)) -> Rect
        # Rect(object) -> Rect
        self.rect = pygame.Rect(rect)
        self.active = False  # 表示该TextBox当前是否被鼠标选中或者处于编辑状态
        self.buffer = []     # 键盘输入过程中作为临时列表保存输入的字符，会将其中的字符转化到final中的字符串
        self.final = None    # 表示该TextBox当前存储的字符串
        self.blink = True
        self.blink_timer = 0.0
        self.process_kwargs(kwargs)
        self.text_box_init()


    def process_kwargs(self, kwargs):
        defaults = {"msg": " ",
                    "bg_color": pygame.Color("white"),
                    "label_font_color": (150, 150, 150),
                    "font_color": pygame.Color("black"),
                    "font": " "}
        for kwarg in kwargs:
            defaults[kwarg] = kwargs[kwarg]
        self.__dict__.update(defaults)

    def text_box_init(self):
        font_size = 18
        font_bold = False
        message = self.msg
        if message != "User" and message != "Password":
            if message == "Login":
                font_size = 32
                font_bold = True
        self.font = pygame.font.SysFont("Arial", font_size)
        self.font.set_bold(font_bold)
        self.box_label = self.font.render(message, True, self.label_font_color, self.bg_color)
        self.box_label_rect = self.box_label.get_rect()
        self.box_label_rect.left = self.rect.left+2
        self.box_label_rect.centery = self.rect.centery
        if message != "User" and message != "Password":
            # 除了User和Password，其余的居中显示
            self.box_label_rect.center = self.rect.center
        self.screen.fill(self.bg_color, self.rect)#先绘制一个用颜色填充的输入框
        self.screen.blit(self.box_label, self.box_label_rect)#再将标签提示文字绘制到输入框左端

    def update_text_box_info(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            s = self.final
            if self.msg == "Password":
                s = len(self.buffer)*"*"
            self.text = self.font.render(s, True, self.font_color, self.bg_color)
            self.text_rect = self.text.get_rect(x=self.rect.x+2, centery=self.rect.centery)
            if self.text_rect.width > self.rect.width - 6:
                offset = self.text_rect.width - (self.rect.width - 6)
                self.text_display_rect = pygame.Rect(offset, 0, self.rect.width - 6, self.text_rect.height)
            else:
                self.text_display_rect = self.text.get_rect(topleft=(0, 0))

        if pygame.time.get_ticks() - self.blink_timer > 400:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def draw_text_box(self, surface):
        surface.fill(self.bg_color, self.rect)  #先清除掉上一次绘制的内容
        if not self.active and len(self.final) == 0:
            self.screen.blit(self.box_label, self.box_label_rect) # 未被选中且文本框中没有输入字符的情况下仍旧显示标签信息
        if self.text:
            # blit(source, dest, area=None, special_flags=0) -> Rect
            # An optional area rectangle can be passed as well. This
            # represents a smaller portion of the source Surface to draw.
            surface.blit(self.text, self.text_rect, self.text_display_rect)
        if self.blink and self.active:
            # copy() -> Surface  Makes a duplicate copy of a Surface.
            curse = self.text_display_rect.copy()
            curse.topleft = self.text_rect.topleft
            surface.fill(self.font_color, (curse.right+1, curse.y, 2, curse.h))


class Login():
    def __init__(self):
        self.screen = self.prep_screen()
        self.done = False
        self.active_text_box = " "
        self.text_box_obj = {}
        self.text_box_obj["user"] = TextBox((SCREEN_W * 3 // 5, 80, 180, 25), msg="User", screen=self.screen)
        self.text_box_obj["password"] = TextBox((SCREEN_W * 3 // 5, 120, 180, 25), msg="Password", screen=self.screen)
        self.text_box_obj["register"] = TextBox((SCREEN_W * 3 // 5, 160, 80, 25), msg="Register", screen=self.screen)
        self.text_box_obj["anonymous"] = TextBox((SCREEN_W * 3 // 5, 195, 80, 25), msg="Anonymous", screen=self.screen)
        self.text_box_obj["login"] = TextBox((SCREEN_W * 3 // 5 + 90, 160, 90, 60), msg="Login", screen=self.screen)
        self.font = pygame.font.SysFont("Arial", 16)
        self.font.set_bold(True)

    def show_hint(self, msg):
        if msg == "":
            # 该rect主要用于清空提示信息区域
            # 就是从anonymous按钮左下角开始到登陆界面右下角的这片区域
            rect = (self.text_box_obj["register"].rect.left,
                    self.text_box_obj["anonymous"].rect.bottom,
                    self.screen.get_rect().right-self.text_box_obj["register"].rect.left,
                    self.screen.get_rect().bottom-self.text_box_obj["anonymous"].rect.bottom)
            self.screen.fill(SCREEN_COLOR, rect)
        else:
            self.hint = self.font.render(msg, True, (210, 0, 0), SCREEN_COLOR)
            self.hint_rect = self.hint.get_rect()
            self.hint_rect.left = self.text_box_obj["register"].rect.left
            self.hint_rect.bottom = self.screen.get_rect().bottom
            self.screen.blit(self.hint, self.hint_rect)

    def prep_screen(self):
        pygame.init()
        pygame.display.set_caption("Welcome to Alien Invasion")
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        screen.fill(SCREEN_COLOR)
        pygame.key.set_repeat(*KEY_REPEAT_SETTING) #加*号去掉KEY_REPEAT_SETTING外面的括号
        return screen

    def update_mouse_click_info(self, pos):
        for key in self.text_box_obj.keys():
            self.text_box_obj[key].active = self.text_box_obj[key].rect.collidepoint(pos)

    def is_text_box_selected(self):
        ret = False
        for key in self.text_box_obj.keys():
            if self.text_box_obj[key].active:
                ret = True
                break
        return ret

    def find_text_box_selected(self):
        ret = ""
        for key in self.text_box_obj.keys():
            if self.text_box_obj[key].active:
                ret = key
                break
        return ret

    def execute(self, active_box):
        self.text_box_obj[active_box].final = "".join(self.text_box_obj[active_box].buffer)
        print("final string: ", self.text_box_obj[active_box].final)

    def proc_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.is_text_box_selected():
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self.execute(self.active_text_box)
                elif event.key == pygame.K_BACKSPACE:
                    if self.text_box_obj[self.active_text_box].buffer:
                        self.text_box_obj[self.active_text_box].buffer.pop()
                elif event.unicode in VALID_CHAR and event.unicode != "": #不等于""用来排除中文输入
                    self.text_box_obj[self.active_text_box].buffer.append(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #鼠标左键按下
                self.update_mouse_click_info(event.pos)
                self.active_text_box = self.find_text_box_selected()
                if self.active_text_box == "register":
                    if len(self.text_box_obj["user"].final) == 0 or len(self.text_box_obj["password"].final) == 0:
                        self.show_hint(msg="Input user and password")
                    else:
                        self.show_hint(msg="")
                        self.done = self.register_user()
                elif self.active_text_box == "login":
                    self.done = True
                elif self.active_text_box == "anonymous":
                    self.done = True
                else:
                    pass

    def get_stored_users(self):
        users = []
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
                list_new.append(dict_new_record)
                json.dump(list_new, obj, ensure_ascii=False)
                return users
        else:
            for d in list_record[1:]:
                users.append(d['name'])
            return users

    def register_user(self):
        users = self.get_stored_users()
        new_user = self.text_box_obj["user"].final
        new_user_password = self.text_box_obj["password"].final
        with open('./misc/record.json', 'r', encoding='utf8') as f_obj:
            list_record = json.load(f_obj)
        if new_user in users:
            self.show_hint(msg="User exists")
            # # 用户存在，密码改成用户最新设置(暂时不支持)
            # i = users.index(new_user) + 1
            # list_record[i]["password"] = new_user_password
            # with open('./misc/record.json', 'w', encoding='utf8') as f_obj:
            #     json.dump(list_record, f_obj, ensure_ascii=False)
            return False
        else:
            dict_new_user = {}
            dict_new_user["name"] = new_user
            dict_new_user["password"] = new_user_password
            dict_new_user['score'] = 0
            dict_new_user['time'] = ''
            list_record.append(dict_new_user)
            with open('./misc/record.json', 'w', encoding='utf8') as f_obj:
                json.dump(list_record, f_obj, ensure_ascii=False)
            self.show_hint(msg="Register OK")
            return True

    def update_screen(self):
        for key in self.text_box_obj.keys():
            if key == "user" or key == "password":
                self.text_box_obj[key].update_text_box_info()
                self.text_box_obj[key].draw_text_box(self.screen)
        pygame.display.update()



if __name__ == '__main__':
    login = Login()
    while not login.done:
        login.proc_event()
        login.update_screen()
    pygame.quit()
    sys.exit()

