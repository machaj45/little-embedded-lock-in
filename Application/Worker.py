#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore
import time


class Worker(QtCore.QThread):

    def __init__(self, gui, serial_thread):
        QtCore.QThread.__init__(self)
        self.running = False
        self.stop = False
        self.gui = gui
        self.serial_thread = serial_thread
        self.sf = 0
        self.f = None

    def end(self):
        self.gui.text = []
        self.gui.Gain = []
        self.gui.Phase = []
        self.gui.FreqMeasured = []
        self.gui.data_bin = False
        self.running = False
        self.gui.text_to_update = 'User End'
        self.gui.text_to_update_2 = 'User End'

    def run(self):
        self.running = True
        self.stop = False
        self.gui.text = []
        self.gui.Gain = []
        self.gui.Phase = []
        self.gui.FreqMeasured = []
        while self.gui.load():
            time.sleep(2)
            pass
        self.gui.text_to_update = 'Automatic Measurement Has Begun'
        i = 0
        for f in self.gui.Freq:
            self.gui.plot = False
            self.serial_thread.ser_out("FRQ!\n")
            self.serial_thread.ser_out("0\n")
            self.serial_thread.ser_out(str(f) + "\n")
            time.sleep(2)
            if self.stop:
                break
            try:
                fr = float(self.gui.last_data)
                self.gui.Freq[i] = fr
            except ValueError:
                self.gui.plainText.insertPlainText('ValueError in run in worker' + '\n')
                fr = f

            self.gui.sf = int(self.gui.sample_per_period * fr)
            self.sf = int(self.gui.sample_per_period * fr)
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
            if self.gui.sin_square_mode:
                self.gui.Phase.append(st)

            i = i + 1
            self.serial_thread.ser_out("OFFS\n")
            self.serial_thread.ser_out("0\n")
            a = (int(self.gui.edit16.text()) / 3300) * (2 ** 12)
            if a <= 0:
                a = 1
            if a >= 4095:
                a = 4095
            self.serial_thread.ser_out(str(int(a)) + "\n")
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break
            time.sleep(2)
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break

            self.gui.text_to_update_1 = str(self.gui.text)

            self.gui.text = []
            self.gui.text_to_update_2 = 'Frequency send: ' + str(f) + ' Hz, Real frequency is: ' + str(fr) + ' Hz'
            self.serial_thread.ser_out("MEAS\n")
            time_sample = 10000 / self.gui.sf
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break
            time.sleep(time_sample + 1)
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break
            self.serial_thread.ser_out("DATA\n")
            # time.sleep(2)
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break
            time.sleep(7)
            if self.stop:
                self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                break
            while not self.gui.data_done:
                self.serial_thread.ser_out("DATA\n")
                if self.stop:
                    self.gui.text_to_update = 'Automatic Measurement Has been Stopped by user'
                    break
                time.sleep(1)
            self.gui.data_done = False
        self.gui.text_to_update_1 = 'Done'
        self.gui.text_to_update_2 = 'Done'
        self.gui.button_automatic_measurement.setText("Automatic Measurement")
        self.gui.save()
        self.f = None
        if not self.stop:
            self.gui.automatic_measurement_is_done = True
