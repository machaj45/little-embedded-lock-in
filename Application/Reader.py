#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import time

from SerialThread import SerialThread


class Reader(QtCore.QThread):

    def __init__(self, gui, serial_thread):  # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.running = True
        self.stop = False
        self.gui = gui
        self.serial_thread = serial_thread
        self.counter = 0
        self.number_of_readings = 0
        self.read = False
        self.single_flag = False
        self.single_running = False
        self.time_single = 0
        self.time_sample = 0
        self.con_flag = False
        self.con_flag_stop = False
        self.con_running = False
        self.time_con = 0
        self.time_con = 0
        self.take_next_measurement = True
        self.con_init = True
        self.calculated = False
        self.in_scan_mode = False

    def reading(self):
        self.gui.text_to_update_3.put('Data read attempt #' + str(self.number_of_readings) + '\n')
        self.number_of_readings = self.number_of_readings + 1
        self.serial_thread.ser_out('DATA\n')

    def single(self):
        if self.single_flag:
            self.single_flag = False
            self.single_running = True
            self.serial_thread.data = []
            self.serial_thread.ser_out("MEAS\n")
            self.gui.acquired_data = []
            self.gui.sf = self.gui.sample_per_period * self.gui.frequency_gen_1
            self.time_sample = 10000 / self.gui.sf
            self.time_single = 0
        if self.single_running:
            self.time_single = self.time_single + 0.1
            if self.time_sample > 10 and self.single_running:
                self.gui.text_to_update_2 = "Time elapsed {0:.2f} s, Time for sampling = {1:.2f} s".format(
                    float(self.time_single), float(self.time_sample))
            if self.time_single >= self.time_sample + self.time_sample * 0.2 + 0.5:
                self.serial_thread.ser_out('DATA\n')
                self.single_running = False
            self.calculated = False

    def reset_serial_thread(self):
        """
        time.sleep(0.5)
        if not self.in_scan_mode and not self.gui.serial_thread_is_running:
            self.serial_thread = SerialThread(115200, self.gui, None)  # Start serial thread
            self.serial_thread.start()
            self.gui.serial_thread = self.serial_thread
            time.sleep(0.5)
        """
        pass

    def con(self):
        if self.con_flag:
            if self.con_init:
                self.con_running = True
                self.gui.sf = self.gui.sample_per_period * self.gui.frequency_gen_1
                self.time_sample = 10000 / self.gui.sf
                if self.time_sample <= 1:
                    self.time_sample = 1
                self.time_con = 0
                self.con_init = False
                self.calculated = True
            if self.take_next_measurement and self.calculated:
                if self.con_flag_stop:
                    self.con_flag = False
                    self.gui.text_to_update_3.put("end of continual measurement")
                    self.con_flag_stop = False
                    return
                self.calculated = False
                self.serial_thread.data = []
                self.time_con = 0
                self.serial_thread.ser_out("MEAS\n")
                self.gui.acquired_data = []
                self.take_next_measurement = False
            if self.con_running:
                self.time_con = self.time_con + 0.1
                if self.time_sample > 10 and not self.take_next_measurement:
                    self.gui.text_to_update_2 = "Time elapsed {0:.2f} s, Time for sampling = {1} s".format(
                        float(self.time_con), str(self.time_sample))
                if self.time_con >= self.time_sample + self.time_sample * 0.2:
                    self.serial_thread.ser_out('DATA\n')
                    self.time_con = 0
                    self.take_next_measurement = True
            if self.take_next_measurement and not self.calculated:
                self.time_con = 0
        else:
            self.con_init = True
            self.con_running = False

    def run(self):
        self.stop = False
        self.counter = 0
        self.number_of_readings = 0
        time.sleep(1)
        while not self.stop:
            time.sleep(0.01)
            self.counter = self.counter + 1
            if self.counter % 50 == 0 and self.read:
                self.reading()
            if self.counter % 10 == 0:
                self.single()
                self.con()
                self.reset_serial_thread()
            if self.counter >= 1000000:
                self.counter = 0
