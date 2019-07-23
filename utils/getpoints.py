#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: getpoints.py
@time: 2019-07-19 21:47
@version 1.0
@desc:
"""
import cv2
import math
import numpy as np


def drawPoints(event, x, y, flags, param):
    """
    # 手工标定四个顶点，参数为默认
    """
    if event == cv2.EVENT_LBUTTONDOWN and len(points_hand) < 4:
        cv2.circle(img_hand_copy, (x, y), 5, (0, 0, 255), 1)
        cv2.imshow("origin", img_hand_copy)
        # cv2.waitKey(0)
        points_hand.append(np.array([x, y]))
        print(points_hand)


def getPoints(image, odf_type, method="hand"):
    """
    # 得到机架的四个顶点
    :param image: 原始图片
    :param odf_type：机架的类型
    :param method: 计算方法
    :return: 四个顶点
    """
    if method == "hand":
        global img_hand, img_hand_copy, points_hand
        img_hand = image
        img_hand_copy = img_hand.copy()
        points_hand = []
        while True:
            cv2.namedWindow("origin")
            cv2.imshow("origin", img_hand)
            cv2.setMouseCallback('origin', drawPoints)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            if len(points_hand) != 4:
                print("Points set size must be 4 for correction.")
            else:
                break
        return points_hand

    if method == 'auto':
        # if odf_type == '1':
        #     points_hand = type1.getpoint(image)
        # elif odf_type == '2':
        #     points_hand = type2.getpoint(image, 'res/type2_6.txt')
        # elif odf_type == '3':
        #     points_hand = type3.getpoint(image)
        # elif odf_type == '4':
        #     points_hand = type4.getpoint(image)
        # else:
        #     print("该算法还未更新！")
        #     points_hand = []
        # TODO
        return points_hand
