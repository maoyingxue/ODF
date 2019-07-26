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

img_base_dir = os.path.join('stores', 'images')
config_base_dir = os.path.join('stores', 'config')


def TestcalType():
    files = os.listdir(img_base_dir)
    for file in files:
        img = cv2.imread(img_base_dir + "/" + file)
        results = calType(img)
        print(file, results)


def TestcalPoints():
    configs = os.listdir(config_base_dir)
    for config in configs:
        print(config)
        with open(config_base_dir + "/" + config, 'r') as load_f:
            load_dict = json.load(load_f)
        print(load_dict)
        result = calPoints(load_dict)
        print(result)


def testGridAnalyzer():
    img_abs_dir = os.path.join(PROJECT_DIR, img_base_dir)
    cfg_abs_dir = os.path.join(PROJECT_DIR, config_base_dir)

    img_dirs = os.listdir(img_abs_dir)
    cfg_dirs = os.listdir(cfg_abs_dir)

    for img_dir in img_dirs:
        img_filename, extention = os.path.splitext(img_dir)
        if extention == '.jpg' or extention == '.png':
            cfg_dir = img_filename + '.json'
            if cfg_dir not in cfg_dirs:
                raise Exception('Test must be specified a corresponding config for every image.')
            config_path = os.path.join(cfg_abs_dir, cfg_dir)
            info = json.load(open(config_path))
            res = calGridInfo(info)
            print(res)


def testPredictPorts():
    img_abs_dir = os.path.join(PROJECT_DIR, img_base_dir)
    cfg_abs_dir = os.path.join(PROJECT_DIR, config_base_dir)

    img_dirs = os.listdir(img_abs_dir)
    cfg_dirs = os.listdir(cfg_abs_dir)

    for img_dir in img_dirs:
        print(img_dir)
        img_filename, extention = os.path.splitext(img_dir)
        if extention == '.jpg':
            cfg_dir = img_filename + '.json'
            if cfg_dir not in cfg_dirs:
                raise Exception('Test must be specified a corresponding config for every image.')
            config_path = os.path.join(cfg_abs_dir, cfg_dir)
            info = json.load(open(config_path))
            res = predictPorts(info)
            print(res)


def overall():
    files = os.listdir(img_base_dir)
    for file in files:
        print(file)
        img = cv2.imread(img_base_dir + "/" + file)
        results = calType(img)
        results["addr"] = file
        print(results)
        results.update(calPoints(results))
        print(results)
        results.update(calGridInfo(results))
        print(results)
        results.update(predictPorts(results))
        print(results)


if __name__ == '__main__':
    # common.labelPoints(img_base_dir, config_base_dir)
    # common.formatColor(config_base_dir)
    # TestcalType()
    # TestcalPoints()
    testGridAnalyzer()
    # testPredictPorts()
    # overall()
