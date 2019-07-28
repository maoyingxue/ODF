# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:35:32 2019

@author: maoyingxuex
"""
"""
info:为接口定义的json输入文件
results：为定义的json输出文件
"""
from Algorithm.grid_analysis import grid_analyzer
from Algorithm.port_classification import get_port_classification_result
from Algorithm.classification.classify import Classify
from constant import TYPE_2_COLOR, IMG_PATH
from Algorithm.getpoints.points import calpoints
import cv2
import uuid

# 计算元分类
cls = Classify()
def calType(img):
    # 输入图片
    types = cls.predict(img)
    color = TYPE_2_COLOR[int(types)]
    # print(color)
    results = {}
    results["outerColor"] = color[0]
    results["innerColor"] = color[1]
    unique_filename = str(uuid.uuid4())
    addr=IMG_PATH+"/"+types+"_"+unique_filename+".jpg"
    cv2.imwrite(addr,img)
    results["addr"]=addr
    return results


# 计算边界点
def calPoints(info):
    results = {}
    results["points"] = calpoints(info)
    return results


# 计算行列信息
def calGridInfo(info):
    return grid_analyzer.analysis(info)


# 计算端口信息
def predictPorts(info):
    return get_port_classification_result(info)
