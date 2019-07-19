#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: ODF
@file: grid_analyzer.py
@time: 2019-07-19 16:52
@version 1.0
@desc:
"""
from constant import *
from Algorithm.grid_analysis.orientation import regOrientationBatch
from Algorithm.grid_analysis.segment import Segmentation
from utils.logging import logger

import cv2


def queryTable(outer_color, inner_color, frame_type=None):
    """
    从系统定义的颜色—类型转换表中查询机架的类别
    :param outer_color:
    :param inner_color:
    :param frame_type: 1~6
    :return:
    """
    # input_color_pair = [outer_color, inner_color]
    frame_type = -1
    for it_type, color_pair in TYPE_2_COLOR.items():
        # 机架色与卡槽色分别对应
        if color_pair[0] == outer_color and color_pair[1] == inner_color:
            frame_type = it_type
    if frame_type == -1:
        logger.warning('Unknown frame type for color composition: [{}, {}].'.format(outer_color, inner_color))
    return frame_type


def analysis(info):
    """
    网格分析器,分析机架的行列信息和横竖排方向
    :param info: 输入图片地址、机架色、卡槽色、机架的边界点
    :return:
    """
    res = {}
    # 确保输入字段的完整性
    for key in GRID_ANALYZER_INPUT_KEYS:
        if key not in info:
            msg = '{} is required.'.format(key)
            logger.error(msg)
            raise Exception(msg)
    res = {
        IS_ROTATE: -1,
        ROW: -1,
        COL: -1
    }
    img_path = os.path.join(PROJECT_DIR, info[ADDR])
    img = cv2.imread(img_path)
    if img is None:
        logger.warning("Can load image from {}.".format(info[ADDR]))
        return res
    # 获取机架的光纤排布方向
    orientation = regOrientationBatch(img, info)
    if orientation == -1:
        logger.warning("Unknown orientation of frame.")
    frame_type = queryTable(info[OUTER_COLOR], info[INNER_COLOR])
    # 网格分割
    row, col = Segmentation(img, frame_type)
    res[IS_ROTATE] = orientation
    res[ROW] = row
    res[COL] = col
    return res
    # regOrientationBatch()


if __name__ == '__main__':
    pass
