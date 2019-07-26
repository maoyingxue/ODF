#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: ODF
@file: constant.py
@time: 2019-07-19 16:58
@version 1.0
@desc: 定义了系统全局配置信息
"""
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
#测试图片存储路径
IMG_DIR = 'stores/images'
CONFIG_DIR = 'stores/config'
#图片自定义存储路径
IMG_PATH=''
# 机架颜色的字符串常量
BLUE_STR = 'blue'
RED_STR = 'red'

## 接口输入JSON的键值常量

ADDR = 'addr'  # 图片路径
OUTER_COLOR = 'outerColor'  # 机架颜色
INNER_COLOR = 'innerColor'  # 卡槽色
POINTS = 'points'  # 机架边界点
IS_ROTATE = 'isRotate'  # 横竖排
ROW = 'row'  # 机架行数
COL = 'col'  # 机架列数

GRID_ANALYZER_INPUT_KEYS = [OUTER_COLOR, INNER_COLOR, ADDR, POINTS]
UNKNOWN_STR = 'Unknown'
# 类型_颜色对照表
TYPE_2_COLOR = {1: ["cyan", "red"],
                2: ["black", "red"],
                3: ["green", "blue"],
                4: ["green", "red"],
                5: ["gray", "blue"],
                6: ["blue", "red"],
                -1: [UNKNOWN_STR, UNKNOWN_STR]
                }

# 颜色对应的hsv范围
HSV_COLOR_RANGE = {"black": [[0, 180], [0, 255], [0, 46]],
                   "grey": [[0, 180], [0, 43], [46, 220]],
                   "white": [[0, 180], [0, 30], [221, 255]],
                   "red": [[0, 10, 156, 180], [43, 255], [46, 255]],
                   "orange": [[11, 25], [43, 255], [46, 255]],
                   "yellow": [[26, 34], [43, 255], [46, 255]],
                   "green": [[35, 77], [43, 255], [46, 255]],
                   "cyan": [[78, 103], [43, 255], [46, 255]],
                   "blue": [[100, 124], [43, 255], [46, 255]],
                   "purple": [[125, 155], [43, 255], [46, 255]]
                   }
