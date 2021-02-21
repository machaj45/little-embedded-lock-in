from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import pyqtgraph


class PlotWindow(QWidget):

    def __init__(self, gui):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Plot")
        self.graphWidget = pyqtgraph.PlotWidget()
        # self.graphWidget.setMouseEnabled(x=False, y=False)
        self.layout.addWidget(self.graphWidget)
        self.gui = gui
        self.mode_nr = True
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(500)
        self.plot_data_now = True
        self.setWindowIcon(self.gui.icon)
        self.horizontal = QHBoxLayout()
        self.button_normal = QPushButton("Normalized ref")
        self.button_raw = QPushButton("Raw ref")
        self.button_raw.clicked.connect(self.on_raw)
        self.button_normal.clicked.connect(self.on_normal)
        self.horizontal.addWidget(self.button_normal)
        self.horizontal.addWidget(self.button_raw)
        self.layout.addLayout(self.horizontal)

    def on_raw(self):
        self.mode_nr = False
        self.plot_data()
        pass

    def on_normal(self):
        self.mode_nr = True
        self.plot_data()
        pass

    def _update(self):
        if self.plot_data_now:
            self.plot_data()
            self.plot_data_now = False

    def plot_data_set(self):
        self.plot_data_now = True

    def plot_data(self):
        self.graphWidget.clear()
        self.graphWidget.showGrid(x=True, y=True, alpha=0.3)
        if self.mode_nr:
            self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.dut))], self.gui.dut,
                                  pen=pyqtgraph.mkPen(color=(255, 0, 0)), name='dut(t)')
            self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.ref_norm))],
                                  self.gui.ref_norm,
                                  pen=pyqtgraph.mkPen(color=(0, 255, 0)), name='ref_norm(t)')
            if self.gui.sin_square_mode:
                self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.X))], self.gui.X,
                                      pen=pyqtgraph.mkPen(color=(0, 100, 255)), name='U2')
            if not self.gui.sin_square_mode:
                self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.ref90_norm))],
                                      self.gui.ref90_norm,
                                      pen=pyqtgraph.mkPen(color=(0, 100, 255)), name='ref_norm(t+90°)')
        else:
            self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.dut))], self.gui.dut,
                                  pen=pyqtgraph.mkPen(color=(255, 0, 0)), name='dut(t)')
            self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.ref))],
                                  self.gui.ref,
                                  pen=pyqtgraph.mkPen(color=(0, 255, 0)), name='ref(t)')
            if self.gui.sin_square_mode:
                self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.X))], self.gui.X,
                                      pen=pyqtgraph.mkPen(color=(0, 100, 255)), name='U2')
            if not self.gui.sin_square_mode:
                self.graphWidget.plot([x * 1 / self.gui.sf for x in range(0, len(self.gui.ref90))],
                                      self.gui.ref90,
                                      pen=pyqtgraph.mkPen(color=(0, 100, 255)), name='ref(t+90°)')
        self.graphWidget.addLegend()
        # self.graphWidget.setMouseEnabled(x=True, y=True)
