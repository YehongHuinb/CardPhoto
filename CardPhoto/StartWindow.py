# -*- coding: gbk -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_startView(object):
    def setupUi(self, startView):
        startView.setObjectName("startView")
        startView.resize(939, 571)
        startView.setMinimumSize(QtCore.QSize(939, 571))
        startView.setMaximumSize(QtCore.QSize(939, 571))
        self.centralwidget = QtWidgets.QWidget(startView)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(520, 180, 131, 131))
        self.btn_exit.setObjectName("btn_exit")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(270, 180, 131, 131))
        self.btn_open.setObjectName("btn_open")
        startView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(startView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 939, 30))
        self.menubar.setObjectName("menubar")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        startView.setMenuBar(self.menubar)
        self.actionabout = QtWidgets.QAction(startView)
        self.actionabout.setObjectName("actionabout")
        self.menuhelp.addAction(self.actionabout)
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(startView)
        QtCore.QMetaObject.connectSlotsByName(startView)

    def retranslateUi(self, startView):
        _translate = QtCore.QCoreApplication.translate
        startView.setWindowTitle(_translate("startView", "快证件照"))
        self.btn_exit.setText(_translate("startView", "退出"))
        self.btn_open.setText(_translate("startView", "打开照片"))
        self.menuhelp.setTitle(_translate("startView", "帮助"))
        self.actionabout.setText(_translate("startView", "关于"))
