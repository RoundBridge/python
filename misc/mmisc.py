#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import chardet
def get_encoding_type(file):
    '''
    :description: 获取文件编码类型
    :param file:  需要检测编码类型的文件
    :return:      字符串形式的编码类型
    '''
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f_obj:
        data = f_obj.read(16)
        return chardet.detect(data)['encoding']


def standardize_dir(dir):
    '''
        :param dir:
        :return: standardized dir
    '''
    ret = "./"
    if len(dir) == 0:
        return ret  # 若是空的，则返回当前工作目录作为默认目录
    else:
        ret = dir
        if dir[-1] == "/": # 传入的目录已经符合要求
            return ret
        elif dir[-1] == "\\" and dir[-2] == "\\":  # 传入的目录已经符合要求
            return ret
        else:
            ret = ret + "/"
            return ret


import re
import os
def find_str_in_file(filename, s):
    '''
        description:    判断某个字符串s是否在文件filename中
                        返回一个列表，列表元素是字符串s所在的行号
        version:        0.0.1
        date:           2020.9.8
    '''
    type = "utf-8"  # 默认采用utf-8
    encode_type = get_encoding_type(filename)
    if encode_type != "ascii":
        type = "gbk"
    ret = []
    with open(filename, 'r', encoding=type) as f_obj:
        # 将文件中的内容按行读入
        list_line = f_obj.readlines()
        for i in range(len(list_line)):
            match = re.findall(s, list_line[i])
            if match:
                ret.append(i+1)
    return ret


ret_find_str_in_dirs = {}
def find_str_in_dirs(dir, s):
    '''
        description:    判断某个字符串s在某个目录dir下的哪个文件中，如果dir下面存在目录，
                        则递归遍历每一个目录。
                        返回一个列表 {"文件名1"：行号，"文件名2"：行号，"文件名3"：行号，...}
        version:        0.0.1
        date:           2020.9.8
    '''
    global ret_find_str_in_dirs  # 采用全局变量保存返回值，防止变量在递归过程中被莫名篡改
    dir = standardize_dir(dir)
    list_dir = os.listdir(dir)
    # 利用map和lambda表达式将list_dir中的每个元素加上dir前缀，得到完整的路径名
    list_dir = list(map(lambda x:dir+x, list_dir))
    for ele in list_dir:
        if os.path.isdir(ele):
            path = standardize_dir(ele)
            # 递归处理path
            ret_find_str_in_dirs = find_str_in_dirs(path, s)
        else:
            r = find_str_in_file(ele, s)
            if r:
                ret_find_str_in_dirs[ele] = r
    return ret_find_str_in_dirs


if __name__ == '__main__':
    pass