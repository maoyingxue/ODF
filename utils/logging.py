#!/usr/bin/env python
# encoding: utf-8
"""
@author: Shanda Lau 刘祥德
@license: (C) Copyright 2019-now, Node Supply Chain Manager Corporation Limited.
@contact: shandalaulv@gmail.com
@software: garner
@file: Logger.py
@time: 2019-07-19 18:05
@version 1.0
@desc:
"""
import logging
import os
from constant import PROJECT_DIR

# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 创建一个handler，用于写入日志文件
logfile = os.path.join(PROJECT_DIR, 'log.txt')
# logfile = './log/logger.txt'
# 追加模式
fh = logging.FileHandler(logfile, mode='a+')
# 控制输出的日志级别
# 日志级别为 NOTSET = 0,DEBUG = 10, INFO = 20 , WARNING = 30 ,ERROR = 40
# >=所设置级别的日志才会被输出
# ERROR 是最高级别
fh.setLevel(logging.NOTSET)  # 输出到file的log等级的开关

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关

# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

# # 日志
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')
