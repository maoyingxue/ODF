#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: correct.py
@time: 2019-07-19 21:08
@version 1.0
@desc:
"""
import cv2
import math
import numpy as np


def getHigh(points_list):
    """
    # 用于计算透射变换的高
    :param points_list: 四个顶点的列表
    """
    h1 = math.sqrt((points_list[0][0] - points_list[3][0]) * (points_list[0][0] - points_list[3][0]) +
                   (points_list[0][1] - points_list[3][1]) * (points_list[0][1] - points_list[3][1]))
    h2 = math.sqrt((points_list[1][0] - points_list[2][0]) * (points_list[1][0] - points_list[2][0]) +
                   (points_list[1][1] - points_list[2][1]) * (points_list[1][1] - points_list[2][1]))
    return int(max(h1, h2))


def getWidth(points_list):
    """
    # 用于计算透射变换的宽
    :param points_list: 四个顶点的列表
    """
    w1 = math.sqrt((points_list[0][0] - points_list[1][0]) * (points_list[0][0] - points_list[1][0]) +
                   (points_list[0][1] - points_list[1][1]) * (points_list[0][1] - points_list[1][1]))
    w2 = math.sqrt((points_list[2][0] - points_list[3][0]) * (points_list[2][0] - points_list[3][0]) +
                   (points_list[2][1] - points_list[3][1]) * (points_list[2][1] - points_list[3][1]))
    return int(max(w1, w2))


def transform(image, points):
    """
    # 图像扶正
    :param image: 待扶正的图片
    :return: 扶正后的图片
    """
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [getWidth(points), 0], [getWidth(points), getHigh(points)], [0, getHigh(points)]])
    p = cv2.getPerspectiveTransform(pts1, pts2)
    image_change = cv2.warpPerspective(image, p, (getWidth(points), getHigh(points)))
    return image_change



