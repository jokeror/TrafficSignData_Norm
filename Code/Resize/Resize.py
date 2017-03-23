# -*- coding:gb2312 -*-
import os
import cv2

"""
功能：将load_path下文件转换为指定大小保存于save_path下
使用：load_path  载入路径
      save_path  保存路径
      img_width  图像宽度
      img_height 图像高度
"""
load_path = 'H:\\TrafficSignData\\TrafficSignData\\15 注意行人\\'
save_path = 'H:\\TrafficSignData\\Norm_DATA\\15 注意行人\\'
img_width = 640
img_height = 960


file_list = os.listdir(load_path)
for name in file_list:
    print name
    img = cv2.imread(load_path + name, cv2.IMREAD_COLOR)
    # print img.shape
    if (img.shape[0]) > (img.shape[1]):
        resized = cv2.resize(img,(img_width,img_height),cv2.INTER_CUBIC)
    elif (img.shape[0]) < (img.shape[1]):
        resized = cv2.resize(img,(img_height,img_width),cv2.INTER_CUBIC)

    cv2.imwrite(save_path + name, resized)
