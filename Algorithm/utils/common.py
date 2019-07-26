#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: 
@file: Common.py
@time: 2019-07-23 11:50
@version 1.0
@desc:
"""
from constant import *
import cv2
import math
import numpy as np
import json
import os
from Algorithm.utils.logging import logger


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
        return np.array(points_hand)

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


def queryType(outer_color="", inner_color="", frame_type=None):
    """
    从系统定义的颜色—类型转换表中查询机架的类别
    :param outer_color: 机架颜色
    :param inner_color: 卡槽颜色
    :param frame_type: 1~6
    :return:
    """
    # input_color_pair = [outer_color, inner_color]
    frame_type = -1
    if outer_color is "" or inner_color is "":
        msg = "Outer color and innter color are required."
        logger.error(msg)
        raise Exception(msg)
    for it_type, color_pair in TYPE_2_COLOR.items():
        # 机架色与卡槽色分别对应
        if color_pair[0] == outer_color and color_pair[1] == inner_color:
            frame_type = it_type
    if frame_type == -1:
        logger.warning('Unknown frame type for color composition: [{}, {}].'.format(outer_color, inner_color))
    return frame_type


def queryColor(frame_type, outer_color=None, inner_color=None):
    """
    从系统定义中查询机架类型对应的颜色
    :param frame_type: 输入机架的类型,输入整数
    :param outer_color:
    :param inner_color:
    :return:查询得到的颜色
    """
    # input_color_pair = [outer_color, inner_color]
    if frame_type is None:
        msg = "Frame type is required."
        logger.error(msg)
        raise Exception(msg)
    for it_type, color_pair in TYPE_2_COLOR.items():
        if it_type == frame_type:
            frame_type = it_type
            outer_color = color_pair[0]
            inner_color = color_pair[1]
    if outer_color is None or inner_color is None:
        logger.warning('Unknown frame type [{}].'.format(frame_type))
        return TYPE_2_COLOR[-1]
    return outer_color, inner_color


def getFrameType(img_name):
    """
    根据文件名获取机架类型,默认文件名的首个数字为机架类型
    :param img_name:
    :return:
    """
    filename, extention = os.path.splitext(img_name)
    return filename.split('_')[0]


def formatColor(config_base_dir):
    """
    根据机架类型格式化配置定义的颜色
    :param config_base_dir:
    :return:
    """
    config_base_dir = os.path.join(PROJECT_DIR, config_base_dir)
    dirs = os.listdir(config_base_dir)
    for config_dir in dirs:
        filename, extention = os.path.splitext(config_dir)
        if extention == '.json':
            config_file, original_config = buildWritableConfigFile(config_base_dir, config_dir)
            if filename == 'template':
                continue
            logger.info('Formatting [{}] .....'.format(config_dir))
            frame_type = int(filename.split('_')[0])
            outer_color, inner_color = queryColor(frame_type)
            if outer_color == UNKNOWN_STR or inner_color == UNKNOWN_STR:
                logger.error("Unknown frame type [{}]".format(frame_type))
            # 更新为系统定义的颜色
            original_config[OUTER_COLOR] = outer_color
            original_config[INNER_COLOR] = inner_color
            # 写回config
            config_file.write(json.dumps(original_config, indent=4))
            config_file.close()
            logger.info('Formatting [{}] done.'.format(config_dir))


def labelPoints(img_base_dir, config_base_dir, shrink=4):
    """
    标定图片四个点，把四个点存入对应的配置文件中以备测试
    图片名前缀必须与配置名前缀一致
    :param img_base_dir: 照片的基路径
    :param config_base_dir: 配置的基路径
    :param shrink:
    :return:
    """
    img_base_dir = os.path.join(PROJECT_DIR, img_base_dir)
    dirs = os.listdir(img_base_dir)
    config_dirs = os.listdir(config_base_dir)
    if not len(dirs):
        return
    for img_dir in dirs:
        filename, extention = os.path.splitext(img_dir)
        if extention == '.jpg' or extention == '.png':
            img_path = os.path.join(img_base_dir, img_dir)
            img = cv2.imread(img_path)
            # 方便标定，将图像缩小为原来的1/shrink
            img = cv2.resize(img, (0, 0), fx=1 / shrink, fy=1 / shrink)
            config_name = filename + '.json'
            if config_name in config_dirs:
                config_file, origin_config = buildWritableConfigFile(config_base_dir, config_name)
                frame_type = int(filename.split('_')[0])
                # 默认文件第一个数字为机架的类型
                if frame_type is not None:
                    # 恢复原来点坐标的倍数
                    points = getPoints(img, frame_type) * shrink
                    if 'points' in origin_config:
                        origin_config['points'] = points.tolist()
                        # 写回config
                        config_file.write(json.dumps(origin_config, indent=4))
                else:
                    raise TypeError("Unknown frame type.")


def buildWritableConfigFile(config_base_dir, config_name):
    """
    新建一个可写的config json对象
    :param config_base_dir:
    :param config_name:
    :return:
    """
    config_path = os.path.join(config_base_dir, config_name)
    # 读模式打开
    config_file = open(config_path)
    origin_config = json.load(config_file)
    config_file.close()
    # 写模式打开
    config_file = open(config_path, 'w')
    return config_file, origin_config
