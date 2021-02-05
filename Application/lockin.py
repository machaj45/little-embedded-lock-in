#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSlider, QFileDialog
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


class Form(QDialog):
    def closeEvent(self, event):
        self.serial_thread.running = False
        self.serial_thread.serial.close()
        self.reader.stop = True
        print('Window closed')

    def make_gui(self):
        pass

    def e10(self):
        if self.edit10.text() != "":
            a = int(self.edit10.text())
            if 0 < a <= 130000:
                self.qs_slider10.setValue(int(self.edit10.text()))
                self.sf = int(self.sample_per_period * a)
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

    def qslider10update(self, value):
        self.edit10.setText(str(value))
        pass

    def qslider15update(self, value):
        self.edit15.setText(str(value))
        pass

    def qslider16update(self, value):
        self.edit16.setText(str(value))
        pass

    def qslider20update(self, value):
        self.edit20.setText(str(value))
        pass

    def qslider25update(self, value):
        self.edit25.setText(str(value))
        pass

    def qslider26update(self, value):
        self.edit26.setText(str(value))
        pass

    def scan(self):
        self.serial_thread.scan()
        pass

    def connect(self):
        self.serial_thread.scan()
        self.serial_thread = SerialThread(115200, self)
        self.serial_thread.comport = self.edit_connect.text()
        self.text_to_update_3 = "Connecting to " + self.serial_thread.comport
        self.running = True
        self.serial_thread.start()
        self.reader.serial_thread = self.serial_thread
        pass

    def spp(self, i):
        i = i + 3
        self.serial_thread.ser_out("SAMP\n")
        self.serial_thread.ser_out(str(2 ** i) + "\n")
        self.sample_per_period = 2 ** i
        self.acquired_data_X = []
        self.acquired_data_Y = []
        ssp = float(2 ** i)
        self.sf = int(ssp * self.frek1)
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
        self.label_spp.setText(
            "Samples per period = {0} [-], Sampling frequency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(
                int(ssp), self.sf, st))

    def reset(self):
        self.button13.setEnabled(True)
        self.acquired_data_Y = []
        self.acquired_data_X = []
        self.acquired_data_XX = []
        self.acquired_data_YY = []
        self.acquired_data_ZZ = []
        self.serial_thread.ser_out(self.edit27.text() + "\n")

    def load(self) -> bool:
        try:
            with open(self.loadFileName) as file:
                self.Freq = []
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    self.Freq.append(float(row[0]))
        except FileNotFoundError:
            self.text_to_update = "File Not Found Please select valid file"
            return True
        return False

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Frequency list in .csv format!", "",
                                                  "Table Files (*.csv)", options=options)
        if fileName:
            self.loadFileName = fileName
            # print(fileName)
        pass

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save as", "", "Table Files (*.csv)", options=options)
        if fileName:
            self.saveFileName = fileName
        # print(fileName)
        pass

    def draw2(self):
        self.serial_thread.ser_out("FILT\n")
        self.serial_thread.ser_out(self.editfil.text() + "\n")

        """
        self.graphWidget.clear()
        my = statistics.mean(self.aquaredDataY)
        mx = statistics.mean(self.aquaredDataX)
        self.aquaredDataZ=[]
        for i in range(0,len(self.aquaredDataY)):
            self.aquaredDataY[i]=self.aquaredDataY[i]-my
        for i in range(0,len(self.aquaredDataX)):
            self.aquaredDataX[i]=self.aquaredDataX[i]-mx
            self.aquaredDataZ.append(self.aquaredDataX[i])
        for i in range(0,int(self.sample_per_periode/4)):
            self.aquaredDataZ.insert(0, 0)
        self.graphWidget.plot(range(0,len(self.aquaredDataY)), self.aquaredDataY,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
        self.graphWidget.plot(range(0,len(self.aquaredDataX)),self.aquaredDataX,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
        self.graphWidget.plot(range(0,len(self.aquaredDataZ)),self.aquaredDataZ,pen=pg.mkPen(color=(0, 0, 255)),name='ref90')
        self.dut = self.aquaredDataY
        self.ref = self.aquaredDataX
        self.ref90 = self.aquaredDataZ
        self.graphWidget.addLegend()
        """

    def update_plot(self, data):
        self.graphWidget.plot(range(0, len(self.acquired_data_YY)), self.acquired_data_YY, pen=pg.mkPen(color=(255, 0, 0)),
                              name='dut')
        self.graphWidget.plot(range(0, len(self.acquired_data_XX)), self.acquired_data_XX, pen=pg.mkPen(color=(0, 255, 0)),
                              name='ref')
        self.graphWidget.plot(range(0, len(self.acquired_data_ZZ)), self.acquired_data_ZZ, pen=pg.mkPen(color=(0, 100, 255)),
                              name='ref90')

    def toggle(self):
        if self.sin_square_mode == False:
            self.button_toggle_sin_square.setText("Toggle to Sin")
            # self.buttongraph7.setEnabled(False)
            self.sin_square_mode = True
        else:
            self.button_toggle_sin_square.setText("Toggle to Sqare")
            self.sin_square_mode = False
            # self.buttongraph7.setEnabled(True)
        self.serial_thread.ser_out("SINS\n")
        time.sleep(0.1)
        self.setEverithing0()

    def draw33(self, plot):
        if self.sin_square_mode:
            self.squareCalk(plot)
        else:
            self.sinCalk(plot)

    def squareCalk(self, plot):
        self.text_to_update_2 = 'Sending data'
        if plot:
            self.graphWidget.clear()
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

        if plot:
            self.graphWidget.plot(range(0, len(self.dut)), self.dut, pen=pg.mkPen(color=(255, 0, 0)), name='dut')
            self.graphWidget.plot(range(0, len(self.ref)), self.ref, pen=pg.mkPen(color=(0, 255, 0)), name='ref')
            # vaclav.grim@fel.cvut.cz

        if plot:
            self.graphWidget.addLegend()
        self.X = []
        self.Y = []
        for i in range(0, len(self.dut)):
            self.X.append(self.dut[i] * self.ref[i])
        if len(self.X) > 0:
            mX = statistics.mean(self.X)
            stdX = statistics.stdev(self.X)
            dist = int(abs(math.log10(abs(stdX)))) + 4
            dist2 = int(abs(math.log10(abs(mX)))) + 4
            dist3 = int(abs(math.log10(abs(mX / stdX))))
            dist = max(dist, dist2)
            string = "{:." + str(dist) + "f}"
            string1 = "{:." + str(dist3) + "f}"
            dist4 = int(abs(math.log10(abs(self.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"

        else:
            mX = 1
        self.acquired_data = []
        self.acquired_data_X = []
        self.acquired_data_Y = []
        ssttrr = string3.format(self.time_sample)
        try:
            self.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(mX) + " V," + " sigma =" + " " + string.format(
                stdX) + " V, " + "U\N{SUBSCRIPT TWO}/sigma= " + string1.format(
                20 * math.log10(mX / stdX)) + " dB\n" + "Time duration = {0} s".format(ssttrr)
        except ValueError:
            self.text_to_update = "U\N{SUBSCRIPT TWO} = " + string.format(mX) + " V," + " sigma =" + " " + string.format(
                stdX) + " V \n" + "Time duration = {0} s".format(ssttrr)
        self.Gain.append(string.format(mX))
        # self.Phase.append(ssttrr)
        self.reader.calculated = True

    def crossings_nonzero_pos2neg(self, data):
        data = np.array(data)
        pos = data > 0
        return (pos[:-1] & ~pos[1:]).nonzero()[0]

    def crossings_nonzero_neg2pos(self, data):
        data = np.array(data)
        pos = data > 0
        return (pos[1:] & ~pos[:-1]).nonzero()[0]

    def crossings_nonzero_f(self, data):
        data = np.array(data)
        pos = data > 0
        npos = ~pos
        return ((pos[:-1] & npos[1:]) | (npos[:-1] & pos[1:])).nonzero()[0][0]

    def crossings_nonzero_l(self, data):
        data = np.array(data)
        pos = data > 0
        npos = ~pos
        return ((pos[:-1] & npos[1:]) | (npos[:-1] & pos[1:])).nonzero()[0][-1]

    def sinCalk(self, plot, strings=None, stringxs=None):
        self.text_to_update_2 = 'Sending data'
        if plot:
            self.graphWidget.clear()
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

        # remove start for angle accuacy

        del self.acquired_data_XX[0:int(self.sample_per_period / 4)]
        del self.acquired_data_YY[0:int(self.sample_per_period / 4)]
        del self.acquired_data_ZZ[0:int(self.sample_per_period / 4)]
        del self.acquired_data_XX[len(self.acquired_data_XX) - self.sample_per_period:-1]
        del self.acquired_data_YY[len(self.acquired_data_YY) - self.sample_per_period:-1]
        del self.acquired_data_ZZ[len(self.acquired_data_ZZ) - int(self.sample_per_period + self.sample_per_period / 4):-1]

        self.dut = [d * (3.30 / 4095) for d in self.acquired_data_YY]
        self.ref = [r * (3.30 / 4095) for r in self.acquired_data_XX]
        self.ref90 = [rd * (3.30 / 4095) for rd in self.acquired_data_ZZ]

        aa = self.crossings_nonzero_pos2neg(self.ref)
        if len(aa) < 2 * int(len(self.ref) / self.sample_per_period):
            ba = self.crossings_nonzero_neg2pos(self.ref)
            sref = min(aa[0], ba[0])
            del self.ref[0:sref]
            del self.ref90[0:sref]
            del self.dut[0:sref]

            a = self.crossings_nonzero_pos2neg(self.ref)
            b = self.crossings_nonzero_neg2pos(self.ref)

            gofor = 0
            if len(self.dut) > len(self.ref):
                gofor = len(self.ref)
            if len(self.dut) < len(self.ref):
                gofor = len(self.dut)
            lref = gofor
            if aa[0] == sref:
                lref = a[-1]
            if ba[0] == sref:
                lref = b[-1]

            del self.ref[lref:-1]
            del self.ref90[lref:-1]
            del self.dut[lref:-1]

        self.ref_norm = [r ** 2 for r in self.ref]
        mnr = math.sqrt(statistics.mean(self.ref_norm))
        # self.texttoupdate3 = str (mnr)
        Ar = mnr
        self.ref_norm = [r / Ar for r in self.ref]

        self.ref90n = [r ** 2 for r in self.ref90]
        mnr90 = math.sqrt(statistics.mean(self.ref90n))
        # self.texttoupdate3 = str (mnr)
        Ar90 = mnr90
        self.ref90n = [r / Ar90 for r in self.ref90]

        del self.ref[-1]
        del self.ref90[-1]
        ref_length = len(self.ref)
        self.time_sample = ref_length / self.sf

        if plot:
            self.graphWidget.plot(range(0, len(self.dut)), self.dut, pen=pg.mkPen(color=(255, 0, 0)), name='dut')
            self.graphWidget.plot(range(0, len(self.ref)), self.ref, pen=pg.mkPen(color=(0, 255, 0)), name='ref')
            self.graphWidget.plot(range(0, len(self.ref90)), self.ref90, pen=pg.mkPen(color=(0, 100, 255)),
                                  name='ref90')

        if plot:
            self.graphWidget.addLegend()
        self.X = []
        self.Y = []
        self.Xn = []
        self.Yn = []
        gofor = 0
        if len(self.dut) >= len(self.ref):
            gofor = len(self.ref)
        if len(self.dut) <= len(self.ref):
            gofor = len(self.dut)
        for i in range(0, gofor):
            self.X.append(self.dut[i] * self.ref[i])
            self.Xn.append(self.dut[i] * self.ref_norm[i])
        for i in range(0, gofor):
            self.Y.append(self.dut[i] * self.ref90[i])
            self.Yn.append(self.dut[i] * self.ref90n[i])
        # self.graphWidget.plot(range(0,len(self.X)), self.X,pen=pg.mkPen(color=(255, 0, 0)),name='X')
        # self.graphWidget.plot(range(0,len(self.Y)), self.Y,pen=pg.mkPen(color=(0, 255, 0)),name='Y')
        if len(self.X) > 0:
            mX = statistics.mean(self.X)
            mY = statistics.mean(self.Y)
            mXn = statistics.mean(self.Xn)
            mYn = statistics.mean(self.Yn)
            stdX = statistics.stdev(self.Xn)
            stdY = statistics.stdev(self.Yn)
            stdX = math.sqrt((2 * stdX) ** 2 + (2 * stdY) ** 2)
        else:
            mX, mY = 1, 0
        if plot:
            time.sleep(0.1)
            self.graphWidget.addLegend()
            time.sleep(0.1)
            self.graphWidget.addLegend()
        self.acquired_data = []
        self.acquired_data_X = []
        self.acquired_data_Y = []
        sa = -(180 * (math.atan2(mY, mX) / math.pi))
        dist = math.sqrt(mX ** 2 + mY ** 2)
        distn = math.sqrt(mXn ** 2 + mYn ** 2)
        if dist > 0:
            if len(self.ref) > 0:
                RRR = math.sqrt(statistics.mean([r ** 2 for r in self.ref]))
            else:
                RRR = 1
            # self.texttoupdate3="RRR = " + str(RRR)+" dist = "  +str(dist)+" distn = "  +str(distn)
            sb = 20 * math.log10((distn / RRR))
            dists = int(abs(math.log10(abs(distn)))) + 4
            string = "{:." + str(dists) + "f}"
            sas = int(abs(math.log10(abs(sa)))) + 4
            strings = "{:." + str(sas) + "f}"
            sbs = int(abs(math.log10(abs(sb)))) + 4
            stringbs = "{:." + str(sbs) + "f}"
            sxs = int(abs(math.log10(abs(mX)))) + 4
            stringxs = "{:." + str(sxs) + "f}"
            dist4 = int(abs(math.log10(abs(self.time_sample)))) + 4
            string3 = "{:." + str(dist4) + "f}"
            ssttrr = string3.format(self.time_sample)
            self.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = " + stringbs.format(
                sb) + " dB,\nX: " + stringxs.format(mX) + " Y: " + stringxs.format(
                mY) + " U\N{SUBSCRIPT TWO} = " + string.format(
                dist) + " V" + " U\N{SUBSCRIPT TWO} / U\N{SUBSCRIPT ONE} = " + string.format(
                (distn / RRR)) + " " + "\nTime duration = {0} s".format(ssttrr)
        else:
            self.text_to_update = "Phase = " + strings.format(sa) + "° and  gain = -Inf " + " dB X: " + stringxs.format(
                mX) + " Y: " + stringxs.format(mY)
        self.Gain.append(20 * math.log10(dist / RRR))
        self.Phase.append(sa)
        self.reader.calculated = True

    def plot_data(self):
        """
        self.graphWidget.clear()
        self.graphWidget.plotItem.setLogMode(True, False)
        self.graphWidget.plot(self.FreqMeasured, self.Gain,pen=pg.mkPen(color=(255, 0, 0)),name="Gain")
        self.graphWidget.plot(self.FreqMeasured, self.Phase,pen=pg.mkPen(color=(0, 255, 0)),name="Phase")
        self.graphWidget.addLegend()
        self.graphWidget.addLegend()
        """
        self.graphWidget.clear()
        self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.dut))], self.dut,
                              pen=pg.mkPen(color=(255, 0, 0)), name='dut')
        self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.ref))], self.ref,
                              pen=pg.mkPen(color=(0, 255, 0)), name='ref')
        # self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.refn))],self.refn,pen=pg.mkPen(color=(100, 0, 200)),name='refn')
        if self.sin_square_mode == True:
            self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.X))], self.X,
                                  pen=pg.mkPen(color=(0, 100, 255), style=Qt.DotLine), name='U2')
        if self.sin_square_mode == False:
            self.graphWidget.plot([x * 1 / self.sf for x in range(0, len(self.ref90))], self.ref90,
                                  pen=pg.mkPen(color=(0, 100, 255)), name='ref90')
        self.graphWidget.addLegend()
        self.graphWidget.setMouseEnabled(x=True, y=True)

    def start_stop_measurment(self):
        self.graphWidget.clear()
        if self.worker == None:
            self.worker = Worker(self, self.serial_thread)
        self.button_automatic_measurement.setText("Stop Measurment")
        if self.worker.running:
            self.button_automatic_measurement.setText("Automatic Measurment")
            self.worker.stop = True
            time.sleep(1)
            self.worker = Worker(self, self.serial_thread)
        else:
            self.worker = Worker(self, self.serial_thread)
            self.running = True
            self.stop = False
            self.openFileNameDialog()
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
        if self.reader.con_flag_stop == True:
            return
        if self.reader.con_flag == False:
            self.reader.con_flag = True
        else:
            self.reader.con_flag_stop = True

        """
        self.texttoupdate2 = 'Reading number ' + str(self.dataporbe)
        self.dataporbe = self.dataporbe + 1
        self.serth.ser_out('DATA\n')3


        if(self.rrr == False):
            self.reader.read = True
            self.rrr = True
        else:
            self.reader.read = False
            self.rrr = False
        """

    def measure(self):
        self.reader.single_flag = True

    # self.serth.data=[]
    # self.serth.ser_out("MEAS\n")
    # self.aquaredData=[]
    # self.serth.notread = 0
    #  self.sf = self.sample_per_periode*self.frek1
    # time_sample = 10000 / self.sf
    # time.sleep(0.2)
    # self.serth.ser_out('DATA\n')
    # time.sleep(6.5)
    #  self.serth.ser_out('DATA\n')

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

    def setEverithing0(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.data_bin = False
        self.serial_thread.send_all_counter = 0
        self.serial_thread.b = 0
        self.serial_thread.data = []
        self.text = []
        self.button13.setEnabled(False)
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("0\n")
        # self.edit10.setText(self.serth.ser_out(self.edit10.text()+"\n"))
        self.serial_thread.ser_out(self.edit10.text() + "\n")
        self.serial_thread.ser_out("SWEP\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out("D\n")
        # self.edit13.setText(self.serth.ser_out(self.edit13.text()+"\n"))
        self.serial_thread.ser_out(self.edit13.text() + "\n")
        self.serial_thread.ser_out("SWEP\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out("U\n")
        # self.edit14.setText(self.serth.ser_out(self.edit14.text()+"\n"))
        self.serial_thread.ser_out(self.edit14.text() + "\n")
        self.serial_thread.ser_out("STEP\n")
        self.serial_thread.ser_out("0\n")
        self.serial_thread.ser_out(self.edit12.text() + "\n")
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

    def setEverithing1(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.text = []
        self.serial_thread.send_all_counter = 0
        self.button23.setEnabled(False)
        self.serial_thread.ser_out("FRQ!\n")
        self.serial_thread.ser_out("1\n")
        # self.edit20.setText(self.serth.ser_out(self.edit20.text()+"\n"))
        self.serial_thread.ser_out(self.edit20.text() + "\n")
        self.serial_thread.ser_out("SWEP\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out("D\n")
        # self.edit23.setText(self.serth.ser_out(self.edit23.text()+"\n"))
        self.serial_thread.ser_out(self.edit23.text() + "\n")
        self.serial_thread.ser_out("SWEP\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out("U\n")
        # self.edit24.setText(self.serth.ser_out(self.edit24.text()+"\n"))
        self.serial_thread.ser_out(self.edit24.text() + "\n")
        self.serial_thread.ser_out("STEP\n")
        self.serial_thread.ser_out("1\n")
        self.serial_thread.ser_out(self.edit22.text() + "\n")
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

    def update_text(self):
        try:
            self.label_xy.setText(self.text_to_update)
            self.label_xy_2.setText(self.text_to_update_2)
            self.label_connect.setText(self.text_to_update_3)
        except RuntimeError:
            pass

    def __init__(self, parent=None):
        self.serial_thread = SerialThread(115200, self)  # Start serial thread
        self.serial_thread.start()
        self.rrr = False
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
            datafile = "icon.ico"
            datafile = os.path.join(sys.prefix, datafile)
            print(datafile)
            print("frozen")

        self.setWindowIcon(QtGui.QIcon(datafile))

        self.loadFileName = 'frec.csv'
        self.saveFileName = 'data.csv'
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
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
        self.text_to_update_3 = "Start empty"
        self.FreqMeasured = []
        self.Gain = []
        self.automatic_measurement_is_done = False
        self.sin_square_mode = False
        self.Phase = []
        self.last_data = ""
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
        self.acquired_data_Z = []
        self.text = []
        self.edit2 = QLineEdit("Write commands here..")
        self.button1 = QPushButton("SET")
        self.button2 = QPushButton("SET")
        self.layout_horizontal_gen = QHBoxLayout()
        self.layout_main_vertical = QVBoxLayout()
        self.layout_vertical_left_gen = QVBoxLayout()
        self.layout_vertical_right_gen = QVBoxLayout()
        self.layoutHH = QHBoxLayout()
        self.layout_horizontal_left_gen = QHBoxLayout()
        self.layout_horizontal_right_gen = QHBoxLayout()
        self.layout_horizontal_connect = QHBoxLayout()
        self.label_name = QLabel("Little Embedded Lock-in Bc. Jan Machálek, ver 1.0")
        self.layout_main_vertical.addWidget(self.label_name)
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
        self.qs_slider10.valueChanged.connect(self.qslider10update)
        self.qs_slider16 = QSlider(Qt.Horizontal, self)
        self.qs_slider16.setRange(0, 3300)
        self.qs_slider16.setFocusPolicy(Qt.NoFocus)
        self.qs_slider16.setPageStep(1)
        self.qs_slider16.valueChanged.connect(self.qslider16update)
        self.qs_slider15 = QSlider(Qt.Horizontal, self)
        self.qs_slider15.setRange(0, 100)
        self.qs_slider15.setFocusPolicy(Qt.NoFocus)
        self.qs_slider15.setPageStep(1)
        self.qs_slider15.valueChanged.connect(self.qslider15update)
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
        self.button13.clicked.connect(self.setEverithing0)
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
        self.qs_slider20.valueChanged.connect(self.qslider20update)
        self.qs_slider26 = QSlider(Qt.Horizontal, self)
        self.qs_slider26.setRange(0, 3300)
        self.qs_slider26.setFocusPolicy(Qt.NoFocus)
        self.qs_slider26.setPageStep(1)
        self.qs_slider26.valueChanged.connect(self.qslider26update)
        self.qs_slider25 = QSlider(Qt.Horizontal, self)
        self.qs_slider25.setRange(0, 100)
        self.qs_slider25.setFocusPolicy(Qt.NoFocus)
        self.qs_slider25.setPageStep(1)
        self.qs_slider25.valueChanged.connect(self.qslider25update)

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
        self.button23.clicked.connect(self.setEverithing1)
        self.label_xy = QLabel("XY")
        font1 = self.font()
        font1.setPointSize(15)
        self.label_xy.setFont(font1)
        self.label_xy_2 = QLabel("XY")
        self.label_connect = QLabel("Select comport to connect to!")
        self.edit_connect = QLineEdit("COM5")
        self.button_scan = QPushButton("Scan")
        self.button_connect = QPushButton("Connect")
        self.button_scan.clicked.connect(self.scan)
        self.button_connect.clicked.connect(self.connect)
        self.layout_main_vertical.addWidget(self.label_connect)
        self.layout_main_vertical.addWidget(self.edit_connect)
        self.layout_horizontal_connect.addWidget(self.button_scan)
        self.layout_horizontal_connect.addWidget(self.button_connect)
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
        self.button_reset = QPushButton("Reset")
        self.button_continuous = QPushButton("Continuous")
        self.button_single = QPushButton("Single")

        self.button_continuous.clicked.connect(self.read)
        self.button_single.clicked.connect(self.measure)
        self.button_load.clicked.connect(self.load)
        self.buttongraph4.clicked.connect(self.draw2)
        self.button_toggle_sin_square.clicked.connect(self.toggle)
        self.button_draw_data.clicked.connect(self.plot_data)
        self.button_automatic_measurement.clicked.connect(self.start_stop_measurment)
        self.button_save_as.clicked.connect(self.saveFileDialog)
        self.button_reset.clicked.connect(self.reset)

        self.drop_down_spp = QComboBox()
        for i in range(3, 11):
            self.drop_down_spp.addItem(str(2 ** i))
        self.drop_down_spp.currentIndexChanged.connect(self.spp)
        self.layout_main_vertical.addWidget(self.label_spp)
        self.layout_main_vertical.addWidget(self.drop_down_spp)
        self.layout_main_vertical.addWidget(self.label_xy)
        self.layout_main_vertical.addWidget(self.label_xy_2)
        self.layout_main_vertical.addWidget(self.graphWidget)
        self.layoutHH.addWidget(self.button_continuous)
        self.layoutHH.addWidget(self.button_single)
        self.layoutHH.addWidget(self.button_toggle_sin_square)
        self.layoutHH.addWidget(self.button_draw_data)
        self.layoutHH.addWidget(self.button_automatic_measurement)
        self.layoutHH.addWidget(self.button_save_as)
        self.layoutHH.addWidget(self.button_reset)
        self.layout_main_vertical.addLayout(self.layoutHH)
        self.layout_main_vertical.addWidget(self.edit27)
        self.setLayout(self.layout_main_vertical)
        self.e10()
        self.e15()
        self.e16()
        self.e20()
        self.e25()
        self.e26()


app = QApplication([])
window = Form()
window.show()
sys.exit(app.exec_())
