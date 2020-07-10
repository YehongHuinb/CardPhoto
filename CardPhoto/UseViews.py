# -*- coding: gbk -*-

import cv2
import dlib
import numpy as np
import Controller
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
        info = '作者：YHH\n完成时间：2020.7.10'
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
        if self.image is None:
            return
        self.rect = Controller.getRect(self.image)
        if self.rect is None:
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
        self.output_im = Controller.getOutline(self.image, self.rect)
        self.output_im = cv2.resize(self.output_im,
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
        self.dilate = Controller.getDilate(self.output_im)

    '''
    @description:将背景改成红色 
    @param {type} :None
    @return: void
    '''
    def toRed(self):
        self.color_select = 0
        if self.output_im is None:
            return
        self.image = \
            Controller.changeColor(self.output_im, self.dilate, self.color_select)
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', self.image)
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
        self.image = \
            Controller.changeColor(self.output_im, self.dilate, self.color_select)
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', self.image)
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
        self.image = \
            Controller.changeColor(self.output_im, self.dilate, self.color_select)
        if not self.batch:
            cv2.imwrite('./temp/toShow.jpg', self.image)
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
    @description:改颜色函数，适应批量处理功能
    @param {type} :None
    @return: void
    '''
    def changeColor(self):
        if self.output_im is None:
            return
        if self.color_select == 0:
            self.toRed()
        elif self.color_select == 1 or self.color_select == -1:
            self.toBlue()
        elif self.color_select == 2:
            self.toWhite()

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
        self.changeColor()

    '''
    @description:预览框变化函数，对应用户选择的尺寸
    @param {type} :None
    @return: void
    '''
    def cutPreview(self):
        if self.output_im is None:
            return
        if self.size_select != -1:
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
        if not self.batch:
            t_img = Controller.changeSize(self.image, self.size_select)
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

                t_img = Controller.changeSize(self.image, self.size_select)
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
        self.beautify_select = False
        self.btn_beauty.setChecked(False)
        if not self.batch:
            self.lab_sizeShow.show()
            self.image = cv2.imread(self.image_path)
            self.toFit()
            self.getRect()
            self.getOutline()
            self.getDilate()
            self.changeColor()
            if self.output_im is not None:
                self.lab_preview.setPixmap(
                    QtGui.QPixmap('./temp/toShow.jpg').scaled(
                        self.lab_preview.width(), self.lab_preview.height()))
            self.cutPreview()
        else:
            self.lab_sizeShow.hide()
            self.wid_hole.setGeometry(QtCore.QRect(540, 50, 361, 381))
            self.lab_preview.move(0, 0)
            self.lab_preview.setPixmap(
                QtGui.QPixmap('./src/noShow.jpg').scaled(
                    self.lab_preview.width(), self.lab_preview.height()))


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
        info = '作者：YHH\n完成时间：2020.7.10'
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
