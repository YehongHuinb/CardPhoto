# -*- coding: gbk -*-

import cv2
import dlib
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor, QIcon, QPalette, QBrush
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QAction, QProgressBar
from StartWindow import Ui_startView
from MainWindow import Ui_mainView


# * 颜色复杂的照片，不能有效运行
# ! 无法保存中文名称的照片
class MainView(QtWidgets.QMainWindow, Ui_mainView):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./src/icon/picture.ico'))
        palette = QPalette()
        palette.setBrush(QPalette.Background,
                         QBrush(QtGui.QPixmap("./src/BG.jpg")))
        self.setPalette(palette)
        self.menuhelp.triggered[QAction].connect(self.info)
        self.btn_exit.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.savePhoto)
        self.btn_reload.clicked.connect(self.reLoad)
        self.btn_wbg.clicked.connect(self.toWhite)
        self.btn_rbg.clicked.connect(self.toRed)
        self.btn_bbg.clicked.connect(self.toBlue)
        self.btn_oneInch.clicked.connect(self.oneInch)
        self.btn_SoneInch.clicked.connect(self.sOneInch)
        self.btn_LoneInch.clicked.connect(self.lOneInch)
        self.btn_twoInch.clicked.connect(self.twoInch)
        self.btn_StwoInch.clicked.connect(self.sTwoInch)
        self.btn_LtwoInch.clicked.connect(self.lTwoInch)
        self.btn_beauty.stateChanged.connect(self.beautify)

        self.detector = dlib.get_frontal_face_detector()
        self.size_width = [295, 260, 390, 413, 413, 413]
        self.size_height = [413, 378, 567, 579, 531, 626]
        self.preview_change = [44, 49, 49, 45, 33, 55]
        self.batch = False
        self.color_select = -1
        self.size_select = -1
        self.beautify_select = False
        self.image_path = ''
        self.image_paths = []
        self.image = None
        self.rect = None
        self.output_im = None
        self.dilate = None

    def info(self):
        info = '作者：YHH\n完成时间：2020.7.1'
        QMessageBox.information(self, '关于', info, QMessageBox.Close)

    '''
    @description:重新上传照片 
    @param {type} :None
    @return: void
    '''
    def reLoad(self):
        img_name, img_type = QFileDialog.getOpenFileNames(
            self, "打开照片", "", " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
        if img_name:
            if len(img_name) == 1:
                self.batch = False
                self.image_path = img_name[0]
            else:
                self.batch = True
                self.image_paths = img_name[:]
            self.preview()
            self.show()
        else:
            return

    '''
    @description:等比缩小函数，应对照片太大不能处理的情况 
    @param {type} :None
    @return: void
    '''
    def toFit(self):
        # 照片大小标准为大二寸的1.5 倍
        t = self.image.shape
        n = t[0] * t[1] / 258538
        if n > 1.5:
            self.image = cv2.resize(self.image, (t[1] / n, t[0] / n))
            cv2.imwrite('./temp/toFit.jpg', self.image)
            self.image_path = './temp/toFit.jpg'

    '''
    @description:找出一个矩形，尽量小且包含头部和肩膀
    @param {type} :None
    @return: void
    '''
    def getRect(self):
        t_img = self.image.copy()
        faces = self.detector(t_img, 1)
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
                self.rect = (left, top, right, bottom)
        else:
            QMessageBox.critical(self, "错误", "没有找到人脸！", QMessageBox.Close)
            return

    '''
    @description: 获取轮廓，并提前将背景改成蓝色
    @param {type} :None
    @return: void
    '''
    def getOutline(self):
        if self.rect is None:
            return
        t_img = self.image.copy()
        t = t_img.shape
        mask = np.zeros(t_img.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        cv2.grabCut(t_img, mask, self.rect, bgd_model, fgd_model, 5,
                    cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        t_img = t_img * mask2[:, :, np.newaxis]
        kernels = np.ones((5, 5), np.uint8)
        erode = cv2.erode(t_img, kernels, iterations=1)
        dilate = cv2.dilate(erode, kernels, iterations=1)
        for i in range(t[0]):
            for j in range(t[1]):
                if max(dilate[i, j]) <= 0:
                    dilate[i, j] = (225, 166, 23)
        dilate = dilate[self.rect[1]:self.rect[3], self.rect[0]:self.rect[2]]
        self.output_im = cv2.resize(dilate,
                                    (self.lab_preview.width(),
                                     self.lab_preview.height()))
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', self.output_im)

    '''
    @description: 获取换底色所用的腐蚀扩张矩阵
    @param {type} :None
    @return: void
    '''
    def getDilate(self):
        if self.output_im is None:
            return
        t_img = self.output_im.copy()
        hsv = cv2.cvtColor(t_img, cv2.COLOR_BGR2HSV)

        # 背景蓝的HSV 值为[99, 229, 225]
        lower_blue = np.array([90, 220, 215])
        upper_blue = np.array([110, 240, 235])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        kernels = np.ones((5, 5), np.uint8)
        erode = cv2.erode(mask, kernels, iterations=1)
        self.dilate = cv2.dilate(erode, kernels, iterations=1)

    '''
    @description:将背景改成红色 
    @param {type} :None
    @return: void
    '''
    def toRed(self):
        self.color_select = 0
        if self.output_im is None:
            return
        t_img = self.output_im.copy()
        rows, cols, channels = t_img.shape
        for i in range(rows):
            for j in range(cols):
                if self.dilate[i, j] == 255:
                    t_img[i, j] = (0, 0, 255)
        self.image = t_img.copy()
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', t_img)
            self.lab_preview.setPixmap(
                QtGui.QPixmap('./temp/toShow.jpg').scaled(
                    self.lab_preview.width(), self.lab_preview.height()))

    '''
    @description:将背景改成蓝色 
    @param {type} :None
    @return: void
    '''
    def toBlue(self):
        self.color_select = 1
        if self.output_im is None:
            return
        t_img = self.output_im.copy()
        rows, cols, channels = t_img.shape
        for i in range(rows):
            for j in range(cols):
                if self.dilate[i, j] == 255:
                    t_img[i, j] = (225, 166, 23)
        self.image = t_img.copy()
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', t_img)
            self.lab_preview.setPixmap(
                QtGui.QPixmap('./temp/toShow.jpg').scaled(
                    self.lab_preview.width(), self.lab_preview.height()))

    '''
    @description:将背景改成白色 
    @param {type} :None
    @return: void
    '''
    def toWhite(self):
        self.color_select = 2
        if self.output_im is None:
            return
        t_img = self.output_im.copy()
        rows, cols, channels = t_img.shape
        for i in range(rows):
            for j in range(cols):
                if self.dilate[i, j] == 255:
                    t_img[i, j] = (255, 255, 255)
        self.image = t_img.copy()
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', t_img)
            self.lab_preview.setPixmap(
                QtGui.QPixmap('./temp/toShow.jpg').scaled(
                    self.lab_preview.width(), self.lab_preview.height()))

    '''
    @description:将尺寸改成1寸 
    @param {type} :None
    @return: void
    '''
    def oneInch(self):
        self.size_select = 0
        if not self.batch:
            self.cutPreview()

    '''
    @description:将尺寸改成小1寸 
    @param {type} :None
    @return: void
    '''
    def sOneInch(self):
        self.size_select = 1
        if not self.batch:
            self.cutPreview()

    '''
    @description:将尺寸改成大1寸 
    @param {type} :None
    @return: void
    '''
    def lOneInch(self):
        self.size_select = 2
        if not self.batch:
            self.cutPreview()

    '''
    @description:将尺寸改成2寸 
    @param {type} :None
    @return: void
    '''
    def twoInch(self):
        self.size_select = 3
        if not self.batch:
            self.cutPreview()

    '''
    @description:将尺寸改成小2寸 
    @param {type} :None
    @return: void
    '''
    def sTwoInch(self):
        self.size_select = 4
        if not self.batch:
            self.cutPreview()

    '''
    @description:将尺寸改成大2寸 
    @param {type} :None
    @return: void
    '''
    def lTwoInch(self):
        self.size_select = 5
        if not self.batch:
            self.cutPreview()

    '''
    @description:美化函数，对照片进行轻度美白
    @param {type} :None
    @return: void
    '''
    def beautify(self):
        if self.btn_beauty.isChecked():
            self.beautify_select = True
            white = 1.02
        else:
            self.beautify_select = False
            white = 0.98
        if self.output_im is None:
            return
        self.output_im = np.power(self.output_im, white)
        if self.color_select == 0:
            self.toRed()
        elif self.color_select == 1 or self.color_select == -1:
            self.toBlue()
        elif self.color_select == 2:
            self.toWhite()

    '''
    @description:预览框变化函数，对应用户选择的尺寸
    @param {type} :None
    @return: void
    '''
    def cutPreview(self):
        if self.output_im is None:
            return
        add_x = self.preview_change[self.size_select]
        self.wid_hole.setGeometry(
            QtCore.QRect(540 + add_x, 50, 361 - 2 * add_x, 381))
        self.lab_preview.move(-add_x, 0)
        width = self.size_width[self.size_select]
        height = self.size_height[self.size_select]
        size = str(width) + ' × ' + str(height)
        self.lab_sizeShow.setText(size)

    '''
    @description:保存照片函数
    @param {type} :None
    @return: void
    '''
    def savePhoto(self):
        if self.size_select == -1 or self.color_select == -1:
            QMessageBox.warning(self, "警告", "请选择尺寸和颜色！", QMessageBox.Close)
            return
        file_path, file_p = QFileDialog.getSaveFileName(
            self, "保存照片", "./save/save.jpg",
            "*.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
        if file_path == '':
            return
        add_x = self.preview_change[self.size_select]
        width = self.size_width[self.size_select]
        height = self.size_height[self.size_select]
        if not self.batch:
            t_img = self.image.copy()
            t = t_img.shape
            t_img = t_img[:, add_x:t[1] - add_x]
            t_img = cv2.resize(t_img, (width, height))
            cv2.imwrite(file_path, t_img, None)
        else:
            file_path = file_path[:len(file_path)-4]
            file_p = file_p[1:]
            bar = QProgressBar(self)
            bar.setGeometry(390, 530, 281, 31)
            step = 100 / len(self.image_paths)
            bar.show()
            bar.setValue(0)
            i = 1
            for path in self.image_paths:
                self.image = cv2.imread(path)
                self.toFit()
                self.getRect()
                self.getOutline()
                self.getDilate()

                if self.beautify_select:
                    self.beautify()

                if self.color_select == 0:
                    self.toRed()
                elif self.color_select == 1:
                    self.toBlue()
                else:
                    self.toWhite()

                t_img = self.image.copy()
                t = t_img.shape
                t_img = t_img[:, add_x:t[1] - add_x]
                t_img = cv2.resize(t_img, (width, height))
                f_path = file_path + str(i) + file_p
                cv2.imwrite(f_path, t_img, None)
                bar.setValue(step * i)
                i = i + 1
            bar.close()
        QMessageBox.information(self, "信息", "保存成功！", QMessageBox.Close)

    '''
    @description:照片预览函数
    @param {type} :None
    @return: void
    '''
    def preview(self):
        if not self.batch:
            self.image = cv2.imread(self.image_path)
            self.toFit()
            self.getRect()
            self.getOutline()
            self.getDilate()
            if self.output_im is not None:
                self.lab_preview.setPixmap(
                    QtGui.QPixmap('./temp/toShow.jpg').scaled(
                        self.lab_preview.width(), self.lab_preview.height()))
        else:
            self.lab_sizeShow.hide()
            self.wid_hole.setGeometry(QtCore.QRect(540, 50, 361, 381))
            self.lab_preview.move(0, 0)
            self.lab_preview.setPixmap(
                QtGui.QPixmap('./src/noShow.jpg').scaled(
                    self.lab_preview.width(), self.lab_preview.height()))


class QtColor(object):
    pass


class StartView(QtWidgets.QMainWindow, Ui_startView):
    def __init__(self):
        super(StartView, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./src/icon/picture.ico'))
        palette = QPalette()
        palette.setColor(self.backgroundRole(), QColor(0, 167, 241))
        self.setPalette(palette)
        self.m_view = MainView()
        self.menuhelp.triggered[QAction].connect(self.info)
        self.btn_exit.clicked.connect(self.close)
        self.btn_open.clicked.connect(self.openImage)

    def info(self):
        info = '作者：YHH\n完成时间：2020.7.1'
        QMessageBox.information(self, '关于', info, QMessageBox.Close)

    '''
    @description:照片打开函数
    @param {type} :None
    @return: void
    '''
    def openImage(self):
        img_name, img_type = QFileDialog.getOpenFileNames(
            self, "打开照片", "", " *.jpg;;*.png;;*.jpeg;;*.bmp;;All Files (*)")
        if img_name:
            self.close()
            if len(img_name) == 1:
                self.m_view.batch = False
                self.m_view.image_path = img_name[0]
            else:
                self.m_view.batch = True
                self.m_view.image_paths = img_name[:]
            self.m_view.preview()
            self.m_view.show()
        else:
            return
