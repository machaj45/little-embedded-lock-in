import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class HelpWindow(QWidget):

    def __init__(self, icon):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,210,0,110)
        self.label = QLabel()
        self.label_link = QLabel()

        self.label.setText("This is help to lock-in amplifier that was created by Jan Machálek,\n"
                           "as part of my Diploma Thesis. There is two mods to select from sin mode and rect mode\n"
                           "In sin mode you get gain and phase in rect mod you get gain and output voltage.\n"
                           "How to start?\n"
                           "1) you have to connect device with right firmware.\n"
                           "2) then you have to set up generator on channel one.\n"
                           "3) you have to select number of samples per period\n"
                           "4) you can select continuous or single measurement\n"
                           "   or you can use automatic measurement\n"
                           "   this option opens dialog to specify csv file with\n"
                           "   frequencies that you want to measure on.\n"
                           "   after automatic measurements is completed you can\n"
                           "   use save as button to save data that has been measured.\n"
                           "\n"
                           "How to select another lock-in? "
                           "You can use scan button that will update dropdown at the top\n"
                           "of application then you can select comport that you want\n"
                           "and then connect to that port using connect button.\n\n"
                           "For more information look at:\n"
                           )
        url_link = "<a href=\"https://github.com/machaj45/little-embedded-lock-in/blob/main/Manual/manual.pdf\">Manual PDF</a>"
        self.label_link.setOpenExternalLinks(True)
        self.label_link.setText(url_link)
        layout.addWidget(self.label)
        layout.addWidget(self.label_link)

        self.setLayout(layout)
        self.icon = icon
        self.setWindowIcon(self.icon)

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
