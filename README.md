<!--
 * @Author: YHH
 * @Date: 2020-06-18 21:01:51
 * @LastEditTime: 2020-06-19 21:16:24
 * @Description: In User Settings Edit
 * @FilePath: \CardPhoto\README.md
--> 
# 前言
1. 这是我第一次接触opencv 而写的程序，可以说bug 有点多。但是我学到了很多关于图像方面的知识，顺便复习了下python。另外吹一波PyCharm 的debug 功能是真的强。
2. 部分代码来自opencv 的帮助文档。

# 项目配置
### 项目环境
    python 3.5
### 模块安装
    pip opencv-python
    pip numpy
    pip dlib

# 关于各个文件
### 1. save 文件夹
照片保存的默认文件夹。
### 2. src 文件夹
里面有用于测试的照片、程序的介绍ppt、思维导图、界面的ui 文件和活动图等。
### 3. temp 文件夹
用于存放程序生成的中间文件(其实就一张照片)。
### 4. StartWindow.py、MainWindow.py
用PyQt uic 转换得到的界面代码。
### 5. UseViews.py
调用上述两个界面代码的的代码。
### 6. main.py
程序运行脚本。