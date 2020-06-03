import re
import os
import cv2
import numpy as np


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img


if __name__ == '__main__':
    # 获取路径下所有图片
    inputDir = "./input"
    files = os.listdir(inputDir)

    # cutWid = int(input('请输入想要切割的宽度:'))
    cutWid = 100

    for file in files:
        # 获取图片大小
        print(file)
        img = cv_imread("./input/"+file)
        hei = img.shape[0]
        wid = img.shape[1]
        print(img.shape)

        # 获取文件名及文件类型
        filename = file[0:(re.search('\.', file).span()[1]) - 1]
        filetype = file[(re.search('\.', file).span()[1]):len(file)]
        print(filename)
        
        # 求出切割的分数
        cutCount = int(wid/cutWid) + 1

        # 循环切割图片
        i = 0
        while i < cutCount:
            # print(i)

            # 最后一次不一定为整数大小
            if i == cutCount-1:
                cropped = img[0:hei, cutWid * i:wid]
            else:
                cropped = img[0:hei, cutWid * i:cutWid * (i + 1)]
            cv2.imwrite("./output/"+filename+'-'+str(i)+'.'+filetype, cropped)
            i += 1
