#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import time
import numpy as np
import os
import random
from matplotlib import pyplot as plt
class Image():

    def marks(self,src_path):
        
        #常用的图像读取函数
        img_bgr = cv2.imread(src_path)
        #返回来一个给定形状和类型的用0填充的数组
        img_rgb = np.zeros(img_bgr.shape, img_bgr.dtype)
        img_rgb[:,:,0] = img_bgr[:,:,2]
        img_rgb[:,:,1] = img_bgr[:,:,1]
        img_rgb[:,:,2] = img_bgr[:,:,0]
        brightness_array = []
        for hight in range(0, img_rgb.shape[0]):
            for width in range(0, img_rgb.shape[1]):
                brightness = img_rgb[hight, width, 0] * 0.3 + img_rgb[hight, width, 1] * 0.59 + img_rgb[hight, width, 2] * 0.11
                brightness_array.append(brightness)

        #高斯滤波实现对图像噪声的消除，增强图像的效果
        img_rgb = cv2.GaussianBlur(img_rgb, ksize=(3,3),sigmaX=0)
        #颜色空间转换
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2GRAY)
        #Laplacian 算子 的离散模拟，可以计算出图像的拉普拉斯算子
		#图像中的边缘区域，像素值会发生“跳跃”，对这些像素求导，在其一阶导数在边缘 
        #位置为极值，这就是Sobel算子使用的原理——极值处就是边缘。如果对像素值求二阶导数， 
        #会发现边缘处的导数值为0 
        #Laplace函数实现的方法是先用Sobel 算子计算二阶x和y导数，再求和：
        img_laplacian = cv2.Laplacian(img_gray,cv2.CV_64F)
        #计算矩阵的均值和标准偏差
        (mean,stddev) = cv2.meanStdDev(img_laplacian)
        
        sharpness=stddev[0][0]
        sharpness=sharpness*3
        if sharpness>=100:
            sharpness=random.randint(90, 95)
        else :
            sharpness=int(sharpness)
        
        exposure=Image().exposure(brightness_array)
        data=src_path.split('/')[6]+'\r\n'+'exposure:'+str(exposure)+'\r\n'+'sharpness:'+str(sharpness)

        #分割出图片的时间
        timer=src_path.split('/')[6].split('.')[0]
        filepath='/home/nvidia/Horus/img/'+str(timer)+'.txt'
        with open(filepath, 'w') as f:
            f.write(data)

    def exposure(self,brightness_array):
        left=0  #亮度小于85的像素
        middle=0  #亮度在85和170之间的像素
        right=0  #亮度大于等于170的像素
        for j in brightness_array:
            if 0<j<85:
                left+=1
            elif 85<=j<=170:
                middle+=1
            else :
                right+=1
        exposure=0
        if left-middle>2*middle or right-middle>2*middle:
            exposure=random.randint(10,50)
        else :
            exposure=random.randint(70,98)
        return exposure


