import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class HelpWindow(QWidget):

    def __init__(self, icon):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.icon = icon

        datafile = "data/hi_res_icon.png"
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
        else:
            datafile = "hi_res_icon.png/hi_res_icon.png"
            datafile = os.path.join(sys.prefix, datafile)
        self.icon = QtGui.QIcon(datafile)
        self.setFixedSize(410, 600)
        self.setWindowTitle("Help for Lock-in Amplifier")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, 410, 195, self.icon.pixmap(410, 195))
