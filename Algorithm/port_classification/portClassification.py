import cv2
import numpy as np
import pickle
from collections import Counter
from sklearn.svm import SVC
from sklearn import neighbors
import time
import constant
import Algorithm.utils.common as utils
import os


def find_most(al):  # 找列表的众数
    c = Counter(al)
    dd = c.most_common(len(al))  # 转为列表
    # print("转换后：", dd)  #[(7, 14), (6, 5), (8, 2), (15, 1)]
    # 把出现次数最大的都找到 要下标和个数
    hh = [t for i, t in dd]
    nmax = hh.count(max(hh))  # 最大次数的个数
    ii = c.most_common(nmax)
    for i in ii:
        return i[0]


def createHistFeature(grid, small_grid=3):
    """
    # 生成颜色直方图特征
    :param grid: 数据
    :param small_grid: 细分的网格数
    :return: 数据的特征
    """
    hist_mask = np.array([])
    colnum = int(grid.shape[1] / small_grid)
    rownum = int(grid.shape[0] / small_grid)
    for i in range(small_grid):
        for j in range(small_grid):
            image = grid[i * colnum:(i + 1) * colnum, j * rownum:(j + 1) * rownum, :]
            hist_mask0 = cv2.calcHist([image], [0], None, [16], [0, 255])
            hist_mask1 = cv2.calcHist([image], [1], None, [16], [0, 255])
            hist_mask2 = cv2.calcHist([image], [2], None, [16], [0, 255])
            hist_mask_small = np.concatenate((hist_mask0, hist_mask1, hist_mask2), axis=0)
            if len(hist_mask) == 0:
                hist_mask = hist_mask_small
            else:
                hist_mask = np.concatenate((hist_mask, hist_mask_small), axis=0)
    return hist_mask


class Classification:
    def __init__(self, gallery_path, method="knn", feature="hist"):
        """
        # 加载训练数据以及模型
        :param gallery_path: 训练数据路径
        :param method: 提取特征的方式
        :param feature: 提取特征的方式
        """
        print("gallery path:", gallery_path)
        data = open(gallery_path + "/complete_dbase.txt", 'rb')
        data = pickle.load(data)
        self.feature = feature

        if method == "knn":
            self.traindata_feature = data
            self.nparray = np.array([[]])
            for i, feat in enumerate(data):
                if i == 0:
                    self.nparray = feat[0].T
                else:
                    self.nparray = np.concatenate((self.nparray, feat[0].T), axis=0)
        elif method == "knn2":
            Xarray = np.array([[]])
            Yarray = np.array([])
            for i, feat in enumerate(data):
                Yarray = np.append(Yarray, feat[1])
                if i == 0:
                    Xarray = feat[0].T
                else:
                    Xarray = np.concatenate((Xarray, feat[0].T), axis=0)
            self.clf = neighbors.KNeighborsClassifier(4, algorithm="auto")
            self.clf.fit(Xarray, Yarray)
        elif method == "svm":
            Xarray = np.array([[]])
            Yarray = np.array([[]])
            for i, feat in enumerate(data):
                Yarray = np.append(Yarray, feat[1])
                if i == 0:
                    Xarray = feat[0].T
                else:
                    Xarray = np.concatenate((Xarray, feat[0].T), axis=0)
            self.clf = SVC(gamma='auto', kernel='rbf')
            self.clf.fit(Xarray, Yarray)

    def knn(self, testdata, k=4):
        """
        # 利用KNN进行分类
        :param testdata:   测试图片
        :param k: 近邻
        :return: 分类结果
        """
        if self.feature == "hist":
            test_feature = createHistFeature(testdata)
        similar = np.linalg.norm(self.nparray - np.squeeze(test_feature), axis=1)
        index = np.argsort(similar)
        select = []
        for i in range(k):
            select.append(int(self.traindata_feature[index[i]][1]))
        return find_most(select)  # 投票

    def knn2(self, testdata):
        """
        # 利用sklearn中的KNN进行分类
        :param testdata:   测试图片
        :return: 分类结果
        """
        if self.feature == "hist":
            test_feature = createHistFeature(testdata)
        return self.clf.predict(test_feature.T)

    def svm(self, testdata):
        """
        # 利用SVM进行分类
        :param testdata:   测试图片
        :return: 分类结果
        """
        if self.feature == "hist":
            test_feature = createHistFeature(testdata)
        return self.clf.predict(test_feature.T)


def get_port_classification_result(info):
    """
    计算端口信息
    :param info:
    :return:
    """
    # 解析输入参数info
    addr = info[constant.ADDR]  # 图片路径
    outercolor = info[constant.OUTER_COLOR]  # 机架色
    innercolor = info[constant.INNER_COLOR]  # 卡槽色
    points = info[constant.POINTS]  # 机架边界点
    isrotate = info[constant.IS_ROTATE]  # 横竖排
    row = info[constant.ROW]  # 行数
    col = info[constant.COL]  # 列数
    #img_path = os.path.join(constant.PROJECT_DIR, constant.IMG_DIR, addr)
    img_path=constant.IMG_DIR+"/"+ addr
    #print(img_path)
    img = cv2.imread(img_path)
    print("img shape:", img.shape)
    image_change = utils.transform(img, points)  # 提取有效区域，并做仿生变换
    type = list(constant.TYPE_2_COLOR.keys())[
        list(constant.TYPE_2_COLOR.values()).index([outercolor, innercolor])]  # 根据机架色和卡槽色确定类型

    gallery_path = os.path.join(os.path.join(os.path.join("Algorithm", "port_classification"), "gallery"),
                                "type" + str(type))
    method = "knn"
    k = Classification(gallery_path, method, "hist")
    split_x = image_change.shape[1] / col
    split_y = image_change.shape[0] / row
    result = np.zeros((row, col))

    c = 0
    for i in range(row):
        for j in range(col):
            c += 1
            img = image_change[round(i * split_y): round((i + 1) * split_y),
                  round(j * split_x): round((j + 1) * split_x)]

            # start = time.clock()
            start = time.time()
            if method == "knn":
                result[i, j] = k.knn(img, 4)
            elif method == "svm":
                result[i, j] = k.svm(img)
            elif method == "knn2":
                result[i, j] = k.knn2(img)
            elapsed = (time.time() - start)
    return {"result": result.tolist()}
