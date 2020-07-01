'''
@Author: your name
@Date: 2020-06-30 19:13:48
@LastEditTime: 2020-06-30 22:33:09
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \CardPhoto\MyButton.py
'''
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class MyButton(QPushButton):
    def __init__(self, parent, normalImg, pressImg):
        super(MyButton, self).__init__(parent)
        self.normalImg = normalImg
        self.pressImg = pressImg
        self.x = int(abs(self.normalImg.width() - self.pressImg.width()) / 2)
        self.y = int(abs(self.normalImg.height() - self.pressImg.height()) / 2)
        self.setIcon(QIcon(self.normalImg))
        self.setFixedSize(QSize(self.normalImg.width(), self.normalImg.height()))
        self.setIconSize(QSize(self.normalImg.width(), self.normalImg.height()))

    def mousePressEvent(self, event):
        self.move(self.pos().x() + self.x, self.pos().y() + self.y)
        self.setIcon(QIcon(self.pressImg))
        self.setFixedSize(QSize(self.pressImg.width(), self.pressImg.height()))
        self.setIconSize(QSize(self.pressImg.width(), self.pressImg.height()))
        return QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.move(self.pos().x() - self.x, self.pos().y() - self.y)
        self.setIcon(QIcon(self.normalImg))
        self.setFixedSize(QSize(self.normalImg.width(), self.normalImg.height()))
        self.setIconSize(QSize(self.normalImg.width(), self.normalImg.height()))
        return QPushButton.mouseReleaseEvent(self, event)
