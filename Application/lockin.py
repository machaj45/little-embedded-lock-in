#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider, QFileDialog, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import math
from SerialThread import SerialThread
from Worker import Worker
from Reader import Reader
import pyqtgraph as pg
import statistics
import csv
import time
import numpy as np
import os
import urllib.request
from bs4 import BeautifulSoup
import re


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class Form(QDialog):

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
            self.plainText.insertPlainText('Unable to check version!' + '\n')
            return
        if self.gui_version == online_versions[0]:
            self.plainText.insertPlainText('Application is update!\t version: ' + self.gui_version + '\n')
        else:
            self.plainText.insertPlainText('Application needs to be updated!' + '\n')
            self.plainText.insertPlainText('Please download newer version from:\n' +
                                           'https://github.com/machaj45/little-embedded-lock-in/releases' + '\n')

    def show_new_window(self):
        self.w.show()

    def closeEvent(self, event):
        self.serial_thread.running = False
        self.w.close()
        if self.serial_thread is not None and self.serial_thread.serial is not None:
            self.serial_thread.serial.close()
        self.reader.stop = True
        print('Window closed')

    def e10(self):
        if self.edit10.text() != "":
            a = float(self.edit10.text())
            if 0 < a <= 130000:
                self.qs_slider10.setValue(float(self.edit10.text()))
                self.sf = int(self.sample_per_period * a)
                st = self.select_st_for_sf()
                self.label_spp.setText(
                    "Samples per period = {0} [-], Sampling frequency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(
                        int(self.sample_per_period), self.sf, st))
            else:
                self.edit10.setText("1")

    def e15(self):
        if self.edit15.text() != "":
            a = int(self.edit15.text())
            if 0 < a <= 100:
                self.qs_slider15.setValue(int(self.edit15.text()))
            else:
                self.edit15.setText("1")

    def e16(self):
        if self.edit16.text() != "":
            a = int(self.edit16.text())
            if 0 < a <= 3300:
                self.qs_slider16.setValue(int(self.edit16.text()))
            else:
                self.edit16.setText("1")

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

    def slider_update_10(self, value):
        self.edit10.setText(str(value))
        pass

    def slider_update_15(self, value):
        self.edit15.setText(str(value))
        pass

    def slider_update_16(self, value):
        self.edit16.setText(str(value))
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
        self.serial_thread.running = False
        pass

    def connect(self):
        self.reader.in_scan_mode = True
        available_ports = self.serial_thread.available_ports
        self.running = False
        self.serial_thread.running = False
        time.sleep(0.4)
        self.serial_thread = SerialThread(115200, self, available_ports[self.selected_comport])
        self.running = True
        self.serial_thread.start()
        self.reader.serial_thread = self.serial_thread
        self.reader.in_scan_mode = False
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
        st = self.select_st_for_sf()
        self.label_spp.setText(
            "Samples per period = {0} [-], Sampling frequency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(
                int(ssp), self.sf, st))

    def send_command(self):
        self.button13.setEnabled(True)
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
            self.gui.plainText.insertPlainText('FileNotFoundError load, load returning true' + '\n')
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
            self.gui.plainText.insertPlainText('File Not Found Please select valid file' + '\n')

    def open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Frequency list in .csv format!", "",
                                                   "Table Files (*.csv)", options=options)
        if file_name:
            self.loadFileName = file_name
            # print(fileName)
        pass

    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save as", "", "Table Files (*.csv)", options=options)
        if file_name:
            self.saveFileName = file_name
        # print(file_name)
        pass

    def update_plot(self):
        self.graphWidget.plot(range(0, len(self.acquired_data_YY)), self.acquired_data_YY,
                              pen=pg.mkPen(color=(255, 0, 0)),
                              name='dut')
        self.graphWidget.plot(range(0, len(self.acquired_data_XX)), self.acquired_data_XX,
                              pen=pg.mkPen(color=(0, 255, 0)),
                              name='ref')
        self.graphWidget.plot(range(0, len(self.acquired_data_ZZ)), self.acquired_data_ZZ,
                              pen=pg.mkPen(color=(0, 100, 255)),
                              name='ref90')

    def toggle(self):
        if not self.sin_square_mode:
            self.button_toggle_sin_square.setText("Toggle to Sin")
            self.sin_square_mode = True
        else:
            self.button_toggle_sin_square.setText("Toggle to Square")
            self.sin_square_mode = False
        self.serial_thread.ser_out("SINS\n")
        time.sleep(0.1)
        self.set_everything0()

    def do_calculation(self):
        if self.sin_square_mode:
            self.square_calculation()
        else:
            self.dual_phase_decomposition()

    def square_calculation(self):
        self.text_to_update_2 = 'Sending data'
        a = 0
        while len(self.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            self.text_to_update = 'no data ' + str(a)
        self.label24.setText('LENGTH ' + str(len(self.acquired_data_Y)))

        my = statistics.mean(self.acquired_data_Y)
        mx = 0

        self.acquired_data_XX = []
        self.acquired_data_YY = []

        for i in range(0, len(self.acquired_data_Y)):
            self.acquired_data_YY.append(self.acquired_data_Y[i] - my)
        for i in range(0, len(self.acquired_data_X)):
            self.acquired_data_XX.append(self.acquired_data_X[i] - mx)

        del self.acquired_data_XX[0:int(self.sample_per_period / 4)]
        del self.acquired_data_YY[0:int(self.sample_per_period / 4)]
        del self.acquired_data_XX[len(self.acquired_data_XX) - self.sample_per_period:-1]
        del self.acquired_data_YY[len(self.acquired_data_YY) - self.sample_per_period:-1]

        self.ref = [r * (3.30 / 4095.0) for r in self.acquired_data_XX]
        self.dut = [d * (3.30 / 4095.0) for d in self.acquired_data_YY]

        del self.ref[-1]
        ref_length = len(self.ref)
        self.time_sample = ref_length / self.sf
        mx = statistics.mean(self.ref)
        a = 0
        for i in self.ref:
            if i > mx:
                self.ref[a] = 1
            if i < mx:
                self.ref[a] = -1
            a = a + 1

            # vaclav.grim@fel.cvut.cz

        self.X = []
        self.Y = []
        for i in range(0, len(self.dut)):
            self.X.append(self.dut[i] * self.ref[i])
        string3 = ""
        string1 = ""
        string = ""
        std_x = 0
        if len(self.X) > 0:
            mean_x = statistics.mean(self.X)
            std_x = statistics.stdev(self.X)
            dist = int(abs(math.log10(abs(std_x)))) + 4
            dist2 = int(abs(math.log10(abs(mean_x)))) + 4
            dist3 = int(abs(math.log10(abs(mean_x / std_x))))
            dist = max(dist, dist2)
            string = "{:." + str(dist) + "f}"
            string1 = "{:." + str(dist3) + "f}"
            dist4 = int(abs(math.log10(abs(self.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"

        else:
            mean_x = 1
        self.acquired_data = []
        self.acquired_data_X = []
        self.acquired_data_Y = []
        string_for_time_sample = string3.format(self.time_sample)
        try:
            self.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(
                mean_x) + " V," + " sigma =" + " " + string.format(
                std_x) + " V, " + "U\N{SUBSCRIPT TWO}/sigma= " + string1.format(
                20 * math.log10(mean_x / std_x)) + " dB\n" + "Time duration = {0} s".format(string_for_time_sample)
        except ValueError:
            self.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(
                mean_x) + " V," + " sigma =" + " " + string.format(
                std_x) + " V \n" + "Time duration = {0} s".format(string_for_time_sample)
        self.Gain.append(string.format(mean_x))
        # self.Phase.append(string_for_time_sample)
        self.reader.calculated = True

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

    def dual_phase_decomposition(self, strings=None, string_for_xy=None):
        self.text_to_update_2 = 'Sending data'
        a = 0
        while len(self.acquired_data_Y) == 0:
            time.sleep(0.2)
            a = a + 1
            self.text_to_update = 'no data ' + str(a)
        self.label24.setText('LENGTH ' + str(len(self.acquired_data_Y)))
        for i in range(0, len(self.acquired_data_Y)):
            if abs(self.acquired_data_Y[i]) >= 4096:
                self.acquired_data_Y[i] = 0
        for i in range(0, len(self.acquired_data_X)):
            if abs(self.acquired_data_X[i]) >= 4096:
                self.acquired_data_X[i] = 0
        my = statistics.mean(self.acquired_data_Y)
        mx = statistics.mean(self.acquired_data_X)

        self.acquired_data_XX = []
        self.acquired_data_YY = []
        self.acquired_data_ZZ = []

        for i in range(0, len(self.acquired_data_Y)):
            self.acquired_data_YY.append(self.acquired_data_Y[i] - my)
        for i in range(0, len(self.acquired_data_X)):
            self.acquired_data_XX.append(self.acquired_data_X[i] - mx)
            self.acquired_data_ZZ.append(self.acquired_data_X[i] - mx)
        for i in range(0, int(self.sample_per_period / 4)):
            self.acquired_data_ZZ.insert(0, 0)

        # remove start for angle accuracy

        del self.acquired_data_XX[0:int(self.sample_per_period / 4)]
        del self.acquired_data_YY[0:int(self.sample_per_period / 4)]
        del self.acquired_data_ZZ[0:int(self.sample_per_period / 4)]
        del self.acquired_data_XX[len(self.acquired_data_XX) - self.sample_per_period:-1]
        del self.acquired_data_YY[len(self.acquired_data_YY) - self.sample_per_period:-1]
        del self.acquired_data_ZZ[
            len(self.acquired_data_ZZ) - int(self.sample_per_period + self.sample_per_period / 4):-1]

        self.dut = [d * (3.30 / 4095) for d in self.acquired_data_YY]
        self.ref = [r * (3.30 / 4095) for r in self.acquired_data_XX]
        self.ref90 = [rd * (3.30 / 4095) for rd in self.acquired_data_ZZ]

        aa = self.crossings_nonzero_pos2neg(self.ref)
        if len(aa) < 2 * int(len(self.ref) / self.sample_per_period):
            ba = self.crossings_nonzero_neg2pos(self.ref)
            min_removed_end = min(aa[0], ba[0])
            del self.ref[0:min_removed_end]
            del self.ref90[0:min_removed_end]
            del self.dut[0:min_removed_end]

            a = self.crossings_nonzero_pos2neg(self.ref)
            b = self.crossings_nonzero_neg2pos(self.ref)

            length_of_calculation = 0
            if len(self.dut) > len(self.ref):
                length_of_calculation = len(self.ref)
            if len(self.dut) < len(self.ref):
                length_of_calculation = len(self.dut)
            length_of_ref = length_of_calculation
            if aa[0] == min_removed_end:
                length_of_ref = a[-1]
            if ba[0] == min_removed_end:
                length_of_ref = b[-1]

            del self.ref[length_of_ref:-1]
            del self.ref90[length_of_ref:-1]
            del self.dut[length_of_ref:-1]

        self.ref_norm = [r ** 2 for r in self.ref]
        mrs_norm_ref = math.sqrt(statistics.mean(self.ref_norm))
        self.ref_norm = [r / mrs_norm_ref for r in self.ref]

        self.ref90n = [r ** 2 for r in self.ref90]
        mrs_norm_ref_90 = math.sqrt(statistics.mean(self.ref90n))
        self.ref90n = [r / mrs_norm_ref_90 for r in self.ref90]

        del self.ref[-1]
        del self.ref90[-1]
        ref_length = len(self.ref)
        self.time_sample = ref_length / self.sf

        self.X = []
        self.Y = []
        self.Xn = []
        self.Yn = []
        length_of_calculation = 0
        if len(self.dut) >= len(self.ref):
            length_of_calculation = len(self.ref)
        if len(self.dut) <= len(self.ref):
            length_of_calculation = len(self.dut)
        for i in range(0, length_of_calculation):
            self.X.append(self.dut[i] * self.ref[i])
            self.Xn.append(self.dut[i] * self.ref_norm[i])
        for i in range(0, length_of_calculation):
            self.Y.append(self.dut[i] * self.ref90[i])
            self.Yn.append(self.dut[i] * self.ref90n[i])
        mean_x_norm = 0
        mean_y_norm = 0
        if len(self.X) > 0:
            mean_x = statistics.mean(self.X)
            mean_y = statistics.mean(self.Y)
            mean_x_norm = statistics.mean(self.Xn)
            mean_y_norm = statistics.mean(self.Yn)
        else:
            mean_x, mean_y = 1, 0

        self.acquired_data = []
        self.acquired_data_X = []
        self.acquired_data_Y = []
        sa = -(180 * (math.atan2(mean_y, mean_x) / math.pi))
        dist = math.sqrt(mean_x ** 2 + mean_y ** 2)
        dist_norm = math.sqrt(mean_x_norm ** 2 + mean_y_norm ** 2)
        input_gain = 1
        if dist > 0:
            if len(self.ref) > 0:
                input_gain = math.sqrt(statistics.mean([r ** 2 for r in self.ref]))
            else:
                input_gain = 1
            sb = 20 * math.log10((dist_norm / input_gain))
            dists = int(abs(math.log10(abs(dist_norm)))) + 4
            string = "{:." + str(dists) + "f}"
            sas = int(abs(math.log10(abs(sa)))) + 4
            strings = "{:." + str(sas) + "f}"
            sbs = int(abs(math.log10(abs(sb)))) + 4
            string_bs = "{:." + str(sbs) + "f}"
            sxs = int(abs(math.log10(abs(mean_x)))) + 4
            string_for_xy = "{:." + str(sxs) + "f}"
            dist4 = int(abs(math.log10(abs(self.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"
            time_duration_string = string3.format(self.time_sample)
            self.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = " + string_bs.format(
                sb) + " dB,\nX: " + string_for_xy.format(mean_x) + " Y: " + string_for_xy.format(
                mean_y) + " U\N{SUBSCRIPT TWO} = " + string.format(
                dist) + " V" + " U\N{SUBSCRIPT TWO} / U\N{SUBSCRIPT ONE} = " + string.format(
                (dist_norm / input_gain)) + " " + "\nTime duration = {0} s".format(time_duration_string)
        else:
            self.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = -Inf " + \
                                  " dB X: " + string_for_xy.format(mean_x) + " Y: " + string_for_xy.format(mean_y)
        self.Gain.append(20 * math.log10(dist / input_gain))
        self.Phase.append(sa)
        self.reader.calculated = True

    def plot_data(self):
        self.graphWidget.clear()
        self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.dut))], self.dut,
                              pen=pg.mkPen(color=(255, 0, 0)), name='dut')
        self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.ref))], self.ref,
                              pen=pg.mkPen(color=(0, 255, 0)), name='ref')
        if self.sin_square_mode:
            self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.X))], self.X,
                                  pen=pg.mkPen(color=(0, 100, 255), style=Qt.DotLine), name='U2')
        if not self.sin_square_mode:
            self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.ref90))], self.ref90,
                                  pen=pg.mkPen(color=(0, 100, 255)), name='ref90')
        self.graphWidget.addLegend()
        self.graphWidget.setMouseEnabled(x=True, y=True)

    def start_stop_measurement(self):
        self.graphWidget.clear()
        if self.worker is None:
            self.worker = Worker(self, self.serial_thread)
        self.button_automatic_measurement.setText("Stop Measurement")
        if self.worker.running:
            self.button_automatic_measurement.setText("Automatic Measurement")
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
        self.serial_thread.ser_out(self.edit10.text() + "\n")

    def save(self):
        if not self.sin_square_mode:
            row_list = [["f [Hz]", "gain [dB]", "phase [°]"]]
        else:
            row_list = [["f [Hz]", "U2 [V]", "Ts [us]"]]
        for i in range(0, len(self.Gain)):
            one_row_list = [self.Freq[i], self.Gain[i], self.Phase[i]]
            row_list.append(one_row_list)
        with open(self.saveFileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)
        pass

    def read(self):
        if self.reader.con_flag_stop:
            return
        if not self.reader.con_flag:
            self.reader.con_flag = True
        else:
            self.reader.con_flag_stop = True

    def measure(self):
        self.reader.single_flag = True

    def start0(self):
        self.serial_thread.ser_out("START\n")
        self.serial_thread.ser_out("0\n")

    def start1(self):
        self.serial_thread.ser_out("START\n")
        self.serial_thread.ser_out("1\n")

    def stop0(self):
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

    def set_everything0(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.data_bin = False
        self.serial_thread.send_all_counter = 0
        self.serial_thread.b = 0
        self.serial_thread.data = []
        self.text = []
        self.button13.setEnabled(False)
        self.serial_thread.ser_out("AMPL\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit15.text() + "\n")
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("0\n")
        a = (int(self.edit16.text()) / 3300) * (2 ** 12)
        if a >= 4095:
            a = 4095
        if a <= 0:
            a = 5000
        self.serial_thread.ser_out(str(int(a)) + "\n")
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit10.text() + "\n")

    def set_everything1(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.text = []
        self.serial_thread.send_all_counter = 0
        self.button23.setEnabled(False)
        self.serial_thread.ser_out("AMPL\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out(self.edit25.text() + "\n")
        self.serial_thread.ser_out("OFFS\n")
        self.serial_thread.ser_out("1\n")
        a = (int(self.edit26.text()) / 3300) * (2 ** 12)
        if a <= 0:
            a = 1
        if a >= 4095:
            a = 4095
        self.serial_thread.ser_out(str(int(a)) + "\n")
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out(self.edit20.text() + "\n")

    def update_text(self):
        try:
            self.label_xy.setText(self.text_to_update)
            self.label_xy_2.setText(self.text_to_update_2)
            if self.plainText.verticalScrollBar().maximum() != self.last_vertical_maximum:
                self.plainText.verticalScrollBar().setValue(self.plainText.verticalScrollBar().maximum() - 1)
                self.last_vertical_maximum = self.plainText.verticalScrollBar().maximum()
            if self.last_text != self.text_to_update_3 and self.plainText is not None:
                if self.text_to_update_3 != "":
                    self.plainText.insertPlainText(self.text_to_update_3 + '\n')
                self.last_text = self.text_to_update_3
        except RuntimeError:
            self.gui.plainText.insertPlainText('RuntimeError in update_text' + '\n')
            pass

    def __init__(self, parent=None):
        self.w = AnotherWindow()
        self.selected_comport = 0
        self.serial_thread = SerialThread(115200, self, None)  # Start serial thread
        self.serial_thread.start()
        # Start worker thread
        self.reader = Reader(self, self.serial_thread)  # Start reading thread
        self.reader.start()
        super(Form, self).__init__(parent)
        font = self.font()
        font.setPointSize(10)
        self.worker = None
        self.sf = 10
        self.window().setFont(font)
        self.counter_of_drawing = 0

        datafile = "data/icon.ico"
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
            print(datafile)
            print(" not frozen")
        else:
            datafile = "icon.ico/icon.ico"
            datafile = os.path.join(sys.prefix, datafile)
            print(datafile)
            print("frozen")

        self.setWindowIcon(QtGui.QIcon(datafile))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.gui_version = 'v1.0.1'
        self.fir_version = 1
        self.loadFileName = 'frec.csv'
        self.saveFileName = 'data.csv'
        self.worker = None
        self.sf = 10
        self.backup1 = []
        self.backup2 = []
        self.acquired_data_YY = []
        self.plot = False
        self.frequency_gen_1 = 100
        self.acquired_data_XX = []
        self.time_sample = 1
        self.acquired_data_ZZ = []
        self.data_probe = 0
        self.backup3 = []
        self.text_to_update = "Start empty"
        self.text_to_update_2 = "Start empty"
        self.text_to_update_3 = ""
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
        self.last_text = ''
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

        self.edit2 = QLineEdit("Write commands here..")
        self.button1 = QPushButton("SET")
        self.button2 = QPushButton("SET")
        self.layout_horizontal_gen = QHBoxLayout()
        self.layout_main_vertical = QVBoxLayout()
        self.layout_vertical_left_gen = QVBoxLayout()
        self.layout_vertical_right_gen = QVBoxLayout()
        self.layout_horizontal_bottom = QHBoxLayout()
        self.layout_horizontal_left_gen = QHBoxLayout()
        self.layout_horizontal_right_gen = QHBoxLayout()
        self.layout_horizontal_connect = QHBoxLayout()
        self.setWindowTitle("Little Embedded Lock-in")
        self.label10 = QLabel("Channel 1 - A2")
        self.label15 = QLabel("Amplitude")
        self.edit15 = QLineEdit("85")
        self.edit15.textChanged.connect(self.e15)
        self.label16 = QLabel("Offset")
        self.edit16 = QLineEdit("250")
        self.edit16.textChanged.connect(self.e16)
        self.label11 = QLabel("Frequency")
        self.edit10 = QLineEdit("100")
        self.edit10.textChanged.connect(self.e10)
        self.label12 = QLabel("Step")
        self.edit12 = QLineEdit("1")
        self.label13 = QLabel("F Start")
        self.edit13 = QLineEdit("100")
        self.label14 = QLabel("F Stop")
        self.edit14 = QLineEdit("1000")
        self.button10 = QPushButton("Start")
        self.button11 = QPushButton("Stop")
        self.button12 = QPushButton("Sweep")
        self.button13 = QPushButton("Set up Generator 1")
        self.qs_slider10 = QSlider(Qt.Horizontal, self)
        self.qs_slider10.setRange(0, 130000)
        self.qs_slider10.setFocusPolicy(Qt.NoFocus)
        self.qs_slider10.setPageStep(1)
        self.qs_slider10.valueChanged.connect(self.slider_update_10)
        self.qs_slider16 = QSlider(Qt.Horizontal, self)
        self.qs_slider16.setRange(0, 3300)
        self.qs_slider16.setFocusPolicy(Qt.NoFocus)
        self.qs_slider16.setPageStep(1)
        self.qs_slider16.valueChanged.connect(self.slider_update_16)
        self.qs_slider15 = QSlider(Qt.Horizontal, self)
        self.qs_slider15.setRange(0, 100)
        self.qs_slider15.setFocusPolicy(Qt.NoFocus)
        self.qs_slider15.setPageStep(1)
        self.qs_slider15.valueChanged.connect(self.slider_update_15)
        self.layout_vertical_left_gen.addWidget(self.label10)
        self.layout_vertical_left_gen.addWidget(self.label15)
        self.layout_vertical_left_gen.addWidget(self.edit15)
        self.layout_vertical_left_gen.addWidget(self.qs_slider15)
        self.layout_vertical_left_gen.addWidget(self.label16)
        self.layout_vertical_left_gen.addWidget(self.edit16)
        self.layout_vertical_left_gen.addWidget(self.qs_slider16)
        self.layout_vertical_left_gen.addWidget(self.label11)
        self.layout_vertical_left_gen.addWidget(self.edit10)
        self.layout_vertical_left_gen.addWidget(self.qs_slider10)
        self.layout_horizontal_left_gen.addWidget(self.button13)
        self.layout_horizontal_left_gen.addWidget(self.button10)
        self.layout_horizontal_left_gen.addWidget(self.button11)
        self.layout_vertical_left_gen.addLayout(self.layout_horizontal_left_gen)
        self.button10.clicked.connect(self.start0)
        self.button11.clicked.connect(self.stop0)
        self.button12.clicked.connect(self.sweep0)
        self.button13.clicked.connect(self.set_everything0)
        self.label20 = QLabel("Channel 2 - D13")
        self.label25 = QLabel("Amplitude")
        self.edit25 = QLineEdit("50")
        self.edit25.textChanged.connect(self.e25)
        self.label26 = QLabel("Offset")
        self.edit26 = QLineEdit("400")
        self.edit26.textChanged.connect(self.e26)
        self.label21 = QLabel("Frequency")
        self.edit20 = QLineEdit("10")
        self.edit20.textChanged.connect(self.e20)
        self.label22 = QLabel("Step")
        self.edit22 = QLineEdit("1")
        self.label23 = QLabel("F Start")
        self.edit23 = QLineEdit("10")
        self.label24 = QLabel("F Stop")
        self.edit24 = QLineEdit("1000")
        self.edit27 = QLineEdit("TEXT")
        self.button20 = QPushButton("Start")
        self.button21 = QPushButton("Stop")
        self.button22 = QPushButton("Sweep")
        self.button23 = QPushButton("Set up Generator 2")
        self.qs_slider20 = QSlider(Qt.Horizontal, self)
        self.qs_slider20.setRange(0, 130000)
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
        self.layout_vertical_right_gen.addWidget(self.label20)
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

        self.layout_main_vertical.addWidget(self.drop_down_comports)
        self.drop_down_comports.currentIndexChanged.connect(self.comports)
        self.layout_horizontal_connect.addWidget(self.button_scan)
        self.layout_horizontal_connect.addWidget(self.button_connect)
        self.layout_horizontal_connect.addWidget(self.button_help)
        self.layout_main_vertical.addLayout(self.layout_horizontal_connect)
        self.layout_horizontal_gen.addLayout(self.layout_vertical_left_gen)
        self.layout_horizontal_gen.addLayout(self.layout_vertical_right_gen)
        self.layout_main_vertical.addLayout(self.layout_horizontal_gen)
        self.label_spp = QLabel("Samples per period")
        self.button_spp = QPushButton("Set Samples per period")
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.hist = pg.HistogramLUTItem()
        self.button_load = QPushButton("Load")
        self.button_toggle_sin_square = QPushButton("Toggle to Square")
        self.button_draw_data = QPushButton("Draw data")
        self.button_load.setEnabled(True)
        self.button_toggle_sin_square.setEnabled(True)
        self.button_automatic_measurement = QPushButton("Automatic Measurement")
        self.button_save_as = QPushButton("Save As")
        self.button_send_command = QPushButton("Send command")
        self.button_continuous = QPushButton("Continuous")
        self.button_single = QPushButton("Single")
        self.button_continuous.clicked.connect(self.read)
        self.button_single.clicked.connect(self.measure)
        self.button_load.clicked.connect(self.load_button)
        self.button_toggle_sin_square.clicked.connect(self.toggle)
        self.button_draw_data.clicked.connect(self.plot_data)
        self.button_automatic_measurement.clicked.connect(self.start_stop_measurement)
        self.button_save_as.clicked.connect(self.save_file_dialog)
        self.button_send_command.clicked.connect(self.send_command)
        self.drop_down_spp = QComboBox()

        for i in range(3, 11):
            self.drop_down_spp.addItem(str(2 ** i))
        self.drop_down_spp.currentIndexChanged.connect(self.spp)
        self.layout_main_vertical.addWidget(self.label_spp)
        self.layout_main_vertical.addWidget(self.drop_down_spp)
        self.layout_main_vertical.addWidget(self.label_xy)
        self.layout_main_vertical.addWidget(self.label_xy_2)
        self.layout_main_vertical.addWidget(self.graphWidget)
        self.layout_horizontal_bottom.addWidget(self.button_continuous)
        self.layout_horizontal_bottom.addWidget(self.button_single)
        self.layout_horizontal_bottom.addWidget(self.button_toggle_sin_square)
        self.layout_horizontal_bottom.addWidget(self.button_draw_data)
        self.layout_horizontal_bottom.addWidget(self.button_automatic_measurement)
        self.layout_horizontal_bottom.addWidget(self.button_save_as)
        self.layout_horizontal_bottom.addWidget(self.button_send_command)
        self.layout_main_vertical.addLayout(self.layout_horizontal_bottom)
        self.layout_main_vertical.addWidget(self.edit27)
        self.setLayout(self.layout_main_vertical)
        self.e10()
        self.e15()
        self.e16()
        self.e20()
        self.e25()
        self.e26()
        self.plainText = QPlainTextEdit(self)
        self.layout_main_vertical.addWidget(self.plainText)
        self.automatic_update_check()


app = QApplication([])
window = Form()
window.show()
sys.exit(app.exec_())
