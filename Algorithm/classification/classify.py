# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:05:33 2019

@author: maoyingxue
"""

import numpy as np
import cv2
import pickle
import os
import operator
class Classify():
    def __init__(self):
        self.getTrainFeature("Algorithm/classification/trainData.txt")
    def getTrainFeature(self,path,reload=False):
        if os.path.exists(path) and reload==False:
            self.trainData=pickle.load(open(path,"rb"))
            self.trainFeature=self.trainData['trainFeature']
            self.trainLabels=self.trainData['trainLabels']
        else:
            self.trainFeature=[]
            self.trainLabels=[]
            imgpath="images"
            files=os.listdir(imgpath)
            for file in files:
                tmp=file.split("_")
                img=cv2.imread(os.path.join(imgpath,file))
                print(file,img.shape)
                img=cv2.resize(img,(500,700))
                hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                hist1 = cv2.calcHist([hsv], [0], None, [9], [0, 180])
                hist2 = cv2.calcHist([hsv], [1], None, [16], [0, 256])
                hist = np.append(hist1, hist2)
                self.trainFeature.append(hist)
                self.trainLabels.append(tmp[0]+"_"+tmp[1])
                #print(hist,tmp[0]+"_"+tmp[1])
            self.trainFeature=np.array(self.trainFeature)
            pickle.dump({'trainFeature':self.trainFeature,'trainLabels':self.trainLabels},open(path,"wb"))
    def predict(self,img):
        img=cv2.resize(img,(500,700))
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        hist1 = cv2.calcHist([hsv], [0], None, [9], [0, 180])
        hist2 = cv2.calcHist([hsv], [1], None, [16], [0, 256])
        hist = np.append(hist1, hist2)
        return self.knn(hist)
    def knn(self,testfeature,k=1):
        dataSetSize = self.trainFeature.shape[0]
        diffMat = np.tile(testfeature, (dataSetSize,1)) - self.trainFeature
        sqDiffMat = diffMat**2
        sqDistances = sqDiffMat.sum(axis=1)
        distances = sqDistances**0.5
        sortedDistIndicies = distances.argsort()     
        classCount={}          
        for i in range(k):
            voteIlabel = self.trainLabels[sortedDistIndicies[i]]
            classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]
if __name__=='__main__':
    cls=Classify()
    print(cls.trainFeature.shape)
    img=cv2.imread("images/5_2_1.jpg")
    result=cls.predict(img)
    print(result)