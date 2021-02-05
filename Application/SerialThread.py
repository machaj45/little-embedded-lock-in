import serial
import time
import serial.tools.list_ports
from PyQt5 import QtCore
import queue

SER_TIMEOUT = 0.08


class SerialThread(QtCore.QThread):
    def __init__(self, baud_rate, gui):  # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.baud_rate = baud_rate
        self.data_out_queue = queue.Queue()
        self.running = True
        self.gui = gui
        self.send_all_counter = 0
        self.comport = None
        self.serial = None
        self.test = 0
        self.count = 0
        self.portConnected = 0
        self.counter_of_dnr_answers = 0
        self.data = 0

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
        self.test = 0
        self.count = 1
        self.portConnected = 'nop'
        self.send_all_counter = 0
        self.counter_of_dnr_answers = 0

    def comport_search(self):
        for i in serial.tools.list_ports.comports():
            self.serial.port = i.device
            try:
                with self.serial as s:
                    time.sleep(0.2)
                    s.write(b'IDN?\n')
                    s.flush()
                    data = s.read(size=18)
                    if len(data) > 0:
                        try:
                            if "Lock-in Amplifier\n" == data.decode('ascii'):
                                # print("i.device")
                                self.portConnected = i.device
                                self.serial.port = i.device
                                self.test = self.test + 1
                                break
                        except UnicodeDecodeError:
                            print("here")
                    s.flushInput()
                    self.serial.close()
            except serial.serialutil.SerialTimeoutException:
                print("Error timeout on port {}".format(i.device))
            except serial.serialutil.SerialException:
                self.serial.close()
                self.initialize_run_method()
                self.gui.text_to_update = "Device has been disconnected in comport_search()"
                continue

        return self.portConnected

    def scan(self):
        self.running = False
        time.sleep(0.1)
        self.initialize_run_method()
        self.gui.text_to_update_3 = "Found devices are: "
        for i in serial.tools.list_ports.comports():
            self.serial.port = i.device
            try:
                with self.serial as s:
                    time.sleep(0.2)
                    s.write(b'IDN?\n')
                    s.flush()
                    data = s.read(size=18)
                    if len(data) > 0:
                        try:
                            if "Lock-in Amplifier\n" == data.decode('ascii'):
                                self.gui.text_to_update_3 = self.gui.text_to_update_3 + " " + str(i.device)
                        except UnicodeDecodeError:
                            print("UnicodeDecodeError in Scan method")
                    s.flushInput()
                    self.serial.close()
            except serial.serialutil.SerialTimeoutException:
                print("Error timeout on port {}".format(i.device))
            except serial.serialutil.SerialException:
                self.serial.close()
                self.initialize_run_method()
                self.gui.text_to_update = "SerialException in Scan method -> closing serial and running " \
                                          "initialize_run_method() "
                continue

        return self.portConnected

    def set_left_gen_gui(self):
        self.gui.label15.setText("Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[4][:-2], int(
            3300 * (float(self.gui.text[4][:-2]) / 100))))
        a = int(3300 * (float(self.gui.text[5][:-1]) / (2 ** 12)))
        if a == 0:
            a = 0
        else:
            a = int(3300 * (float(self.gui.text[5][:-1]) / (2 ** 12))) + 1
        self.gui.label16.setText("Offset - {0} mV".format(a))
        self.gui.label11.setText("Frequency - {0} Hz".format(self.gui.text[0][:-1]))
        self.gui.frequency_gen_1 = float(self.gui.text[0][:-1])
        self.gui.label12.setText("Step - {0} Hz".format(self.gui.text[3][:-1]))
        self.gui.label13.setText("F Start - {0} Hz".format(self.gui.text[1][:-1]))
        self.gui.label14.setText("F Stop - {0} Hz".format(self.gui.text[2][:-1]))
        self.gui.button13.setEnabled(True)

    def set_right_gen_gui(self):
        self.gui.label25.setText("Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[4][:-2], int(
            3300 * (float(self.gui.text[4][:-2]) / 100))))
        a = int(3300 * (int(self.gui.text[5][:-1]) / (2 ** 12))) + 1
        if a == 1:
            a = 0
        self.gui.label26.setText("Offset - {0} mV".format(a))
        self.gui.label21.setText("Frequency - {0} Hz".format(self.gui.text[0][:-1]))
        self.gui.label22.setText("Step - {0} Hz".format(self.gui.text[3][:-1]))
        self.gui.label23.setText("F Start - {0} Hz".format(self.gui.text[1][:-1]))
        self.gui.label24.setText("F Stop - {0} Hz".format(self.gui.text[2][:-1]))
        self.gui.button23.setEnabled(True)

    def asci_mode(self, s, txd):
        self.serial.timeout = SER_TIMEOUT
        s.write_timeout = 0.09
        self.data = self.serial.read_until('\n')
        if self.data:
            try:
                self.gui.setWindowTitle("Send {0}, Received {1}".format(txd, self.data.decode('ascii')))
                self.gui.edit27.setText("{0}".format(self.data.decode('ascii')))
                self.gui.last_data = "{0}".format(self.data.decode('ascii'))
            except UnicodeDecodeError:
                self.gui.data_bin = True
                self.gui.setWindowTitle("Turning on bin mode")
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
                self.gui.text_to_update_2 = self.gui.text_to_update_2 + " DNR " + str(self.counter_of_dnr_answers)
            self.send_all_counter = self.send_all_counter + 1

        if self.send_all_counter == 6:
            self.send_all_counter = 0
            if self.gui.button23.isEnabled() and not self.gui.button13.isEnabled():
                self.set_left_gen_gui()
            elif self.gui.button13.isEnabled() and not self.gui.button23.isEnabled():
                self.set_right_gen_gui()
            self.gui.text = []

    def bin_mode(self, open_serial):
        open_serial.timeout = 6
        data_length_in_bytes = int(10000 / self.gui.sample_per_periode)
        samples = (data_length_in_bytes - 1) * self.gui.sample_per_periode
        self.gui.text_to_update_2 = str(samples)
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
            self.gui.aquaredDataX += (self.gui.acquired_data[0:-1:2])
            self.gui.aquaredDataY += (self.gui.acquired_data[1:-1:2])
            self.gui.draw33(self.gui.plot)

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
                        print("here")
                s.flushInput()
                self.serial.close()
        except serial.serialutil.SerialException:
            self.serial.close()
            self.initialize_run_method()
            self.gui.text_to_update = "Device has been disconnected in scan"
        return checkout

    def run(self):
        data_out_queue = ''
        self.initialize_run_method()
        if self.comport is None:
            while self.test == 0:
                time.sleep(0.2)
                self.portConnected = self.comport_search()
                if self.portConnected != 'nop':
                    self.serial.port = self.portConnected
                    self.comport = self.serial.port
                else:
                    self.gui.button13.setEnabled(True)
                self.gui.setWindowTitle('Not Connected attempt {0}'.format(self.count))
                self.count = self.count + 1
                if self.count > 10:
                    self.serial.close()
                    self.initialize_run_method()
        else:
            self.serial.port = self.comport

        if self.check():
            self.gui.setWindowTitle("Opening %s at %u baud" % (self.serial.port, self.baud_rate))
            self.gui.text_to_update_3 = "Opening %s at %u baud" % (self.serial.port, self.baud_rate)
        else:
            self.gui.setWindowTitle("Un able to connect to comport %s " % self.serial.port)

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
                        data_out_queue = str(self.data_out_queue.get())
                        s.write(self.str_bytes(data_out_queue))
                        s.flush()
                    if not self.gui.data_bin:
                        self.asci_mode(s, data_out_queue)
                    else:
                        self.bin_mode(s)
                        self.gui.data_bin = False
                    self.data = []
            except serial.serialutil.SerialException:
                self.gui.text_to_update = "SerialException in running enabling send all button and waiting"
                self.gui.button13.setEnabled(True)
                time.sleep(SER_TIMEOUT)
        if self.serial:
            self.serial.close()
            self.serial = None
