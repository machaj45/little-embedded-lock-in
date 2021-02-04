import serial
import time
import serial.tools.list_ports
import struct
import math
from PyQt5 import QtCore
import queue as Queue
SER_TIMEOUT = 0.08


class SerialThread(QtCore.QThread):
    def __init__(self, baudrate, gui):  # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.baudrate = baudrate
        self.txq = Queue.Queue()
        self.running = True
        self.sended = False
        self.gui = gui
        self.a = 0
        self.buf = ""
        self.dataarrived = False
        self.comport = None
        self.s = []

    def str_bytes(self, s):
        return s.encode('latin-1')

    def ser_out(self, s):
        self.txq.put(s)

    def ser_in(self, s):  # Write incoming serial data to screen
        # self.gui.setWindowTitle(s)
        pass

    def initrun(self):
        self.ser = serial.Serial(baudrate=self.baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE, timeout=SER_TIMEOUT, write_timeout=0.01)
        self.test = 0
        self.count = 1
        self.portConnected = 'nop'
        self.a = 0
        self.b = 1
        self.notready = 0

    def comportsearch(self):
        for i in serial.tools.list_ports.comports():
            self.ser.port = i.device
            try:
                with self.ser as s:
                    time.sleep(0.2)
                    s.write(b'IDN?\n')
                    s.flush()
                    data = s.read(size=14)
                    if len(data) > 0:
                        try:
                            if ("DDS Generator\n" == data.decode('ascii')):
                                # print("i.device")
                                self.portConnected = i.device
                                self.ser.port = i.device
                                self.test = self.test + 1
                                break
                        except UnicodeDecodeError:
                            print("here")
                    s.flushInput()
                    self.ser.close()
            except serial.serialutil.SerialTimeoutException:
                print("Error timeout on port {}".format(i.device))
            except serial.serialutil.SerialException:
                self.ser.close()
                self.initrun()
                self.gui.texttoupdate = "Device has been disconnected in comportsearch"
                continue

        return self.portConnected

    def scan(self):
        self.running = False
        time.sleep(0.1)
        self.initrun()
        self.gui.texttoupdate3 = "Faund devices are: "
        for i in serial.tools.list_ports.comports():
            self.ser.port = i.device
            try:
                with self.ser as s:
                    time.sleep(0.2)
                    s.write(b'IDN?\n')
                    s.flush()
                    data = s.read(size=14)
                    if len(data) > 0:
                        try:
                            if ("DDS Generator\n" == data.decode('ascii')):
                                self.gui.texttoupdate3 = self.gui.texttoupdate3 + " " + str(i.device)
                        except UnicodeDecodeError:
                            print("here")
                    s.flushInput()
                    self.ser.close()
            except serial.serialutil.SerialTimeoutException:
                print("Error timeout on port {}".format(i.device))
            except serial.serialutil.SerialException:
                self.ser.close()
                self.initrun()
                self.gui.texttoupdate = "Device has been disconnected in scan"
                continue

        return self.portConnected

    def setGui1(self):
        self.gui.label15.setText("Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[4][:-2], int(
            3300 * (float(self.gui.text[4][:-2]) / 100))))
        a = int(3300 * (float(self.gui.text[5][:-1]) / (2 ** 12)))
        if (a == 0):
            a = 0
        else:
            a = int(3300 * (float(self.gui.text[5][:-1]) / (2 ** 12))) + 1
        self.gui.label16.setText("Offset - {0} mV".format(a))
        self.gui.label11.setText("Frequency - {0} Hz".format(self.gui.text[0][:-1]))
        self.gui.frek1 = float(self.gui.text[0][:-1])
        self.gui.label12.setText("Step - {0} Hz".format(self.gui.text[3][:-1]))
        self.gui.label13.setText("F Start - {0} Hz".format(self.gui.text[1][:-1]))
        self.gui.label14.setText("F Stop - {0} Hz".format(self.gui.text[2][:-1]))
        self.gui.button13.setEnabled(True)

    def setGui2(self):
        self.gui.label25.setText("Amplitude - {0} %, Upp = {1} mV".format(self.gui.text[4][:-2], int(
            3300 * (float(self.gui.text[4][:-2]) / 100))))
        a = int(3300 * (int(self.gui.text[5][:-1]) / (2 ** 12))) + 1
        if (a == 1):
            a = 0
        self.gui.label26.setText("Offset - {0} mV".format(a))
        self.gui.label21.setText("Frequency - {0} Hz".format(self.gui.text[0][:-1]))
        self.gui.label22.setText("Step - {0} Hz".format(self.gui.text[3][:-1]))
        self.gui.label23.setText("F Start - {0} Hz".format(self.gui.text[1][:-1]))
        self.gui.label24.setText("F Stop - {0} Hz".format(self.gui.text[2][:-1]))
        self.gui.button23.setEnabled(True)

    def asciMode(self, s, txd):
        self.ser.timeout = SER_TIMEOUT
        s.write_timeout = 0.09
        self.data = self.ser.read_until('\n')
        if self.data:
            self.dataarrived = True
            try:
                self.gui.setWindowTitle("Send {0}, Received {1}".format(txd, self.data.decode('ascii')))
                self.gui.edit27.setText("{0}".format(self.data.decode('ascii')))
                self.gui.lastdata = "{0}".format(self.data.decode('ascii'))
            except UnicodeDecodeError:
                self.gui.databin = True
                self.gui.setWindowTitle("Turning on bin mode")
                return
            self.gui.text.append(self.data.decode('ascii'))
            if (self.gui.lastdata == "MD\n\r"):
                self.notready = 0
                self.gui.databin = True
                self.gui.dataready = True
                self.ser_out("DATA\n")
                self.gui.lastdata = ""
                # self.gui.texttoupdate = "Measrument done"

            if (self.gui.lastdata == "DNR\n\r"):
                self.notready = self.notready + 1
                self.gui.lastdata = ""
                self.gui.texttoupdate2 = self.gui.texttoupdate2 + " DNR " + str(self.notready)
            self.a = self.a + 1
            self.b = self.b + 1

        if self.a == 6:
            self.a = 0
            self.b = 1
            if (self.gui.button23.isEnabled() and not self.gui.button13.isEnabled()):
                self.setGui1()
            elif (self.gui.button13.isEnabled() and not self.gui.button23.isEnabled()):
                self.setGui2()
            self.gui.text = []

    def binMode(self, s):
        s.timeout = 6
        a = int(10000 / self.gui.sample_per_periode)
        samples = (a - 1) * (self.gui.sample_per_periode)
        self.gui.texttoupdate2 = str(samples)
        self.gui.datadone = True
        self.data = s.read(int(samples) * 4)
        s.timeout = SER_TIMEOUT
        self.gui.databin = False

        if self.data:
            # print('aj')
            a = int(len(self.data) / 2)
            # self.gui.texttoupdate="delka je  "+ str(a)
            for i in range(0, a):
                number = int(self.data[i * 2]) + int(self.data[i * 2 + 1] * 255)
                self.gui.aquaredData.append(number)
            self.data = []
            self.gui.aquaredDataX += (self.gui.aquaredData[0:-1:2])
            self.gui.aquaredDataY += (self.gui.aquaredData[1:-1:2])
            self.aquaredData = []
            self.gui.draw33(self.gui.plot)

    def binMode2(self, s):
        if (False):
            self.data = []
            self.data = s.read(8)
            if self.data:
                if len(self.data) == 8:
                    self.gui.dataX = struct.unpack('<f', self.data[0:4:1])[0]
                    self.gui.dataY = struct.unpack('<f', self.data[4:8:1])[0]
                    self.gui.databin = False
        else:
            self.data = []
            self.data = s.read(8)
            if self.data:
                if len(self.data) == 8:
                    self.gui.dataX = struct.unpack('<f', self.data[0:4:1])[0]
                    self.gui.dataY = struct.unpack('<f', self.data[4:8:1])[0]
                    theta = 180 * (math.atan2(self.gui.dataY, self.gui.dataX) / math.pi)
                    if (math.sqrt((self.gui.dataX) ** 2 + (self.gui.dataY) ** 2) > 0):
                        RR = 20 * math.log10(math.sqrt((self.gui.dataX) ** 2 + (self.gui.dataY) ** 2))
                        self.gui.texttoupdate = "X = " + str(self.gui.dataX) + " Y = " + str(
                            self.gui.dataY) + " theta = " + str(theta) + "°, R =" + str(RR) + 'dB'
                    else:
                        RR = '-inf'
                        self.gui.texttoupdate = "X = " + str(self.gui.dataX) + " Y = " + str(
                            self.gui.dataY) + " theta = " + str(theta) + "°, R =" + str(RR) + ' dB'
                    self.gui.databin = False
                else:
                    self.gui.texttoupdate = "data wron length"

    def check(self):
        checkout = False
        self.ser.port = self.comport
        try:
            with self.ser as s:
                s.write(b'IDN?\n')
                s.flush()
                data = s.read(size=14)
                if len(data) > 0:
                    try:
                        if ("DDS Generator\n" == data.decode('ascii')):
                            checkout = True
                    except UnicodeDecodeError:
                        print("here")
                s.flushInput()
                self.ser.close()
        except serial.serialutil.SerialException:
            self.ser.close()
            self.initrun()
            self.gui.texttoupdate = "Device has been disconnected in scan"
        return checkout

    def run(self):
        txd = ''
        self.initrun()
        if (self.comport == None):
            while (self.test == 0):
                time.sleep(0.2)
                self.portConnected = self.comportsearch()
                if (self.portConnected != 'nop'):
                    self.ser.port = self.portConnected
                    self.comport = self.ser.port
                else:
                    self.gui.button13.setEnabled(True)
                self.gui.setWindowTitle('Not Connected attempt {0}'.format(self.count))
                self.count = self.count + 1
                if (self.count > 10):
                    self.ser.close()
                    self.initrun()
        else:
            self.ser.port = self.comport

        if (self.check()):
            self.gui.setWindowTitle("Opening %s at %u baud" % (self.ser.port, self.baudrate))
            self.gui.texttoupdate3 = "Opening %s at %u baud" % (self.ser.port, self.baudrate)
        else:
            self.gui.setWindowTitle("Un able to connect to comport %s " % (self.ser.port))

        # -------------------------------------------------------------------------------#
        # Connected to right port
        # -------------------------------------------------------------------------------#

        if not self.ser:
            print("Can't open port")
            self.running = False

        while self.running:
            try:
                with self.ser as s:
                    if not self.txq.empty():
                        txd = str(self.txq.get())
                        # self.gui.texttoupdate2=txd
                        s.write(self.str_bytes(txd))
                        s.flush()
                        self.sended = True
                    if self.gui.databin == False:
                        self.asciMode(s, txd)
                    else:
                        self.binMode(s)
                        self.gui.databin = False
                    self.data = []
            except serial.serialutil.SerialException:
                self.gui.texttoupdate = "Device has been disconected in running"
                self.gui.button13.setEnabled(True)
                time.sleep(SER_TIMEOUT)
        if self.ser:
            self.ser.close()
            self.ser = None
