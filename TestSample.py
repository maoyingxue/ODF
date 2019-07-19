# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:34:59 2019

@author: maoyingxue
"""

from Interface import *
import cv2
from constant import *
from utils import correct, getpoints


def testGridAnalyzer():
    resize_dir = 'origin_data/resize'
    if not os.path.exists(resize_dir):
        os.mkdir(resize_dir)
    resize_path = os.path.join(resize_dir, 'type4_3.jpg')
    img_path = "origin_data/test/type4_3.jpg"
    img = cv2.imread(img_path)
    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    frame_type = 4
    if img is None:
        print("Img is None.")

    points = getpoints.getPoints(img, frame_type)
    assert len(points) == 4
    img_corrected = correct.transform(img, points)
    cv2.imwrite(resize_path, img_corrected)
    info = {
        OUTER_COLOR: 'green',
        INNER_COLOR: 'red',
        ADDR: resize_path,
        POINTS: points
    }
    res = calGridInfo(info)
    print(res)


if __name__ == '__main__':
    testGridAnalyzer()
