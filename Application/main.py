#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow
from PyQt5.QtCore import Qt
from lockin import Form


class LockInHandler:
    def __init__(self):
        self.windows = []

    def create_lock_in(self):
        if len(self.windows) <= 1:
            self.windows.append(Form())
            self.windows[-1].show()
            print(len(self.windows))


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.lock_in_handler = LockInHandler()
        self.setWindowTitle("My Awesome App")
        label = QLabel("This is a PyQt5 window!")
        label.setAlignment(Qt.AlignCenter)
        button = QPushButton("This is a PyQt5 button!")
        button.clicked.connect(self.lock_in_handler.create_lock_in)
        self.setCentralWidget(label)
        self.setCentralWidget(button)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
