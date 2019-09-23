# coding:utf-8
# !/Users/yincg/PycharmProjects/environments/venv_study/bin/python3
import random

import sys

import matplotlib
from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout, QApplication
from numpy.ma import arange, sin
import numpy as np
from qtpy import QtCore

matplotlib.use("Qt5Agg")  # 声明使用QT5

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


class FigureTemplate(FigureCanvas):
    """FigureCanvas的最终父类是QWidget"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # 新建一个绘图对象
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 建立一个子图， 如果建立复合图， 可以在这里修改
        self.axes = self.fig.add_subplot(111)

        # self.axes.hold()  # 每次绘图时都不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略， 意思是设置FigureCanvas，使之尽可能向外填充空间'''
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def start_static_plot(self):
        self.fig.suptitle('绘制静态图')
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * np.pi * t)

        self.axes.plot()
        self.axes.set_ylabel('静态图：Y轴')
        self.axes.set_xlabel('静态图：X轴')

        self.axes.grid(True)

    def start_dynamic_plot(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def update_figure(self):
        self.fig.suptitle('测试动态图')
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([1, 2, 3, 4], l, 'r')
        self.axes.set_ylabel('动态图：Y轴')
        self.axes.set_xlabel('动态图：X轴')
        self.axes.grid(True)
        self.draw()


class MatplotWidget(QWidget):

    def __init__(self, parent=None):
        super(MatplotWidget, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.mpl = FigureTemplate(self)

        # self.mpl.start_dynamic_plot()
        self.mpl.start_static_plot()

        self.layout.addWidget(self.mpl)
        self.mpl_tool = NavigationToolbar(self.mpl, self)
        self.layout.addWidget(self.mpl_tool)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotWidget()
    # ui.mpl.start_dynamic_plot()

    ui.show()
    sys.exit(app.exec_())
