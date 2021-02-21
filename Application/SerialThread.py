#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import serial.tools.list_ports
from PyQt5 import QtCore
import queue

SER_TIMEOUT = 0.08


class SerialThread(QtCore.QThread):
    def __init__(self, baud_rate, gui, comport):  # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.baud_rate = baud_rate
        self.data_out_queue = queue.Queue()
        self.running = True
        self.gui = gui
        self.send_all_counter = 0
        self.comport = comport
        self.serial = None
        self.count = 0
        self.available_ports = []
        self.counter_of_dnr_answers = 0
        self.data = 0
        self.gui.data_bin = False

    @staticmethod
    def str_bytes(s):
        return s.encode('latin-1')

    def ser_out(self, s):
        self.data_out_queue.put(s)

    def ser_in(self, s):  # Write incoming serial data to screen
        # self.gui.setWindowTitle(s)
        pass

    def initialize_run_method(self):
            self.serial = serial.Serial(baudrate=self.baud_rate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE, timeout=SER_TIMEOUT, write_timeout=0.01)
            self.count = 1
            self.available_ports = []
            self.send_all_counter = 0
            self.counter_of_dnr_answers = 0

    def comport_search(self):
        for i in serial.tools.list_ports.comports():
            self.serial.port = i.device
            try:
                with self.serial as s:
                    time.sleep(0.5)
                    s.write(b'IDN?\n')
                    s.flush()
                    data = s.read(size=18)
                    if len(data) > 0:
                        try:
                            if "Lock-in Amplifier\n" == data.decode('ascii'):
                                # print("i.device")
                                self.available_ports.append(i.device)
                                self.serial.port = i.device
                        except UnicodeDecodeError:
                            self.gui.text_to_update_3.put('UnicodeDecodeError in comport_search' + '\n')
                    s.flushInput()
                self.serial.close()
            except serial.serialutil.SerialTimeoutException:
                self.gui.text_to_update_3.put("Error timeout on port {}".format(i.device) + '\n')
                if self.serial:
                    self.serial.close()
                    self.running = False
            except serial.serialutil.SerialException as e:
                self.gui.text_to_update_3.put("SerialException in comport_search()" + '\n' + str(e))
                if self.serial:
                    self.serial.close()
                    self.running = False
                break

        return self.available_ports

    def set_left_gen_gui(self):
        self.gui.label_amplitude_left_text = "Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[0][:-2], int(
            3300 * (float(self.gui.text[0][:-2]) / 100)))
        a = int(3300 * (float(self.gui.text[2][:-1]) / (2 ** 12)))
        if a == 0:
            a = 0
        else:
            a = int(3300 * (float(self.gui.text[2][:-1]) / (2 ** 12))) + 1
        self.gui.label_offset_left_text = "Offset - {0} mV".format(a)
        self.gui.label_frequency_left_text = "Frequency - {0} Hz".format(self.gui.text[1][:-1])
        self.gui.frequency_gen_1 = float(self.gui.text[1][:-1])
        self.gui.button_setup_left.setEnabled(True)

    def set_right_gen_gui(self):
        self.gui.label25_text = "Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[0][:-2], int(
            3300 * (float(self.gui.text[0][:-2]) / 100)))
        a = int(3300 * (float(self.gui.text[2][:-1]) / (2 ** 12))) + 1
        if a == 1:
            a = 0
        self.gui.label26_text = "Offset - {0} mV".format(a)
        self.gui.label21_text = "Frequency - {0} Hz".format(self.gui.text[1][:-1])
        self.gui.button23.setEnabled(True)

    def asci_mode(self, s, txd):
        self.serial.timeout = SER_TIMEOUT
        s.write_timeout = 0.09
        self.data = self.serial.read_until('\n')
        if self.data:
            try:
                text_decoded = self.data.decode('ascii')
                if text_decoded[-1] == '\r':
                    text_decoded = text_decoded[:-1]
                self.gui.text_to_update_3.put("Send {0},\t Received {1}".format(txd[:-1], text_decoded))
                self.gui.last_data = "{0}".format(self.data.decode('ascii'))
            except UnicodeDecodeError:
                self.gui.data_bin = True
                self.gui.text_to_update_3.put("Turning on bin mode\n")
                return
            self.gui.text.append(self.data.decode('ascii'))
            if self.gui.last_data == "MD\n\r":
                self.counter_of_dnr_answers = 0
                self.gui.data_bin = True
                self.gui.data_ready = True
                self.ser_out("DATA\n")
                self.gui.last_data = ""
            if self.gui.last_data == "DNR\n\r":
                self.counter_of_dnr_answers = self.counter_of_dnr_answers + 1
                self.gui.last_data = ""
                self.gui.text_to_update_3.put("DNR #" + str(self.counter_of_dnr_answers) + '\n')

            self.send_all_counter = self.send_all_counter + 1

        if self.send_all_counter == 3:
            self.send_all_counter = 0
            if self.gui.button23.isEnabled() and not self.gui.button_setup_left.isEnabled():
                self.set_left_gen_gui()
            elif self.gui.button_setup_left.isEnabled() and not self.gui.button23.isEnabled():
                self.set_right_gen_gui()
            self.gui.text = []

    def bin_mode(self, open_serial):
        open_serial.timeout = 6
        data_length_in_bytes = int(10000 / self.gui.sample_per_period)
        samples = (data_length_in_bytes - 1) * self.gui.sample_per_period
        self.gui.text_to_update_3.put("Number of samples " + str(samples) + '\n')
        self.gui.data_done = True
        self.data = open_serial.read(int(samples) * 4)
        open_serial.timeout = SER_TIMEOUT
        self.gui.data_bin = False

        if self.data:
            data_length_in_bytes = int(len(self.data) / 2)
            for i in range(0, data_length_in_bytes):
                number = int(self.data[i * 2]) + int(self.data[i * 2 + 1] * 255)
                self.gui.acquired_data.append(number)
            self.data = []
            self.gui.acquired_data_X += (self.gui.acquired_data[0:-1:2])
            self.gui.acquired_data_Y += (self.gui.acquired_data[1:-1:2])
            self.gui.do_calculation_flag = True

    def check(self):
        checkout = False
        self.serial.port = self.comport
        try:
            with self.serial as s:
                s.write(b'IDN?\n')
                s.flush()
                data = s.read(size=18)
                if len(data) > 0:
                    try:
                        if "Lock-in Amplifier\n" == data.decode('ascii'):
                            checkout = True
                    except UnicodeDecodeError:
                        self.gui.text_to_update_3.put("UnicodeDecodeError in check\n")
                s.flushInput()
                s.write(b'VER?\n')
                s.flush()
                data = s.read(size=14)
                if len(data) > 0:
                    try:
                        self.gui.fir_version = data.decode('ascii')
                        i = 1
                        check = 0
                        txt = self.gui.fir_version[8:-1]
                        for ss in txt:
                            if ss == self.gui.gui_version[i]:
                                check = check + 1
                            i = i + 1
                        if check == 5:
                            self.gui.text_to_update_3.put("Firmware version and gui version are same!\n")
                        else:
                            self.gui.text_to_update_3.put("Firmware version and gui version are not same!\n")
                            self.gui.text_to_update_3.put("Please update your firmware!\n")

                    except UnicodeDecodeError:
                        self.gui.text_to_update_3.put("UnicodeDecodeError in check\n")
                s.flushInput()
                self.serial.close()
        except serial.serialutil.SerialException as e:
            if self.serial:
                self.serial.close()
                self.running = False
            self.gui.text_to_update_3.put("SerialException in check\n" + str(e))
        return checkout

    def run(self):
        time.sleep(1)
        self.running = True
        self.gui.text_to_update_3.put("Start of serial Thread")
        self.gui.serial_thread_is_running = True
        data_out_queue_string = ''
        self.initialize_run_method()
        t_comport = None
        if self.comport is not None:
            t_comport = self.comport

        while len(self.available_ports) == 0 and self.running:
            self.available_ports = self.comport_search()
            if len(self.available_ports) > 0:
                self.serial.port = self.available_ports[0]
                self.comport = self.serial.port
            else:
                self.gui.button_setup_left.setEnabled(True)
            self.gui.text_to_update_3.put('Not Connected, attempting to connect number {0}\n'.format(self.count))
            self.count = self.count + 1
            if self.count > 10:
                if self.serial:
                    self.serial.close()
                self.initialize_run_method()

            if t_comport is not None:
                self.serial.port = t_comport
                self.comport = t_comport
            else:
                self.serial.port = self.comport

        if self.running and self.check():
            self.gui.text_to_update_3.put("Connected to %s at %u baud" % (self.serial.port, self.baud_rate) + '\n')
        else:
            if self.serial is not None:
                self.gui.text_to_update_3.put("Unable to connect to comport %s " % self.serial.port + '\n')
            else:
                self.gui.text_to_update_3.put("Unable to connect to comport self.serial is None\n")
            self.running = False

        # -------------------------------------------------------------------------------#
        # Connected to right port
        # -------------------------------------------------------------------------------#

        if not self.serial:
            print("Can't open port")
            self.running = False

        while self.running:
            try:
                with self.serial as s:
                    if not self.data_out_queue.empty():
                        data_out_queue_string = str(self.data_out_queue.get())
                        s.write(self.str_bytes(data_out_queue_string))
                        s.flush()
                    if not self.gui.data_bin:
                        self.asci_mode(s, data_out_queue_string)
                    else:
                        self.bin_mode(s)
                        self.gui.data_bin = False
                    self.data = []
            except serial.serialutil.SerialException:
                self.gui.text_to_update_3.put("SerialException in running enabling send all \
                                               button and waiting\n")
                if self.serial:
                    self.serial.close()
                    self.running = False
                self.gui.button_setup_left.setEnabled(True)
                if self.serial:
                    self.serial.close()
                    self.running = False
                self.available_ports = []
        if self.serial:
            self.serial.close()
            self.serial = None
        self.gui.text_to_update_3.put("End of serial Thread")
        self.gui.serial_thread_is_running = False
        self.deleteLater()
