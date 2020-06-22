# -*- coding: gbk -*-
'''
@Author: YHH
@Date: 2020-06-06 20:58:56
@LastEditTime: 2020-06-22 14:27:52
@Description: 驱动程序
@FilePath: \CardPhoto\main.py
'''

import sys
from PyQt5 import QtWidgets
from UseViews import StartView

app = QtWidgets.QApplication(sys.argv)
start = StartView()
start.show()
sys.exit(app.exec_())
