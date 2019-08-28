# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:34:59 2019

@author: maoyingxue
"""

from Interface import *
from constant import *
import os
import cv2
import json
from Algorithm.utils import common


def TestcalType():
    files = os.listdir(IMG_DIR)
    for file in files:
        img = cv2.imread(IMG_DIR + "/" + file)
        results = calType(img)
        print(file, results)


def TestcalPoints():
    configs = os.listdir(CONFIG_DIR)
    for config in configs:
        print(config)
        info = json.load(open(CONFIG_DIR + "/" + config))
        print(info)
        result = calPoints(info)
        print(result)


def testGridAnalyzer():
    img_dirs = os.listdir(IMG_DIR)
    cfg_dirs = os.listdir(CONFIG_DIR)

    for img_dir in img_dirs:
        img_filename, extention = os.path.splitext(img_dir)
        if extention == '.jpg' or extention == '.png':
            cfg_dir = img_filename + '.json'
            if cfg_dir not in cfg_dirs:
                raise Exception('Test must be specified a corresponding config for every image.')
            config_path = os.path.join(CONFIG_DIR, cfg_dir)
            info = json.load(open(config_path))
            res = calGridInfo(info)
            print(res)


def testPredictPorts():
    img_dirs = os.listdir(IMG_DIR)
    cfg_dirs = os.listdir(CONFIG_DIR)

    for img_dir in img_dirs:
        print(img_dir)
        img_filename, extention = os.path.splitext(img_dir)
        if extention == '.jpg' or extention == '.png':
            cfg_dir = img_filename + '.json'
            if cfg_dir not in cfg_dirs:
                raise Exception('Test must be specified a corresponding config for every image.')
            config_path = os.path.join(CONFIG_DIR, cfg_dir)
            info = json.load(open(config_path))
            res = predictPorts(info)
            print(res)


def overall():
    files = os.listdir(IMG_DIR)
    for file in files:
        print(file)
        img = cv2.imread(IMG_DIR + "/" + file)
        results = calType(img)
        print(results)
        results.update(calPoints(results))
        print(results)
        results.update(calGridInfo(results))
        print(results)
        results.update(predictPorts(results))
        print(results)


IMG_BASE_DIR = os.path.join(PROJECT_DIR, IMG_DIR_TWO)
CONFIG_BASE_DIR = os.path.join(PROJECT_DIR,CONFIG_DIR_TWO)
if __name__ == '__main__':
    common.labelPoints(IMG_BASE_DIR, CONFIG_BASE_DIR)
    # common.formatColor(config_base_dir)
    # TestcalType()
    # TestcalPoints()
    # testGridAnalyzer()
    # testPredictPorts()
    # overall()
