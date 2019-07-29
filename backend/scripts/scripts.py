# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np

#全局阈值
def threshold_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    #直接阈值化是对输入的单通道矩阵逐像素进行阈值分割。
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
    print("threshold value %s"%ret)
    cv.namedWindow("binary0", cv.WINDOW_NORMAL)
    show("binary0", binary)


#局部阈值
def local_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    #自适应阈值化能够根据图像不同区域亮度分布，改变阈值
    binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)
    cv.namedWindow("binary1", cv.WINDOW_NORMAL)
    show("binary1", binary)


#用户自己计算阈值
def custom_threshold(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)  #把输入图像灰度化
    h, w =gray.shape[:2]
    m = np.reshape(gray, [1,w*h])
    mean = m.sum()/(w*h)
    print("mean:",mean)
    ret, binary =  cv.threshold(gray, mean, 255, cv.THRESH_BINARY)
    cv.namedWindow("binary2", cv.WINDOW_NORMAL)
    show("binary2", binary)


def show(string, binary):
    """
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    #开操作
    ret1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel, iterations=5)
    #闭操作
    ret2 = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel, iterations=5)
    """
    cv.imshow(string, binary)


def contours(image):
    img = cv.imread(image)
    size = img.shape
    print (size)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)#cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    l = size[1]
    u = size[0]
    r = b = 0
    print (len(contours))
    for contour in contours:
        leftmost = tuple(contour[:,0][contour[:,:,0].argmin()])
        if leftmost[0] != 0 and leftmost[0] < l:
            l = leftmost[0]

        rightmost = tuple(contour[:,0][contour[:,:,0].argmax()])
        if rightmost[0] != size[1]-1 and rightmost[0] > r:
            r = rightmost[0]

        upmost = tuple(contour[:,0][contour[:,:,1].argmin()])
        if upmost[1] != 0 and upmost[1] < u:
            u = upmost[1]

        bottommost = tuple(contour[:,0][contour[:,:,1].argmax()])
        if bottommost[1] != size[0]-1 and bottommost[1] > b:
            b = bottommost[1]
    print (l, r, u, b)
    cv.circle(img, (l, u), 2, (0, 0, 255), 3)
    cv.circle(img, (r, b), 2, (0, 0, 255), 3)

    cv.drawContours(img, contours, -1, (0, 0, 255), 3)
    cv.namedWindow("contours", cv.WINDOW_NORMAL)
    cv.imshow("contours", img)


def grabcut(image):
    img = cv.imread(image)
    size = img.shape
    print (size)
    src = img
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    binary =  cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 25, 10)#cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    l = size[1]
    u = size[0]
    r = b = 0
    for contour in contours:
        leftmost = tuple(contour[:,0][contour[:,:,0].argmin()])
        if leftmost[0] != 0 and leftmost[0] < l:
            l = leftmost[0]

        rightmost = tuple(contour[:,0][contour[:,:,0].argmax()])
        if rightmost[0] != size[1]-1 and rightmost[0] > r:
            r = rightmost[0]

        upmost = tuple(contour[:,0][contour[:,:,1].argmin()])
        if upmost[1] != 0 and upmost[1] < u:
            u = upmost[1]

        bottommost = tuple(contour[:,0][contour[:,:,1].argmax()])
        if bottommost[1] != size[0]-1 and bottommost[1] > b:
            b = bottommost[1]
    print ("left:%d right:%d up:%d bottom:%d" % (l, r, u, b))

    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (l, u, r, b)
    cv.grabCut(img, mask, rect, bgdModel, fgdModel, 10, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    img += 255 * (1 - cv.cvtColor(mask2, cv.COLOR_GRAY2BGR))
    cv.namedWindow("grabcut", cv.WINDOW_NORMAL)
    cv.imshow("grabcut", img)

    mask = np.ones(size[0:2], dtype = np.uint8)
    mask *= 255
    for row in range(size[0]):
        for col in range(size[1]):
            """RGB 3 channel img"""
            (r, g, b) = img[row][col]
            if r == 255 and g == 255 and b == 255:
                continue
            mask[row][col] = 0
    cv.namedWindow("mask", cv.WINDOW_NORMAL)
    cv.imshow("mask", mask)

    result = cv.add(src, np.zeros(np.shape(src), dtype=np.uint8), mask=mask)
    cv.namedWindow("result", cv.WINDOW_NORMAL)
    cv.imshow("result", result)

    return result


if __name__ == "__main__":
    image = "./img/8.jpg"
    src = cv.imread(image)
    cv.namedWindow('input_image', cv.WINDOW_NORMAL) #设置为WINDOW_NORMAL可以任意缩放
    show('input_image', src)
    #threshold_demo(src)
    #local_threshold(src)
    #custom_threshold(src)
    #contours(image)
    grabcut(image)
    cv.waitKey(0)
    cv.destroyAllWindows()
