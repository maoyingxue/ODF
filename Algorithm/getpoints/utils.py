# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:13:53 2019

@author: maoyingxue
"""
import numpy as np
#计算上下边界处是否空盘
def calProjection(mask,n=20,ratio=0.2):
    h,w=mask.shape
    print(h,w)
    interval=h//n
    start=(h-interval*n)//2
    print(interval,start)
    a = [0 for z in range(0, h)]  
    for j in range(0,h):  
        for i in range(0,w):  
            if  mask[j,i]==255: 
                a[j]+=1 
    #print(a) 
    mean1=np.mean(a)
    meanup=np.mean(a[start:(start+interval)])
    meandown=np.mean(a[h-start-interval:h-start])
    print(mean1,meanup,meandown)
    result=[False,False]
    if meanup<(ratio*mean1):
        result[0]=True
    if meandown<(ratio*mean1):
        result[1]=True
    return result

    