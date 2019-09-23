# !/Users/yincg/PycharmProjects/environments/venv_study/bin/python3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QCursor


class RightWidget:

    @staticmethod
    def file_widget():
        file_widget = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(file_widget)

        file_tool_btn = QtWidgets.QToolButton()
        file_tool_btn.setText('上传文件')
        file_tool_btn.setIcon(QtGui.QIcon('../resources/background.png'))
        file_tool_btn.setIconSize(QtCore.QSize(150, 150))
        file_tool_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        file_tool_btn.setCursor(QCursor(QtCore.Qt.OpenHandCursor))
        file_tool_btn.setStyleSheet('''
            QToolButton{
                border:none;
                text-align: center;
            }
        ''')

        h_layout.addStretch(0)
        h_layout.addWidget(file_tool_btn)
        h_layout.addStretch(0)
        return file_tool_btn, file_widget

    @staticmethod
    def fit_widget():
        fit_wdiget = QtWidgets.QWidget()
        fit_layout = QtWidgets.QGridLayout(fit_wdiget)
        return fit_wdiget, fit_layout

    @staticmethod
    def export_widget():
        export_wdiget = QtWidgets.QWidget()
        export_layout = QtWidgets.QGridLayout(export_wdiget)
        return export_wdiget, export_layout