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
from Algorithm.utils.logging import logger
from Algorithm.utils import common
import cv2
import time


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
    # img_path = os.path.join(PROJECT_DIR, IMG_DIR, info[ADDR])
    img_path = IMG_DIR + "/" + info[ADDR]
    img = cv2.imread(img_path)
    if img is None:
        logger.error("Cannot load image from [{}].".format(info[ADDR]))
        return res
    logger.debug("Analysis image: [{}]..........".format(info[ADDR]))
    img = common.transform(img, info[POINTS])
    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    # 获取机架的光纤排布方向
    orientation = regOrientationBatch(img, info)
    if orientation == -1:
        logger.warning("Image :[{}]: Unknown orientation of frame.".format(info[ADDR]))
    frame_type = common.queryType(info[OUTER_COLOR], info[INNER_COLOR])
    if frame_type == -1:
        logger.info("Image: [{}]: Unknown frame type.".format(info[ADDR]))
        return res
    # 网格分割
    try:
        start = time.time()
        row, col = Segmentation(img, frame_type)
        end = time.time() - start
        logger.info("Time consumption: [{}]........".format(end))
    except:
        row = -1
        col = -1
    finally:
        res[IS_ROTATE] = orientation
        res[ROW] = row
        res[COL] = col
        logger.debug("Analysis image done: [{}]..........".format(info[ADDR]))
        logger.info("Image [{}]: Grid Analysis result: [{}].".format(info[ADDR], res))
        return res
    # regOrientationBatch()


if __name__ == '__main__':
    pass
