# !/Users/yincg/PycharmProjects/environments/venv_study/bin/python3
import pandas as pd
from PyQt5 import QtWidgets

from com.qtproject.window.FigCanvas import FigCanvas
from com.qtproject.window.RightWidget import RightWidget

import numpy as np
import math
from scipy.interpolate import Rbf


# file button触发的方法
def data_file_btn(main_window, btn_name):
    while len(main_window.scroll_widget) > 0:
        main_window.right_main_layout.removeWidget(main_window.scroll_widget.pop(0))

    for temp in main_window.btn_widget:
        if not temp == btn_name:
            pass

    if btn_name in main_window.btn_widget:
        show_widget(btn_name, main_window)
    else:
        file_tool_btn, file_widget = RightWidget.file_widget()
        main_window.btn_widget[btn_name] = file_widget
        main_window.right_main_layout.addWidget(file_widget)
        file_tool_btn.clicked.connect(main_window.open_file)


# 通过此方法显示和隐藏btn_name对应的weidget
def show_widget(btn_name, main_window):
    for tmp in main_window.btn_widget.keys():
        if tmp == btn_name:
            main_window.btn_widget[tmp].show()
        else:
            main_window.btn_widget[tmp].hide()


# 拟合
def do_fit_func(main_window, btn_name):
    while len(main_window.scroll_widget) > 0:
        main_window.right_main_layout.removeWidget(main_window.scroll_widget.pop(0))

    if btn_name in main_window.btn_widget:
        main_window.btn_widget.pop(btn_name)

    # if btn_name in main_window.btn_widget:
    #     show_data(main_window)
    #     show_widget(btn_name, main_window)
    # else:
    scroll = show_data(main_window)
    if scroll:
        main_window.btn_widget[btn_name] = scroll
        show_widget(btn_name, main_window)


# 解析数据并展示
def show_data(main_window):
    main_window.ccm = {}  # 重置ccm对象
    main_window.analog_value = {}  # 重置analog对象
    if main_window.file_path:
        file_path = main_window.file_path  # 文件路径
        fit_widget, fit_layout = RightWidget.fit_widget()
        #     main_window.btn_widget[btn_name] = fit_widget
        # file_path = main_window.file_path  # 文件路径
        df = pd.read_excel(file_path)
        data = pd.DataFrame(df.values)

        data_columns = data.iloc[0, 1:]
        data_index = data.iloc[1:, 0]
        data_content = data.iloc[1:, 1:]

        data_content.index = data_index.tolist()
        data_content.columns = data_columns.tolist()

        main_window.pd_data = data_content
        main_window.pd_index = data_index.tolist()
        main_window.pd_columns = data_columns.tolist()

        x = np.around(data.iloc[0, 1:].values.astype(float), decimals=10)
        row = data.shape[0]
        start_row = 0
        start_col = 0
        for i in range(row):

            if i != 0:
                iTitle = str(i)
                y = np.around(data.iloc[i, 1:].values.astype(float), decimals=10)
                fig_canvas = FigCanvas(fit_widget)
                fig_canvas.axes.plot(x, y, 'r--o', label='p')

                label_widget = QtWidgets.QWidget()
                label_layout = QtWidgets.QGridLayout(label_widget)
                label_layout.setSpacing(0)
                val_start = 0
                for j in range(1, 5, 1):  # 一次二次三次四次拟合
                    f = np.polyfit(x, y, j)
                    p = np.poly1d(f)
                    yvals = p(x)  # 拟合值

                    if i in main_window.analog_value:  # 存储模拟值
                        main_window.analog_value[i].append(yvals.tolist())
                    else:
                        main_window.analog_value[i] = [yvals.tolist()]

                    jName = str(j)
                    xi = np.linspace(x.min(), x.max(), 100)
                    rbf = Rbf(x, yvals)
                    fi = rbf(xi)

                    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
                    # plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）plt.plot(x, yvals, 'b*')

                    fig_canvas.axes.plot(xi, fi, label=jName + 'time')  # 拟合曲线
                    fig_canvas.axes.legend(loc='best')
                    fig_canvas.fig.suptitle('juli' + iTitle)
                    ym = np.array(y)  # 原值
                    yMean = np.mean(ym)  # 原值平均数
                    varX = 0  # R方残差模上部公式
                    varY = 0  # R方下部公式
                    for n in range(0, len(y)):  # 依次遍历
                        y_v = y[n] - yvals[n]
                        y_m = y[n] - yMean
                        varX += y_v ** 2
                        varY += y_m ** 2
                    CCM = math.sqrt(varX)  # 残差模

                    if j in main_window.ccm:
                        main_window.ccm[j].append(CCM)
                    else:
                        main_window.ccm[j] = [CCM]

                    r = 1 - varX / varY

                    label_ccm_head = QtWidgets.QLabel()
                    label_ccm_head.setText(jName + 'time CCM：')

                    label_ccm_value = QtWidgets.QLabel()
                    label_ccm_value.setText(str(CCM))

                    label_rval_head = QtWidgets.QLabel()
                    label_rval_head.setText(jName + 'time R方：')
                    label_rval_value = QtWidgets.QLabel()
                    label_rval_value.setText(str(r))

                    label_layout.addWidget(label_ccm_head, val_start, 0, 1, 2)
                    label_layout.addWidget(label_ccm_value, val_start, 2, 1, 6)
                    label_layout.addWidget(label_rval_head, val_start + 1, 0, 1, 2)
                    label_layout.addWidget(label_rval_value, val_start + 1, 2, 1, 6)

                    val_start = val_start + 2

                fig_canvas.axes.grid(True)
                # fig_canvas.axes.plot()

                fit_layout.addWidget(fig_canvas, start_row, start_col, 8, 8)

                fit_layout.addWidget(label_widget, start_row, start_col + 8, 8, 4)

                start_row = start_row + 8
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(fit_widget)
        main_window.right_main_layout.addWidget(scroll)
        main_window.scroll_widget.append(scroll)
        return scroll
    else:
        main_window.tool_box.setCurrentIndex(0)
        main_window.source_button.click()


# 导出功能实现
def do_export_func(main_window, btn_name):
    while len(main_window.scroll_widget) > 0:
        main_window.right_main_layout.removeWidget(main_window.scroll_widget.pop(0))

    if btn_name in main_window.btn_widget:
        main_window.btn_widget.pop(btn_name)

    if main_window.file_path:
        # if btn_name in main_window.btn_widget:
        #     ccm_scroll(btn_name, main_window)
        #     show_widget(btn_name, main_window)
        # else:
        scroll = ccm_scroll(btn_name, main_window)
        main_window.btn_widget[btn_name] = scroll
        show_widget(btn_name, main_window)
    else:
        main_window.tool_box.setCurrentIndex(0)
        main_window.source_button.click()


def ccm_scroll(btn_name, main_window):
    ccm_widget, ccm_layout = RightWidget.export_widget()
    main_window.btn_widget[btn_name] = ccm_widget
    fig_canvas = FigCanvas(ccm_widget, width=6, height=4.8)
    key_arr = main_window.ccm.keys()
    for key in key_arr:
        x_index = [i for i in range(1, len(main_window.ccm[key]) + 1, 1)]
        fig_canvas.axes.plot(x_index, main_window.ccm[key], label=str(key) + 'time CCM')
        fig_canvas.fig.suptitle('CCM')
    fig_canvas.axes.legend(loc='best')
    fig_canvas.axes.grid(True)
    data_widget = QtWidgets.QWidget()
    data_widget.setMaximumWidth(750)
    data_layout = QtWidgets.QVBoxLayout(data_widget)
    ccm_layout.addWidget(data_widget)
    data_layout.addWidget(fig_canvas)
    # 添加下拉框选择
    new_key_arr = [str(x) for x in key_arr]  # 下拉框数据数字该字符串
    combo_box = QtWidgets.QComboBox()  # 下拉选择控件
    combo_box.addItems(new_key_arr)
    main_window.combox_select = combo_box  # combox_select赋值
    select_label = QtWidgets.QLabel('最优选择')
    data_layout.addWidget(select_label)
    data_layout.addWidget(combo_box)
    export_widget = QtWidgets.QWidget()
    export_layout = QtWidgets.QHBoxLayout(export_widget)
    export_button = QtWidgets.QPushButton('导出')  # 导出按钮
    export_button.clicked.connect(main_window.export_file)  # 导出按钮事件
    export_layout.addStretch(0)
    export_layout.addWidget(export_button)
    data_layout.addWidget(export_widget)
    scroll = QtWidgets.QScrollArea()  # 滚动控件
    scroll.setWidget(ccm_widget)  # 设置滚动
    main_window.right_main_layout.addWidget(scroll)
    main_window.scroll_widget.append(scroll)
    return scroll
