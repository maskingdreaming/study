# !/Users/yincg/PycharmProjects/environments/venv_study/bin/python3
import sys
import time

import pandas as pd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget

from com.qtproject.window.BtnFunc import data_file_btn, do_fit_func, do_export_func


class MainWindows(QMainWindow):
    func_btn_clicked_signal = pyqtSignal()

    def __init__(self):
        super(MainWindows, self).__init__()
        self.init_btn_func()
        self.init_btn_widget()
        self.func_btn_arr = []
        self.scroll_widget = []
        self.init_window(self)
        self.file_path = None
        self.ccm = {}
        self.pd_data = None  # 数据-矩阵
        self.pd_index = None  # 索引
        self.pd_columns = None  # 列
        self.analog_value = {}  # 所有数据的模拟值
        self.combox_select = None  # 下拉选择控件
        self.center()

    # 初始化按钮对应的点击事件
    def init_btn_func(self):
        self.btn_func = {
            'data_file_btn': data_file_btn,
            'fit_func_btn': do_fit_func,
            'export_func_btn': do_export_func
        }

    # 只是初始化按钮对应widget，初始是个空字典，添加按钮时会同步添加这个widget
    def init_btn_widget(self):
        self.btn_widget = {}

    # 初始窗口元素
    def init_window(self, main_window):
        self.setFixedSize(1000, 800)

        self.edit_main_widget(main_window)

        self.edit_left_widget()  # 编辑左侧控件
        self.edit_right_widget()  # 编辑右侧控件

        self.bind_click_event()

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

        self.source_button.click()

    # 绑定按钮点击时间
    def bind_click_event(self):
        for temp in self.func_btn_arr:
            temp.clicked.connect(self.click_event)

    # 按钮点击事件触发的回调函数
    def click_event(self):
        sender = self.sender()
        # 选中效果实现
        self.do_click(sender)

    # 执行btn click的内容
    def do_click(self, btn):
        for tmp in self.func_btn_arr:
            if tmp == btn:
                tmp.setStyleSheet('''
                    border-left:4px solid red;font-weight:700;
                ''')
            else:
                tmp.setStyleSheet('''''')
        self.do_something(btn.objectName())

    # 执行按钮对应功能
    def do_something(self, obj_name):
        if obj_name in self.btn_func:
            self.btn_func[obj_name](self, obj_name)

    # 主控件
    def edit_main_widget(self, main_window):
        self.main_widget = QtWidgets.QWidget(main_window)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QtWidgets.QGridLayout(self.main_widget)  # 添加主窗口网格布局

    # 左侧控件
    def edit_left_widget(self):
        self.left_widget = QtWidgets.QWidget()  # 左侧控件
        self.left_widget.setObjectName('left_widget')

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)
        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}

            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        self.left_main_layout = QtWidgets.QGridLayout(self.left_widget)

        self.left_main_layout.setSpacing(20)

        self.left_tool_button()  # 按钮：关闭，缩小，放大

        self.tool_box = QtWidgets.QToolBox()  # 创建toolbox
        self.tool_box.setStyleSheet('''
            QToolBox::tab{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }

            QToolBox::tab:selected{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }

            QToolBox{
                background:gray;
            }
        ''')

        self.box_data_source = QtWidgets.QWidget()  # 数据栏
        self.box_data_source.setStyleSheet('''
            QPushButton:hover{border-left:4px solid red;font-weight:700;}
            QWidget{
                background:gray;
            }
        ''')
        self.box_source_layout = QtWidgets.QVBoxLayout(self.box_data_source)
        self.source_button = QtWidgets.QPushButton('文件')  # 数据按钮
        self.source_button.setObjectName('data_file_btn')

        self.func_btn_arr.append(self.source_button)

        self.box_source_layout.addWidget(self.source_button)
        self.box_source_layout.addStretch(0)

        self.box_widget1 = QtWidgets.QWidget()  # 拟合栏
        self.box_widget1.setStyleSheet('''
            QPushButton:hover{border-left:4px solid red;font-weight:700;}
            QWidget{
                background:gray;
            }
        ''')
        self.box_layout1 = QtWidgets.QVBoxLayout(self.box_widget1)
        self.fit_button = QtWidgets.QPushButton('方程拟合')  # 方程拟合按钮
        self.fit_button.setObjectName('fit_func_btn')
        self.func_btn_arr.append(self.fit_button)

        self.box_layout1.addWidget(self.fit_button)  # 方程拟合按钮添加

        self.export_button = QtWidgets.QPushButton('导出')  # 导出按钮
        self.export_button.setObjectName('export_func_btn')
        self.func_btn_arr.append(self.export_button)

        self.box_layout1.addWidget(self.export_button)  # 导出按钮

        self.box_layout1.addStretch(0)

        self.box_widget2 = QtWidgets.QWidget()  # 求值栏
        self.box_widget2.setStyleSheet('''
            QPushButton:hover{border-left:4px solid red;font-weight:700;}
            QWidget{
                background:gray;
            }
        ''')
        self.box_layout2 = QtWidgets.QVBoxLayout(self.box_widget2)

        self.original_button = QtWidgets.QPushButton('原值')  # 求值按钮
        self.original_button.setObjectName('original_func_btn')
        self.box_layout2.addWidget(self.original_button)
        self.func_btn_arr.append(self.original_button)

        self.analog_button = QtWidgets.QPushButton('模拟值')  # 模拟值按钮
        self.analog_button.setObjectName('analog_func_btn')
        self.box_layout2.addWidget(self.analog_button)
        self.func_btn_arr.append(self.analog_button)

        self.ppm_button = QtWidgets.QPushButton('改正值')  # 改正值按钮
        self.ppm_button.setObjectName('ppm_func_btn')
        self.box_layout2.addWidget(self.ppm_button)
        self.func_btn_arr.append(self.ppm_button)

        self.dval_button = QtWidgets.QPushButton('差值')  # 差值按钮
        self.dval_button.setObjectName('dval_func_btn')
        self.box_layout2.addWidget(self.dval_button)
        self.func_btn_arr.append(self.dval_button)
        self.box_layout2.addStretch(0)

        self.tool_box.addItem(self.box_data_source, '数据')
        self.tool_box.addItem(self.box_widget1, '拟合')
        # self.tool_box.addItem(self.box_widget2, '求值')

        self.left_main_layout.addWidget(self.tool_box, 3, 0, 11, 3)

    # 按钮组 后期可能会有优化
    def left_tool_button(self):
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.setFixedSize(10, 10)
        self.left_visit = QtWidgets.QPushButton("")  # 隐藏按钮
        self.left_visit.setFixedSize(10, 10)
        self.left_mini = QtWidgets.QPushButton("")  # 最大化按钮
        self.left_mini.setFixedSize(10, 10)
        self.left_main_layout.addWidget(self.left_close, 0, 0, 1, 1)
        # self.left_main_layout.addWidget(self.left_mini, 0, 1, 1, 1)  # 功能为实现，暂不添加显示
        # self.left_main_layout.addWidget(self.left_visit, 0, 2, 1, 1)
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:4px;}QPushButton:hover{background:red;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:4px;}QPushButton:hover{background:yellow;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:4px;}QPushButton:hover{background:green;}''')
        self.left_close.clicked.connect(self.close)
        # self.left_mini.clicked.connect()

    # 右侧控件
    def edit_right_widget(self):
        self.right_widget = QtWidgets.QWidget()  # 右侧控件
        self.right_widget.setObjectName('right_widget')

        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
        ''')
        self.right_main_layout = QtWidgets.QGridLayout(self.right_widget)

    # 打开文件
    def open_file(self):
        # noinspection PyCallByClass
        file_path = QFileDialog.getOpenFileName(self, '选取文件', '/', 'Excel files(*.xlsx *.xls)')
        if file_path[0]:
            self.file_path = file_path[0]
            self.tool_box.setCurrentIndex(1)
            self.fit_button.click()

    # 导出文件
    def export_file(self):
        # print(self.combox_select.currentText())  # 获取选择的值
        p_level = int(self.combox_select.currentText())
        analog_value = []  # 写入文件的模拟值

        for i in self.analog_value:  # 获取数据
            analog_value.append(self.analog_value[i][p_level - 1])

        analog_dataframe = pd.DataFrame(data=analog_value, index=self.pd_index, columns=self.pd_columns)  # 写入文件的模拟值矩阵

        d_dataframe = analog_dataframe - analog_dataframe.iloc[len(self.pd_index) - 1, len(self.pd_columns) - 1]  # 取得差值

        ft = '%Y-%m-%d %H:%M:%S'
        now_time = time.strftime(ft, time.localtime())
        # self.pd_data  # 原值
        file = QFileDialog.getSaveFileName(self, '保存文件', '/example_' + now_time + '.xlsx', 'Excel files(*.xlsx *.xls)')

        file_path = file[0]

        if file_path:
            with pd.ExcelWriter(file_path, enginge='openpyxl') as excel_writer:  # 开始写入excel
                length = len(self.pd_index) + 2
                # excel_writer.write_cells(startrow=0, sheet_name='v1')
                self.pd_data.to_excel(excel_writer, startrow=1, sheet_name='v1')
                analog_dataframe.to_excel(excel_writer, startrow=1 + length * 1, sheet_name='v1')
                d_dataframe.to_excel(excel_writer, startrow=1 + length * 2, sheet_name='v1')
            # excel_writer.save()
        else:
            pass

    # 设置居中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindows()
    win.show()
    sys.exit(app.exec_())
