#!/usr/bin/python
# -*- coding: utf-8 -*-
import queue
import sys

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QApplication, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider, QFileDialog, QPlainTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui
from SquareCalculation import SquareCalculation
from HelpWindow import HelpWindow
from PlotWindow import PlotWindow
from SerialThread import SerialThread
from Worker import Worker
from Reader import Reader
from DualPhase import DualPhase
import statistics
import csv
import time
import numpy as np
import os
import urllib.request
from bs4 import BeautifulSoup
import socket
import serial
import re


class MainWindow(QDialog):
    def open_plot_window(self):
        self.plot_window.show()
        self.plot_window.plot_data_set()

    @staticmethod
    def get_online_versions():
        online_versions = []
        url = "https://github.com/machaj45/little-embedded-lock-in/tags"
        try:
            file = urllib.request.urlopen(url, timeout=1)
        except urllib.error.URLError as e:
            print(e)
            return online_versions
            pass
        except socket.timeout as e:
            print(e)
            return online_versions
            pass
        soup = BeautifulSoup(file, 'html.parser')
        for div in soup.find_all('div', {'class': 'Box-row position-relative d-flex'}):
            for a in div.find_all('a', {'class': ''}):
                for reg in re.findall(r'v\d.*\d.*\d', str(a)):
                    if reg not in online_versions:
                        online_versions.append(reg)
        return online_versions

    def automatic_update_check(self):
        online_versions = self.get_online_versions()
        if len(online_versions) == 0:
            self.text_to_update_3.put('Unable to check version!' + '\n')
            return
        if self.gui_version == online_versions[0]:
            self.text_to_update_3.put('Application is update!\t version: ' + self.gui_version + '\n')
        else:
            self.text_to_update_3.put('Application needs to be updated!' + '\n')
            self.text_to_update_3.put('Please download newer version from:\n' +
                                      'https://github.com/machaj45/little-embedded-lock-in/releases' + '\n')

    def show_new_window(self):
        self.help_window.show()

    def closeEvent(self, event):
        self.serial_thread.running = False
        self.help_window.close()
        self.plot_window.close()
        if self.serial_thread is not None and self.serial_thread is not None and self.serial_thread.serial is not None:
            self.serial_thread.serial.close()
        self.reader.stop = True
        print('Window closed')

    def on_edit_change_frequency_left(self):
        if self.edit_frequency_left.text() != "":
            a = float(self.edit_frequency_left.text())
            if 0 < a <= 130000:
                self.slider_frequency_left.setValue(float(self.edit_frequency_left.text()))
                self.sf = int(self.sample_per_period * a)
                self.st = self.select_st_for_sf()
                self.label_spp.setText(
                    "Samples per period = {0} [-], Sampling frequency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(
                        int(self.sample_per_period), self.sf, self.st))
            else:
                self.edit_frequency_left.setText("1")

    def on_edit_change_amplitude_left(self):
        if self.edit_amplitude_left.text() != "":
            a = int(self.edit_amplitude_left.text())
            if 0 < a <= 100:
                self.slider_amplitude_left.setValue(int(self.edit_amplitude_left.text()))
            else:
                self.edit_amplitude_left.setText("1")

    def on_edit_change_offset_left(self):
        if self.edit_offset_left.text() != "":
            a = int(self.edit_offset_left.text())
            if 0 < a <= 3300:
                self.slider_offset_left.setValue(int(self.edit_offset_left.text()))
            else:
                self.edit_offset_left.setText("1")

    def e20(self):
        if self.edit20.text() != "":
            a = int(self.edit20.text())
            if 0 < a <= 130000:
                self.qs_slider20.setValue(int(self.edit20.text()))
            else:
                self.edit20.setText("1")

    def e25(self):
        if self.edit25.text() != "":
            a = int(self.edit25.text())
            if 0 < a <= 100:
                self.qs_slider25.setValue(int(self.edit25.text()))
            else:
                self.edit25.setText("1")

    def e26(self):
        if self.edit26.text() != "":
            a = int(self.edit26.text())
            if 0 < a <= 3300:
                self.qs_slider26.setValue(int(self.edit26.text()))
            else:
                self.edit26.setText("1")

    def on_slider_change_frequency_left(self, value):
        self.edit_frequency_left.setText(str(value))
        pass

    def on_slider_change_amplitude_left(self, value):
        self.edit_amplitude_left.setText(str(value))
        pass

    def on_slider_change_offset_left(self, value):
        self.edit_offset_left.setText(str(value))
        pass

    def slider_update_20(self, value):
        self.edit20.setText(str(value))
        pass

    def slider_update_25(self, value):
        self.edit25.setText(str(value))
        pass

    def slider_update_26(self, value):
        self.edit26.setText(str(value))
        pass

    def scan(self):
        self.serial_thread.available_ports.clear()
        self.drop_down_comports.clear()
        txt = "Available  port are: "
        for dev in serial.tools.list_ports.comports():
            if re.findall("STLink", str(dev)):
                txt += ("%s" % str(dev.device) + ', ')
                self.drop_down_comports.addItem(dev.device)
                self.serial_thread.available_ports.append(dev.device)
        txt = txt[:-2]
        if len(self.serial_thread.available_ports) > 0:
            self.text_to_update_3.put(txt + '\n')
        else:
            self.text_to_update_3.put("There are no available ports" + '\n')
        pass

    def connect(self):
        if len(self.serial_thread.available_ports) > 0:
            self.reader.in_scan_mode = True
            available_ports = self.serial_thread.available_ports
            self.running = False
            self.serial_thread.running = False
            time.sleep(1)
            self.serial_thread = SerialThread(115200, self, available_ports[self.selected_comport])
            self.running = True
            self.serial_thread.start()
            self.reader.serial_thread = self.serial_thread
            self.reader.in_scan_mode = False
            self.drop_down_comports.clear()
        else:
            self.text_to_update_3.put("There are not available ports!")
        pass

    def select_st_for_sf(self):
        cct = 0.194 / 14.0
        st = 1
        if 0 < self.sf <= 117532:
            st = 601.5 * cct
        if 117533 < self.sf <= 371984:
            st = 181.5 * cct
        if 371984 < self.sf <= 975202:
            st = 61.5 * cct
        if 975202 < self.sf <= 2255154:
            st = 19.5 * cct
        if 2255154 < self.sf <= 3608247:
            st = 7.5 * cct
        if 3608247 < self.sf <= 4244997:
            st = 4.5 * cct
        if 4244997 < self.sf <= 4810996:
            st = 2.5 * cct
        if 4810996 < self.sf <= 5154639:
            st = 1.5 * cct
        return st

    def comports(self, i):
        self.selected_comport = i
        pass

    def spp(self, i):
        i = i + 3
        self.serial_thread.ser_out("SAMP\n")
        self.serial_thread.ser_out(str(2 ** i) + "\n")
        self.sample_per_period = 2 ** i
        self.acquired_data_X = []
        self.acquired_data_Y = []
        ssp = float(2 ** i)
        self.sf = int(ssp * self.frequency_gen_1)
        self.st = self.select_st_for_sf()
        self.label_spp.setText(
            "Samples per period = {0} [-], Sampling frequency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(
                int(ssp), self.sf, self.st))

    def send_command(self):
        self.button_setup_left.setEnabled(True)
        self.button23.setEnabled(True)
        self.serial_thread.ser_out(self.edit27.text() + "\n")

    def load(self) -> bool:
        try:
            with open(self.loadFileName) as file:
                self.Freq = []
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    self.Freq.append(float(row[0]))
        except FileNotFoundError:
            self.text_to_update_3.put('FileNotFoundError load, load returning true' + '\n')
            return True
        return False

    def load_button(self):
        try:
            with open(self.loadFileName) as file:
                self.Freq = []
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    self.Freq.append(float(row[0]))
        except FileNotFoundError:
            self.text_to_update_3.put('File Not Found Please select valid file' + '\n')

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Frequency list in .csv format!", "",
                                                   "Table Files (*.csv)", options=options)
        if file_name:
            self.loadFileName = file_name
            self.text_to_update_3.put('Automatic measurement will be using frequencies from file:\n'
                                      + self.loadFileName + '\n')
        pass

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as", "", "Table Files (*.csv)", options=options)
        if file_name:
            self.saveFileName = file_name
        # print(file_name)
        if len(self.Freq) > 0:
            self.save()
            self.text_to_update_3.put('Data has been saved in to ' + self.saveFileName + '\n')
        else:
            self.text_to_update_3.put('No data to write to file ' + self.saveFileName + '\n')
        pass

    def toggle(self):
        if not self.sin_square_mode:
            self.button_toggle_sin_square.setText("Toggle to Sin")
            self.sin_square_mode = True
        else:
            self.button_toggle_sin_square.setText("Toggle to Square")
            self.sin_square_mode = False
        self.serial_thread.ser_out("SINS\n")
        time.sleep(0.1)
        self.set_everything_left_gen()

    def do_calculation(self):
        if self.do_calculation_flag:
            if self.sin_square_mode:
                SquareCalculation.square_calculation(self)
            else:
                DualPhase.dual_phase_decomposition(self)
                self.plot_window.plot_data_set()
            self.do_calculation_flag = False

    @staticmethod
    def crossings_nonzero_pos2neg(data):
        data = np.array(data)
        pos = data > 0
        return (pos[:-1] & ~pos[1:]).nonzero()[0]

    @staticmethod
    def crossings_nonzero_neg2pos(data):
        data = np.array(data)
        pos = data > 0
        return (pos[1:] & ~pos[:-1]).nonzero()[0]

    @staticmethod
    def crossings_nonzero_f(data):
        data = np.array(data)
        pos = data > 0
        not_pos = ~pos
        return ((pos[:-1] & not_pos[1:]) | (not_pos[:-1] & pos[1:])).nonzero()[0][0]

    @staticmethod
    def crossings_nonzero_l(data):
        data = np.array(data)
        pos = data > 0
        not_pos = ~pos
        return ((pos[:-1] & not_pos[1:]) | (not_pos[:-1] & pos[1:])).nonzero()[0][-1]

    def start_stop_measurement(self):
        self.plot_window.graphWidget.clear()
        if self.worker is None:
            self.worker = Worker(self, self.serial_thread)
        self.button_automatic_measurement.setText("Stop Measurement")
        if self.worker.running:
            self.button_automatic_measurement_text = "Automatic Measurement"
            self.worker.stop = True
            time.sleep(1)
            self.worker = Worker(self, self.serial_thread)
        else:
            self.worker = Worker(self, self.serial_thread)
            self.running = True
            self.stop = False
            self.open_file_name_dialog()
            self.worker.start()
        if self.automatic_measurement_is_done:
            self.automatic_measurement_is_done = False
            self.worker = Worker(self, self.serial_thread)
            self.running = True
            self.stop = False
            self.worker.start()

    def draw6(self):
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit_frequency_left.text() + "\n")

    def save(self):
        if not self.sin_square_mode:
            row_list = [["f [Hz]", "gain [dB]", "phase [°]"]]
        else:
            row_list = [["f [Hz]", "U2 [V]", "Ts [us]"]]
        for i in range(0, len(self.Gain)):
            one_row_list = [self.Freq[i], self.Gain[i], self.Phase[i]]
            row_list.append(one_row_list)
        try:
            with open(self.saveFileName, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
        except FileNotFoundError as e:
            self.text_to_update_3.put(str(e))
        pass

    def read(self):
        if self.reader.con_flag_stop:
            return
        if not self.reader.con_flag:
            self.reader.con_flag = True
            self.button_continuous.setText("Stop continuous")
        else:
            self.reader.con_flag_stop = True
            self.button_continuous.setText("Continuous")

    def measure(self):
        self.reader.single_flag = True

    def start_left_gen(self):
        self.serial_thread.ser_out("START\n")
        self.serial_thread.ser_out("0\n")
        time.sleep(0.5)
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("0\n")
        a = (int(self.edit_offset_left.text()) / 3300) * (2 ** 12)
        if a >= 4095:
            a = 4095
        if a <= 0:
            a = 5000  # this is special case for zero
        self.serial_thread.ser_out(str(int(a)) + "\n")

    def start1(self):
        self.serial_thread.ser_out("START\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("1\n")
        a = (int(self.edit26.text()) / 3300) * (2 ** 12)
        if a <= 0:
            a = 1
        if a >= 4095:
            a = 4095
        self.serial_thread.ser_out(str(int(a)) + "\n")

    def stop_left_gen(self):
        self.serial_thread.ser_out("STOP\n")
        self.serial_thread.ser_out("0\n")

    def stop1(self):
        self.serial_thread.ser_out("STOP\n")
        self.serial_thread.ser_out("1\n")

    def sweep0(self):
        self.serial_thread.ser_out("SWEPS\n")
        self.serial_thread.ser_out("0\n")

    def sweep1(self):
        self.serial_thread.ser_out("SWEPS\n")
        self.serial_thread.ser_out("1\n")

    def set_everything_left_gen(self):
        self.plot_window.graphWidget.setMouseEnabled(x=False, y=False)
        self.data_bin = False
        self.serial_thread.send_all_counter = 0
        self.serial_thread.b = 0
        self.serial_thread.data = []
        self.text = []
        self.button_setup_left.setEnabled(False)
        self.serial_thread.ser_out("AMPL\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit_amplitude_left.text() + "\n")
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit_frequency_left.text() + "\n")
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("0\n")
        a = (int(self.edit_offset_left.text()) / 3300) * (2 ** 12)
        if a >= 4095:
            a = 4095
        if a <= 0:
            a = 5000  # this is special case for zero
        self.serial_thread.ser_out(str(int(a)) + "\n")

    def set_everything1(self):
        self.plot_window.graphWidget.setMouseEnabled(x=False, y=False)
        self.text = []
        self.serial_thread.send_all_counter = 0
        self.button23.setEnabled(False)
        self.serial_thread.ser_out("AMPL\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out(self.edit25.text() + "\n")
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out(self.edit20.text() + "\n")
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("1\n")
        a = (int(self.edit26.text()) / 3300) * (2 ** 12)
        if a <= 0:
            a = 1
        if a >= 4095:
            a = 4095
        self.serial_thread.ser_out(str(int(a)) + "\n")

    def update_text(self):
        try:
            self.button_automatic_measurement.setText(self.button_automatic_measurement_text)
            self.label_amplitude_left.setText(self.label_amplitude_left_text)
            self.label_offset_left.setText(self.label_offset_left_text)
            self.label_frequency_left.setText(self.label_frequency_left_text)
            self.label25.setText(self.label25_text)
            self.label26.setText(self.label26_text)
            self.label21.setText(self.label21_text)
            self.do_calculation()
            self.label_xy.setText(self.text_to_update)
            self.label_xy_2.setText(self.text_to_update_2)

            while not self.text_to_update_3.empty():
                new_text = str(self.text_to_update_3.get())
                if new_text != "":
                    self.plainText.moveCursor(QTextCursor.End)
                    if new_text.endswith('\n'):
                        self.plainText.insertPlainText(new_text)

                    else:
                        self.plainText.insertPlainText(new_text + '\n')
                 #   self.plainText.moveCursor(QTextCursor.End)
        except RuntimeError as a:
            print(a)

    def __init__(self, parent=None):

        self.selected_comport = 0
        self.serial_thread = SerialThread(115200, self, None)  # Start serial thread
        self.serial_thread.start()
        self.reader = Reader(self, self.serial_thread)  # Start reading thread
        self.reader.start()

        super(MainWindow, self).__init__(parent)
        font = self.font()
        font.setPointSize(10)
        self.window().setFont(font)
        self.setWindowTitle("Little Embedded Lock-in")
        datafile = "data/icon.ico"
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
        else:
            datafile = "icon.ico/icon.ico"
            datafile = os.path.join(sys.prefix, datafile)
        self.icon = QtGui.QIcon(datafile)
        self.setWindowIcon(self.icon)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.help_window = HelpWindow(self.icon)
        self.plot_window = PlotWindow(self)

        self.counter_of_drawing = 0
        self.gui_version = 'v1.0.7'
        self.fir_version = 'nop'
        self.loadFileName = 'frec.csv'
        self.saveFileName = 'data.csv'
        self.worker = None
        self.sf = 10
        self.worker = None
        self.backup1 = []
        self.backup2 = []
        self.serial_thread_is_running = False
        self.acquired_data_YY = []
        self.plot = False
        self.frequency_gen_1 = 100
        self.acquired_data_XX = []
        self.time_sample = 1
        self.acquired_data_ZZ = []
        self.data_probe = 0
        self.backup3 = []
        self.text_to_update = "After measurement data will be displayed here!"
        self.text_to_update_2 = "Program start"
        self.text_to_update_3 = queue.Queue()
        self.FreqMeasured = []
        self.Gain = []
        self.automatic_measurement_is_done = False
        self.sin_square_mode = False
        self.Phase = []
        self.last_data = ""
        self.stop = None
        self.Freq = []
        self.data_done = False
        self.dataX = 0
        self.dataY = 0
        self.data_ready = False
        self.dut = []
        self.ref = []
        self.running = None
        self.ref90 = []
        self.ref_norm = []
        self.ref90n = []
        self.X = []
        self.Y = []

        self.Xn = []
        self.Yn = []
        self.data_bin = False
        self.sample_per_period = 32
        self.acquired_data = []
        self.acquired_data_X = []
        self.acquired_data_Y = []
        self.last_vertical_maximum = 0
        self.acquired_data_Z = []
        self.text = []
        self.st = 1

        self.label_amplitude_left_text = "Amplitude"
        self.label_offset_left_text = "Offset"
        self.label_frequency_left_text = "Frequency"

        self.label25_text = "Amplitude"
        self.label26_text = "Offset"
        self.label21_text = "Frequency"
        self.do_calculation_flag = False
        self.layout_main_vertical = QVBoxLayout()

        self.layout_horizontal_connect = QHBoxLayout()
        self.layout_horizontal_connect_out = QVBoxLayout()

        self.layout_horizontal_gen = QHBoxLayout()
        self.layout_vertical_left_gen = QVBoxLayout()
        self.layout_vertical_right_gen = QVBoxLayout()
        self.layout_horizontal_left_gen = QHBoxLayout()
        self.layout_horizontal_right_gen = QHBoxLayout()

        self.layout_horizontal_bottom = QHBoxLayout()

        self.group_box_connectivity = QGroupBox("Connectivity")
        self.group_box_connectivity.setCheckable(False)
        self.group_box_left_gen = QGroupBox("Generator channel 1 - pin A2")
        self.group_box_left_gen.setCheckable(False)
        self.group_box_right_gen = QGroupBox("Generator channel 2 - pin D13")
        self.group_box_right_gen.setCheckable(False)
        self.group_box_ssp = QGroupBox("Sampling settings")
        self.group_box_ssp.setCheckable(False)
        self.group_box_out = QGroupBox("Output")
        self.group_box_out.setCheckable(False)

        self.group_box_left_gen.setLayout(self.layout_vertical_left_gen)
        self.group_box_right_gen.setLayout(self.layout_vertical_right_gen)
        self.layout_horizontal_connect_out.addLayout(self.layout_horizontal_connect)
        self.group_box_connectivity.setLayout(self.layout_horizontal_connect_out)

        self.label_amplitude_left = QLabel("Amplitude")
        self.edit_amplitude_left = QLineEdit("85")
        self.edit_amplitude_left.textChanged.connect(self.on_edit_change_amplitude_left)
        self.slider_amplitude_left = QSlider(Qt.Horizontal, self)
        self.slider_amplitude_left.setRange(0, 100)
        self.slider_amplitude_left.setFocusPolicy(Qt.NoFocus)
        self.slider_amplitude_left.setPageStep(1)
        self.slider_amplitude_left.valueChanged.connect(self.on_slider_change_amplitude_left)

        self.label_offset_left = QLabel("Offset")
        self.edit_offset_left = QLineEdit("250")
        self.edit_offset_left.textChanged.connect(self.on_edit_change_offset_left)
        self.slider_offset_left = QSlider(Qt.Horizontal, self)
        self.slider_offset_left.setRange(0, 3300)
        self.slider_offset_left.setFocusPolicy(Qt.NoFocus)
        self.slider_offset_left.setPageStep(1)
        self.slider_offset_left.valueChanged.connect(self.on_slider_change_offset_left)

        self.label_frequency_left = QLabel("Frequency")
        self.edit_frequency_left = QLineEdit("100")
        self.edit_frequency_left.textChanged.connect(self.on_edit_change_frequency_left)
        self.button_start_left = QPushButton("Start")
        self.button_stop_left = QPushButton("Stop")
        self.button_setup_left = QPushButton("Set up Generator 1")
        self.slider_frequency_left = QSlider(Qt.Horizontal, self)
        self.slider_frequency_left.setRange(0, 130000)
        self.slider_frequency_left.setFocusPolicy(Qt.NoFocus)
        self.slider_frequency_left.setPageStep(1)
        self.slider_frequency_left.valueChanged.connect(self.on_slider_change_frequency_left)

        self.layout_vertical_left_gen.addWidget(self.label_amplitude_left)
        self.layout_vertical_left_gen.addWidget(self.edit_amplitude_left)
        self.layout_vertical_left_gen.addWidget(self.slider_amplitude_left)
        self.layout_vertical_left_gen.addWidget(self.label_offset_left)
        self.layout_vertical_left_gen.addWidget(self.edit_offset_left)
        self.layout_vertical_left_gen.addWidget(self.slider_offset_left)
        self.layout_vertical_left_gen.addWidget(self.label_frequency_left)
        self.layout_vertical_left_gen.addWidget(self.edit_frequency_left)
        self.layout_vertical_left_gen.addWidget(self.slider_frequency_left)
        self.layout_vertical_left_gen.addLayout(self.layout_horizontal_left_gen)

        self.layout_horizontal_left_gen.addWidget(self.button_setup_left)
        self.layout_horizontal_left_gen.addWidget(self.button_start_left)
        self.layout_horizontal_left_gen.addWidget(self.button_stop_left)

        self.button_start_left.clicked.connect(self.start_left_gen)
        self.button_stop_left.clicked.connect(self.stop_left_gen)
        self.button_setup_left.clicked.connect(self.set_everything_left_gen)

        self.label25 = QLabel("Amplitude")
        self.edit25 = QLineEdit("50")
        self.edit25.textChanged.connect(self.e25)
        self.label26 = QLabel("Offset")
        self.edit26 = QLineEdit("400")
        self.edit26.textChanged.connect(self.e26)
        self.label21 = QLabel("Frequency")
        self.edit20 = QLineEdit("10")
        self.edit20.textChanged.connect(self.e20)

        self.edit27 = QLineEdit("Commands for Lock-in.\t Ex. \"IDN?\"")
        self.button20 = QPushButton("Start")
        self.button21 = QPushButton("Stop")
        self.button22 = QPushButton("Sweep")
        self.button23 = QPushButton("Set up Generator 2")
        self.qs_slider20 = QSlider(Qt.Horizontal, self)
        self.qs_slider20.setRange(0, 60000)
        self.qs_slider20.setFocusPolicy(Qt.NoFocus)
        self.qs_slider20.setPageStep(1)
        self.qs_slider20.valueChanged.connect(self.slider_update_20)
        self.qs_slider26 = QSlider(Qt.Horizontal, self)
        self.qs_slider26.setRange(0, 3300)
        self.qs_slider26.setFocusPolicy(Qt.NoFocus)
        self.qs_slider26.setPageStep(1)
        self.qs_slider26.valueChanged.connect(self.slider_update_26)
        self.qs_slider25 = QSlider(Qt.Horizontal, self)
        self.qs_slider25.setRange(0, 100)
        self.qs_slider25.setFocusPolicy(Qt.NoFocus)
        self.qs_slider25.setPageStep(1)
        self.qs_slider25.valueChanged.connect(self.slider_update_25)
        self.layout_vertical_right_gen.addWidget(self.label25)
        self.layout_vertical_right_gen.addWidget(self.edit25)
        self.layout_vertical_right_gen.addWidget(self.qs_slider25)
        self.layout_vertical_right_gen.addWidget(self.label26)
        self.layout_vertical_right_gen.addWidget(self.edit26)
        self.layout_vertical_right_gen.addWidget(self.qs_slider26)
        self.layout_vertical_right_gen.addWidget(self.label21)
        self.layout_vertical_right_gen.addWidget(self.edit20)
        self.layout_vertical_right_gen.addWidget(self.qs_slider20)
        self.layout_horizontal_right_gen.addWidget(self.button23)
        self.layout_horizontal_right_gen.addWidget(self.button20)
        self.layout_horizontal_right_gen.addWidget(self.button21)
        self.layout_vertical_right_gen.addLayout(self.layout_horizontal_right_gen)
        self.button20.clicked.connect(self.start1)
        self.button21.clicked.connect(self.stop1)
        self.button22.clicked.connect(self.sweep1)

        self.button23.clicked.connect(self.set_everything1)
        self.label_xy = QLabel("XY")
        font1 = self.font()
        font1.setPointSize(15)
        self.label_xy.setFont(font1)

        self.label_xy_2 = QLabel("XY")
        self.drop_down_comports = QComboBox()
        self.button_scan = QPushButton("Scan")
        self.button_connect = QPushButton("Connect")
        self.button_scan.clicked.connect(self.scan)
        self.button_connect.clicked.connect(self.connect)
        self.button_help = QPushButton("Help")
        self.button_help.clicked.connect(self.show_new_window)
        self.layout_horizontal_connect_out.addWidget(self.drop_down_comports)
        self.drop_down_comports.currentIndexChanged.connect(self.comports)
        self.layout_horizontal_connect.addWidget(self.button_scan)
        self.layout_horizontal_connect.addWidget(self.button_connect)
        self.layout_horizontal_connect.addWidget(self.button_help)
        self.layout_main_vertical.addWidget(self.group_box_connectivity)
        self.layout_horizontal_gen.addWidget(self.group_box_left_gen)
        self.layout_horizontal_gen.addWidget(self.group_box_right_gen)
        self.layout_main_vertical.addLayout(self.layout_horizontal_gen)
        self.label_spp = QLabel("Samples per period")
        self.button_spp = QPushButton("Set Samples per period")
        self.button_load = QPushButton("Load")
        self.button_toggle_sin_square = QPushButton("Toggle to Square")
        self.button_draw_data = QPushButton("Draw data")
        self.button_load.setEnabled(True)
        self.button_toggle_sin_square.setEnabled(True)
        self.button_automatic_measurement = QPushButton("Automatic Measurement")
        self.button_automatic_measurement_text = "Automatic Measurement"
        self.button_save_as = QPushButton("Save as")
        self.button_send_command = QPushButton("Send command")
        self.button_continuous = QPushButton("Continuous")
        self.button_single = QPushButton("Single")
        self.button_continuous.clicked.connect(self.read)
        self.button_single.clicked.connect(self.measure)
        self.button_load.clicked.connect(self.load_button)
        self.button_toggle_sin_square.clicked.connect(self.toggle)
        self.button_draw_data.clicked.connect(self.open_plot_window)
        self.button_automatic_measurement.clicked.connect(self.start_stop_measurement)
        self.button_save_as.clicked.connect(self.save_file_dialog)
        self.button_send_command.clicked.connect(self.send_command)
        self.drop_down_spp = QComboBox()
        for i in range(3, 11):
            self.drop_down_spp.addItem(str(2 ** i))
        self.drop_down_spp.currentIndexChanged.connect(self.spp)

        self.layout_vertical_ssp = QVBoxLayout()
        self.layout_vertical_ssp.addWidget(self.label_spp)
        self.layout_vertical_ssp.addWidget(self.drop_down_spp)
        self.group_box_ssp.setLayout(self.layout_vertical_ssp)
        self.layout_main_vertical.addWidget(self.group_box_ssp)

        self.layout_vertical_output = QVBoxLayout()
        self.layout_vertical_output.addWidget(self.label_xy)
        self.layout_vertical_output.addWidget(self.label_xy_2)
        self.layout_horizontal_bottom.addWidget(self.button_continuous)
        self.layout_horizontal_bottom.addWidget(self.button_single)
        self.layout_horizontal_bottom.addWidget(self.button_toggle_sin_square)
        self.layout_horizontal_bottom.addWidget(self.button_draw_data)
        self.layout_horizontal_bottom.addWidget(self.button_automatic_measurement)
        self.layout_horizontal_bottom.addWidget(self.button_save_as)
        self.layout_horizontal_bottom.addWidget(self.button_send_command)
        self.layout_vertical_output.addLayout(self.layout_horizontal_bottom)
        self.group_box_out.setLayout(self.layout_vertical_output)
        self.layout_main_vertical.addWidget(self.group_box_out)
        self.layout_main_vertical.addWidget(self.edit27)
        self.setLayout(self.layout_main_vertical)
        self.on_edit_change_frequency_left()
        self.on_edit_change_amplitude_left()
        self.on_edit_change_offset_left()
        self.e20()
        self.e25()
        self.e26()
        self.plainText = QPlainTextEdit(self)
        self.plainText.setReadOnly(True)
        self.layout_main_vertical.addWidget(self.plainText)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.automatic_update_check()


app = QApplication([])
window = MainWindow()
window.show()
window.timer.start(100)
sys.exit(app.exec_())
