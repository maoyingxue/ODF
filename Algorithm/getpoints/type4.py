# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 15:21:32 2019

@author: maoyingxue
"""

import numpy as np
import cv2
from Algorithm.getpoints.utils import calProjection
def getpoint(image,vis=True):
    #print(image.shape)
    h,w,_=image.shape
    r1,r2=400/w,w/400
    image=cv2.resize(image,(0,0),fx=r1,fy=r1)
    #image = cv2.imread('odf_test/type4_2.jpg')
    #image=cv2.resize(image,(500,700))
    Img=image
    HSV = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(HSV)
    #green
    lower = np.array([35, 80, 46], dtype="uint8")
    upper = np.array([99, 255, 255], dtype="uint8")
    Mask = cv2.inRange(HSV, lower, upper)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    Mask = cv2.erode(Mask, kernel)
    Mask = cv2.dilate(Mask, kernel)

    if vis==True:
        BlueThings = cv2.bitwise_and(Img, Img, mask=Mask)    
        cv2.imshow("images2", np.hstack([Img, BlueThings]))
    #cv2.imwrite("type/type1_1.jpg",np.hstack([Img, BlueThings]))
    Contours, Hierarchy = cv2.findContours(Mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #Contours = sorted(Contours, key=lambda c: c.shape[0], reverse=True)
    #Contours = [c for c in Contours if len(c) > 5 ]
    #cv2.drawContours(image,Contours,-1,(0,255,0),3)
    distance1=0
    distance2=0
    distance3=0
    distance4=0
    x=image.shape[1]//2
    y=image.shape[0]//2
    P1 = np.array([[-1, -1]]);P2 = np.array([[-1, -1]]);P3 = np.array([[-1, -1]]);P4 = np.array([[-1, -1]])
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
    result=calProjection(Mask,ratio=0.5)
    print(result)
    w1=((P1[0][0]-P2[0][0])**2+(P1[0][1]-P2[0][1])**2)**0.5
    #h1=((P1[0][0]-P3[0][0])**2+(P1[0][1]-P2[0][1])**2)**0.5
    w2=((P3[0][0]-P4[0][0])**2+(P3[0][1]-P4[0][1])**2)**0.5
    #h2=((P2[0][0]-P4[0][0])**2+(P2[0][1]-P4[0][1])**2)**0.5
    #print(w1)
    P1[0][0],P1[0][1]=P1[0][0]+w1*0.1,P1[0][1]
    P2[0][0],P2[0][1]=P2[0][0]-w1*0.1,P2[0][1]
    P3[0][0],P3[0][1]=P3[0][0]+w2*0.1,P3[0][1]
    P4[0][0],P4[0][1]=P4[0][0]-w2*0.1,P4[0][1]
    if vis==True:        
        cv2.circle(image,tuple(P1[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P2[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P3[0]),5,(0,0,155),-1)
        cv2.circle(image,tuple(P4[0]),5,(0,0,155),-1)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    P1[0]=(P1[0]*r2).astype(int)
    P2[0]=(P2[0]*r2).astype(int)
    P3[0]=(P3[0]*r2).astype(int)
    P4[0]=(P4[0]*r2).astype(int)
    #print([P1[0],P2[0],P4[0],P3[0]])
    return [P1[0].tolist(),P2[0].tolist(),P4[0].tolist(),P3[0].tolist()]
if __name__=='__main__':
    image = cv2.imread('E:/maoyingxue/ODF-Port-Identification/stores/images/4_1.jpg')
    #image=cv2.resize(image,(0,0),fx=0.1,fy=0.1)
    getpoint(image)
