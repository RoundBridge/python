#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pygame.font


class Button():
    def __init__(self, ai_settings, screen, msg):
        '''初始化按钮的属性'''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        '''设置按钮的尺寸和其他属性'''
        self.width, self.height = 200, 50
        self.button_color = (100,100,100)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)  # 从系统字体库创建一个Font对象

        '''创建按钮的rect对象并使其居中'''
        self.rect = pygame.Rect(0,0,self.width,self.height)  # pygame.Rect(left, top, width, height)
        self.rect.center = self.screen_rect.center

        '''按钮的标签只需创建一次'''
        self.prep_msg(msg)

    def prep_msg(self, msg):
        '''将msg渲染为图像并使其在按钮上居中'''
        # draw text on a new Surface
        # 该函数创建一个新的 Surface 对象，并在上边渲染指定的文本。Pygame 没有提供直接的方式在一个
        # 现有的 Surface 对象上绘制文本，取而代之的方法是：使用 Font.render() 函数创建一个渲染了
        # 文本的图像（Surface 对象），然后将这个图像绘制到目标 Surface 对象上。
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)  # 先绘制一个用颜色填充的按钮
        self.screen.blit(self.msg_image, self.msg_image_rect)  # 再将文字绘制到按钮上

if __name__ == '__main__':
    pass

