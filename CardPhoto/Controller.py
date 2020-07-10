import cv2
import dlib
import numpy as np


def getRect(image):
    rect = None
    detector = dlib.get_frontal_face_detector()
    t_img = image.copy()
    faces = detector(t_img, 1)
    t = t_img.shape
    if len(faces) > 0:
        for k, d in enumerate(faces):
            # 假设肩膀的宽度与头部的宽度的比例大致为 3:1
            left = max(int((3 * d.left() - d.right()) / 2), 1)
            top = max(int((3 * d.top() - d.bottom()) / 2) - 50, 1)
            right = min(int((3 * d.right() - d.left()) / 2), t[1])
            bottom = min(int((3 * d.bottom() - d.top()) / 2), t[0])

            # 使矩形的比例与预览框的大致相同
            # 381 / 361 约为1.06
            # 361 / 381 约为0.98
            if bottom / right <= 0.9:
                x = int((right - bottom / 1.06) / 2)
                left = left + x
                right = right - x
            elif bottom / right >= 1.1:
                y = int((bottom - right / 0.98) / 2)
                top = top + y
                bottom = bottom - y
            rect = (left, top, right, bottom)
    return rect


def getOutline(image, rect):
    t = image.shape
    mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5,
                cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    image = image * mask2[:, :, np.newaxis]
    kernels = np.ones((5, 5), np.uint8)
    erode = cv2.erode(image, kernels, iterations=1)
    dilate = cv2.dilate(erode, kernels, iterations=1)
    for i in range(t[0]):
        for j in range(t[1]):
            if max(dilate[i, j]) <= 0:
                dilate[i, j] = (225, 166, 23)
    dilate = dilate[rect[1]:rect[3], rect[0]:rect[2]]
    return dilate


def getDilate(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 背景蓝的HSV 值为[99, 229, 225]
    lower_blue = np.array([90, 220, 215])
    upper_blue = np.array([110, 240, 235])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernels = np.ones((5, 5), np.uint8)
    erode = cv2.erode(mask, kernels, iterations=1)
    dilate = cv2.dilate(erode, kernels, iterations=1)
    return dilate


def changeColor(image, dilate, color_select):
    color = None
    if color_select == 0:
        color = (0, 0, 255)
    elif color_select == 1:
        color = (225, 166, 23)
    elif color_select == 2:
        color = (255, 255, 255)
    rows, cols, channels = image.shape
    for i in range(rows):
        for j in range(cols):
            if dilate[i, j] == 255:
                image[i, j] = color
    return image


def changeSize(image, size_select):
    size_width = [295, 260, 390, 413, 413, 413]
    size_height = [413, 378, 567, 579, 531, 626]
    preview_change = [44, 49, 49, 45, 33, 55]

    add_x = preview_change[size_select]
    width = size_width[size_select]
    height = size_height[size_select]
    t = image.shape
    image = image[:, add_x:t[1] - add_x]
    image = cv2.resize(image, (width, height))
    return image
