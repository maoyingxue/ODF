# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 11:28:01 2019
"""

import numpy as np
import cv2
from utils import calProjection
def getpoint(image,color,vis=False,ratio=[0.1,0.1]):
    Img=image
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)
    #color
    lower = np.array([color[0][0], color[1][0], color[2][0]], dtype="uint8")
    upper = np.array([color[0][1], color[1][1], color[2][1]], dtype="uint8")
    Mask = cv2.inRange(HSV, lower, upper)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    Mask = cv2.erode(Mask, kernel)
    Mask = cv2.dilate(Mask, kernel)

    if vis==True:
        Things = cv2.bitwise_and(Img, Img, mask=Mask)
        cv2.imshow("images2", np.hstack([Img, Things]))
    _, Contours, Hierarchy = cv2.findContours(Mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Contours = sorted(Contours, key=lambda c: c.shape[0], reverse=True)
    distance1=0
    distance2=0
    distance3=0
    distance4=0
    x=image.shape[1]//2
    y=image.shape[0]//2
    
    for c in Contours:
        for p in c:
            #print(p)
            dis=(p[0][0]-x)**2+(p[0][1]-y)**2
            if dis>distance1 and p[0][0]<x and p[0][1]<y:
                distance1=dis
                P1=p
            if dis>distance2 and p[0][0]>x and p[0][1]<y:
                distance2=dis
                P2=p
            if dis>distance3 and p[0][0]<x and p[0][1]>y:
                distance3=dis
                P3=p
            if dis>distance4 and p[0][0]>x and p[0][1]>y:
                distance4=dis
                P4=p
    #计算上下是否空盘
    result=calProjection(Mask)
    print(result)
    # caculate width
    w1=((P1[0][0]-P2[0][0])**2+(P1[0][1]-P2[0][1])**2)**0.5
    w2=((P3[0][0]-P4[0][0])**2+(P3[0][1]-P4[0][1])**2)**0.5
    #去除左右边框
    if result[0]==False:
        P1[0][0]=P1[0][0]+w1*ratio[0]
        P2[0][0]=P2[0][0]-w1*ratio[1]
    if result[1]==False:
        P3[0][0]=P3[0][0]+w2*ratio[0]
        P4[0][0]=P4[0][0]-w2*ratio[1]
    if vis==True:
        cv2.circle(image,tuple(P1[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P2[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P3[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P4[0]),5,(0,0,155),-1)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return [P1[0],P2[0],P4[0],P3[0]]
if __name__=='__main__':
    image = cv2.imread('E:/maoyingxue/ODF-Port-Identification/stores/images/4_2.jpg')
    image=image[0:3300]
    image=cv2.resize(image,(0,0),fx=0.1,fy=0.1)
    getpoint(image,[[35,99],[80,255],[46,255]])
