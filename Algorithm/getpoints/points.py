# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:47:45 2019

"""

from Algorithm.getpoints import type1,type2,type3,type4,type5,type6
import os
import cv2
def calpoints(info):
    img = cv2.imread(info["addr"])
    path = os.path.split(info["addr"])
    cls=path[-1].split("_")[0]
    print("type:",cls)
    if info["outerColor"]=="cyan" and info["innerColor"]=="red":
        result=type1.getpoint(img,False)
        return result
    elif info["outerColor"]=="black" and info["innerColor"]=="red":
        #result=type2.getpoint(img,False)
        #result = type2.getpoint(img, path[-1][:-4])
        return "unsupported"
    elif info["outerColor"]=="green" and info["innerColor"]=="blue":
        result=type3.getpoint(img,False)
        return result
    elif info["outerColor"]=="green" and info["innerColor"]=="red":
        result=type4.getpoint(img,False)
        return result
    elif info["outerColor"]=="gray" and info["innerColor"]=="blue":
        result=type5.getpoint(img,False)
        return result
    elif info["outerColor"]=="blue" and info["innerColor"]=="red":
        result=type6.getpoint(img,False)
        return result
    else:
        return "unsupported"

    
