# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 17:05:50 2019
"""

import numpy as np
import cv2
def getpoint(image,color,vis=False):
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
    #vis=False
    if vis==True:
        BlueThings = cv2.bitwise_and(Img, Img, mask=Mask)
        cv2.imshow("images2", np.hstack([Img, BlueThings]))
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
    if vis==True:
        cv2.circle(image,tuple(P1[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P2[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P3[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P4[0]),5,(0,0,155),-1)

        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return [P1[0],P2[0],P4[0],P3[0]]