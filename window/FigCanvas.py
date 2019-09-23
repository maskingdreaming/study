# !/Users/yincg/PycharmProjects/environments/venv_study/bin/python3
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure


class FigCanvas(FigureCanvas):
    def __init__(self, parent=None, dpi=100, width=5, height=4):
        # super(FigCanvas, self).__init__(self)

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def start_fit_plot(self, data):

        self.axes.plot()
        pass

