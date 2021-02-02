# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QApplication
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout,QComboBox,QSlider,QFileDialog,QAction
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
        #print('end')
        self.serth.running = False
        self.serth.ser.close()

    def make_gui(self):
        font = self.font()
        font.setPointSize(10)
        self.worker = None
        self.sf = 10;
        self.window().setFont(font)
        self.countofdrawing=0
        datafile = "icon.ico"
        if not hasattr(sys, "frozen"):
            datafile = os.path.join(os.path.dirname(__file__), datafile)
        else:
            datafile = os.path.join(sys.prefix, datafile)
        self.setWindowIcon(QtGui.QIcon(datafile))
        self.loadFileName = 'frec.csv'
        self.saveFileName = 'data.csv'
        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)
        self.backup1=[]
        self.backup2=[]
        self.aquaredDataYY= []
        self.plot=False
        self.frek1 =100
        self.aquaredDataXX= []
        self.time_sample =1
        self.aquaredDataZZ = []
        self.dataporbe=0
        self.backup3=[]
        self.texttoupdate="Start empty"
        self.texttoupdate2="Start empty"
        self.texttoupdate3="Start empty"
        self.FreqMeasured=[]
        self.Gain = []
        self.automaticMeasurmetIsDone  = False
        self.sinsquaremode = False
        self.Phase = []
        self.lastdata = ""
        self.Freq =[]
        self.datadone = False
        self.dataX=0
        self.dataY=0
        self.dataready = False
        self.dut =[]
        self.ref = []
        self.ref90=[]
        self.refn = []
        self.ref90n=[]
        self.X=[]
        self.Y=[]
        self.Xn=[]
        self.Yn=[]
        self.databin=False
        self.sample_per_periode=32
        self.aquaredData=[]
        self.aquaredDataX=[]
        self.aquaredDataY=[]
        self.aquaredDataZ=[]
        self.text = []
        self.edit2 = QLineEdit("Write commands here..")
        self.button1 = QPushButton("SET")
        self.button2 = QPushButton("SET")
        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.layoutV1 = QVBoxLayout()
        self.layoutV2 = QVBoxLayout()
        self.layoutHH = QHBoxLayout()
        self.layoutHgen0 = QHBoxLayout()
        self.layoutHgen1 = QHBoxLayout()
        self.layoutHHcon = QHBoxLayout()
        self.labelname = QLabel("Little Embedded Lock-in Bc. Jan Machálek, ver 1.0")
        self.layoutV.addWidget(self.labelname)
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
        self.qslider10 = QSlider(Qt.Horizontal, self)
        self.qslider10.setRange(0, 130000)
        self.qslider10.setFocusPolicy(Qt.NoFocus)
        self.qslider10.setPageStep(1)
        self.qslider10.valueChanged.connect(self.qslider10update)
        self.qslider16 = QSlider(Qt.Horizontal, self)
        self.qslider16.setRange(0, 3300)
        self.qslider16.setFocusPolicy(Qt.NoFocus)
        self.qslider16.setPageStep(1)
        self.qslider16.valueChanged.connect(self.qslider16update)
        self.qslider15 = QSlider(Qt.Horizontal, self)
        self.qslider15.setRange(0, 100)
        self.qslider15.setFocusPolicy(Qt.NoFocus)
        self.qslider15.setPageStep(1)
        self.qslider15.valueChanged.connect(self.qslider15update)


        self.layoutV1.addWidget(self.label10)
        self.layoutV1.addWidget(self.label15)
        self.layoutV1.addWidget(self.edit15)
        self.layoutV1.addWidget(self.qslider15)
        self.layoutV1.addWidget(self.label16)
        self.layoutV1.addWidget(self.edit16)
        self.layoutV1.addWidget(self.qslider16)
        self.layoutV1.addWidget(self.label11)
        self.layoutV1.addWidget(self.edit10)
        self.layoutV1.addWidget(self.qslider10)
        #self.layoutV1.addWidget(self.label12)
        #self.layoutV1.addWidget(self.edit12)
        #self.layoutV1.addWidget(self.label13)
        #self.layoutV1.addWidget(self.edit13)
        #self.layoutV1.addWidget(self.label14)
        #self.layoutV1.addWidget(self.edit14)
        self.layoutHgen0.addWidget(self.button13)
        self.layoutHgen0.addWidget(self.button10)
        self.layoutHgen0.addWidget(self.button11)
        #self.layoutV1.addWidget(self.button12)

        self.layoutV1.addLayout(self.layoutHgen0)
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
        self.qslider20 = QSlider(Qt.Horizontal, self)
        self.qslider20.setRange(0, 130000)
        self.qslider20.setFocusPolicy(Qt.NoFocus)
        self.qslider20.setPageStep(1)
        self.qslider20.valueChanged.connect(self.qslider20update)
        self.qslider26 = QSlider(Qt.Horizontal, self)
        self.qslider26.setRange(0, 3300)
        self.qslider26.setFocusPolicy(Qt.NoFocus)
        self.qslider26.setPageStep(1)
        self.qslider26.valueChanged.connect(self.qslider26update)
        self.qslider25 = QSlider(Qt.Horizontal, self)
        self.qslider25.setRange(0, 100)
        self.qslider25.setFocusPolicy(Qt.NoFocus)
        self.qslider25.setPageStep(1)
        self.qslider25.valueChanged.connect(self.qslider25update)

        self.layoutV2.addWidget(self.label20)
        self.layoutV2.addWidget(self.label25)
        self.layoutV2.addWidget(self.edit25)
        self.layoutV2.addWidget(self.qslider25)
        self.layoutV2.addWidget(self.label26)
        self.layoutV2.addWidget(self.edit26)
        self.layoutV2.addWidget(self.qslider26)
        self.layoutV2.addWidget(self.label21)
        self.layoutV2.addWidget(self.edit20)
        self.layoutV2.addWidget(self.qslider20)
        #self.layoutV2.addWidget(self.label22)
        #self.layoutV2.addWidget(self.edit22)
        #self.layoutV2.addWidget(self.label23)
        #self.layoutV2.addWidget(self.edit23)
        #self.layoutV2.addWidget(self.label24)
        #self.layoutV2.addWidget(self.edit24)
        self.layoutHgen1.addWidget(self.button23)
        self.layoutHgen1.addWidget(self.button20)
        self.layoutHgen1.addWidget(self.button21)
        #self.layoutV2.addWidget(self.button22)

        self.layoutV2.addLayout(self.layoutHgen1)
        self.button20.clicked.connect(self.start1)
        self.button21.clicked.connect(self.stop1)
        self.button22.clicked.connect(self.sweep1)
        self.button23.clicked.connect(self.setEverithing1)
        self.labelxy = QLabel("XY")
        font1 = self.font()
        font1.setPointSize(15)
        self.labelxy.setFont(font1)
        self.labelxy2 = QLabel("XY")
        self.labelcon = QLabel("Selet comport to connect to!")
        self.editcon = QLineEdit("COM5")
        self.buttonscan = QPushButton("Scan")
        self.buttoncon = QPushButton("Connect")
        self.buttonscan.clicked.connect(self.scan)
        self.buttoncon.clicked.connect(self.connect)
        self.layoutV.addWidget(self.labelcon)
        self.layoutV.addWidget(self.editcon)
        self.layoutHHcon.addWidget(self.buttonscan)
        self.layoutHHcon.addWidget(self.buttoncon)
        self.layoutV.addLayout(self.layoutHHcon)
        self.layoutH.addLayout(self.layoutV1)
        self.layoutH.addLayout(self.layoutV2)
        self.layoutV.addLayout(self.layoutH)

        self.labelspp = QLabel("Samples per period")
        #self.editspp = QLineEdit("32")
        self.buttonspp = QPushButton("Set Samples per period")
        self.labelfil = QLabel("Filter")
        self.editfil = QLineEdit("1000")

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.hist = pg.HistogramLUTItem()

        self.buttongraph = QPushButton("Save")
        self.buttongraph3 = QPushButton("Load")
        self.buttongraph4 = QPushButton("Set Filtr")
        self.buttongraph5 = QPushButton("Toggle to Square")
        self.buttongraph6 = QPushButton("Draw data")
        self.buttongraph3.setEnabled(True)
        self.buttongraph4.setEnabled(True)
        self.buttongraph5.setEnabled(True)
        self.buttongraph7 = QPushButton("Automatic Measurment")
        self.buttongraph8 = QPushButton("Save As")
        self.buttongraph9 = QPushButton("Reset")
        self.buttongraph1 = QPushButton("Continous")
        self.buttongraph2 = QPushButton("Single")

        self.buttongraph.clicked.connect(self.save)
        self.buttongraph1.clicked.connect(self.read)
        self.buttongraph2.clicked.connect(self.measure)
        self.buttongraph3.clicked.connect(self.load)
        self.buttongraph4.clicked.connect(self.draw2)
        self.buttongraph5.clicked.connect(self.toggle)
        self.buttongraph6.clicked.connect(self.plot_data)
        self.buttongraph7.clicked.connect(self.start_stop_measurment)
        self.buttongraph8.clicked.connect(self.saveFileDialog)
        self.buttongraph9.clicked.connect(self.reset)

        #self.buttonspp.clicked.connect(self.spp)
        self.sppcb = QComboBox()
        for i in range(3,11):
            self.sppcb.addItem(str(2**i))
        self.sppcb.currentIndexChanged.connect(self.spp)
        self.layoutV.addWidget(self.labelspp)
        #self.layoutV.addWidget(self.editspp)
        self.layoutV.addWidget(self.sppcb)
        #self.layoutV.addWidget(self.buttonspp)



        #self.layoutV.addWidget(self.labelfil)
        #self.layoutV.addWidget(self.editfil)
        self.layoutV.addWidget(self.labelxy)
        self.layoutV.addWidget(self.labelxy2)
        self.layoutV.addWidget(self.graphWidget)
        #self.layoutHH.addWidget(self.buttongraph)
        self.layoutHH.addWidget(self.buttongraph1)
        self.layoutHH.addWidget(self.buttongraph2)
        #self.layoutHH.addWidget(self.buttongraph3)
        #self.layoutHH.addWidget(self.buttongraph4)
        self.layoutHH.addWidget(self.buttongraph5)
        self.layoutHH.addWidget(self.buttongraph6)
        self.layoutHH.addWidget(self.buttongraph7)
        self.layoutHH.addWidget(self.buttongraph8)
        self.layoutHH.addWidget(self.buttongraph9)
        self.layoutV.addLayout(self.layoutHH)
        self.layoutV.addWidget(self.edit27)
        self.setLayout(self.layoutV)
        self.e10()
        self.e15()
        self.e16()
        self.e20()
        self.e25()
        self.e26()

# define CALL_BACK {
    def e10(self):
        if(self.edit10.text() != ""):
            a = int(self.edit10.text())
            if(0<a<=130000):
                self.qslider10.setValue( int(self.edit10.text()))
                self.sf = int(self.sample_per_periode*a)
                cct = 0.194/14.0;
                st = 1
                if(0<self.sf<=117532):
                    st = 601.5*cct
                if(117533<self.sf<=371984):
                    st = 181.5*cct
                if(371984<self.sf<=975202):
                    st =  61.5*cct
                if(975202<self.sf<=2255154):
                    st = 19.5*cct
                if(2255154<self.sf<=3608247):
                    st =  7.5*cct
                if(3608247<self.sf<=4244997):
                    st =  4.5 *cct
                if(4244997<self.sf<=4810996):
                    st =  2.5*cct
                if(4810996<self.sf<=5154639):
                    st = 1.5*cct
                self.labelspp.setText("Samples per period = {0} [-], Sampling frekquency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(int(self.sample_per_periode),self.sf,st))
            else:
                self.edit10.setText("1")

    def e15(self):
        if(self.edit15.text() != ""):
            a = int(self.edit15.text())
            if(0<a<=100):
                self.qslider15.setValue( int(self.edit15.text()))
            else:
                self.edit15.setText("1")
    def e16(self):
        if(self.edit16.text() != ""):
            a = int(self.edit16.text())
            if(0<a<=3300):
                self.qslider16.setValue( int(self.edit16.text()))
            else:
                self.edit16.setText("1")
    def e20(self):
        if(self.edit20.text() != ""):
            a = int(self.edit20.text())
            if(0<a<=130000):
                self.qslider20.setValue( int(self.edit20.text()))
            else:
                self.edit20.setText("1")

    def e25(self):
        if(self.edit25.text() != ""):
            a = int(self.edit25.text())
            if(0<a<=100):
                self.qslider25.setValue( int(self.edit25.text()))
            else:
                self.edit25.setText("1")
    def e26(self):
        if(self.edit26.text() != ""):
            a = int(self.edit26.text())
            if(0<a<=3300):
                self.qslider26.setValue( int(self.edit26.text()))
            else:
                self.edit26.setText("1")
    def qslider10update(self,value):
        self.edit10.setText(str(value))
        pass
    def qslider15update(self,value):
        self.edit15.setText(str(value))
        pass
    def qslider16update(self,value):
        self.edit16.setText(str(value))
        pass
    def qslider20update(self,value):
        self.edit20.setText(str(value))
        pass
    def qslider25update(self,value):
        self.edit25.setText(str(value))
        pass
    def qslider26update(self,value):
        self.edit26.setText(str(value))
        pass
    def scan(self):
        self.serth.scan()
        pass
    def connect(self):
        self.serth.scan()
        self.serth = SerialThread(115200, self)
        self.serth.comport = self.editcon.text()
        self.texttoupdate3 = "Connecting to " + self.serth.comport
        self.running = True
        self.serth.start()
        self.reader.serth=self.serth
        pass
    def spp(self,i):
        i=i+3
        self.serth.ser_out("SAMP\n")
        self.serth.ser_out(str(2**i)+"\n")
        self.sample_per_periode = 2**i
        self.aquaredDataX = []
        self.aquaredDataY = []
        ssp = float(2**i)
        self.sf = int(ssp*self.frek1)
        cct = 0.194/14.0;
        st = 1
        if(0<self.sf<=117532):
            st = 601.5*cct
        if(117533<self.sf<=371984):
            st = 181.5*cct
        if(371984<self.sf<=975202):
            st =  61.5*cct
        if(975202<self.sf<=2255154):
            st = 19.5*cct
        if(2255154<self.sf<=3608247):
            st =  7.5*cct
        if(3608247<self.sf<=4244997):
            st =  4.5 *cct
        if(4244997<self.sf<=4810996):
            st =  2.5*cct
        if(4810996<self.sf<=5154639):
            st = 1.5*cct
        self.labelspp.setText("Samples per period = {0} [-], Sampling frekquency = {1} [Hz], Sampling Time = {2:.3f} [us]".format(int(ssp),self.sf,st))

    def reset(self):
        self.button13.setEnabled(True)
        self.aquaredDataY = []
        self.aquaredDataX = []
        self.aquaredDataXX = []
        self.aquaredDataYY = []
        self.aquaredDataZZ = []
        self.serth.ser_out(self.edit27.text()+"\n")
    def load(self):
        try:
            with open(self.loadFileName) as file:
                self.Freq = []
                csv_reader = csv.reader(file, delimiter=',')
                for row in csv_reader:
                    self.Freq.append(float(row[0]))
        except FileNotFoundError:
            self.texttoupdate = "File Not Found Please select valid file"
            return True
        return False

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Select Frequency list in .csv format!", "","Table Files (*.csv)", options=options)
        if fileName:
            self.loadFileName=fileName
            #print(fileName)
        pass
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save as","","Table Files (*.csv)", options=options)
        if fileName:
            self.saveFileName=fileName
        #print(fileName)
        pass
        """
        self.graphWidget.clear()
        self.graphWidget.plot(range(0,len(self.aquaredDataY)), self.aquaredDataY,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
        self.graphWidget.plot(range(0,len(self.aquaredDataX)),self.aquaredDataX,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
        self.graphWidget.addLegend()
        """
    def draw2(self):
        self.serth.ser_out("FILT\n")
        self.serth.ser_out(self.editfil.text()+"\n")

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
    def update(self,data):
        self.graphWidget.plot(range(0,len(self.aquaredDataYY)), self.aquaredDataYY,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
        self.graphWidget.plot(range(0,len(self.aquaredDataXX)),self.aquaredDataXX,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
        self.graphWidget.plot(range(0,len(self.aquaredDataZZ)),self.aquaredDataZZ,pen=pg.mkPen(color=(0, 100, 255)),name='ref90')


    def toggle(self):
        if(self.sinsquaremode==False):
            self.buttongraph5.setText("Toggle to Sin")
            #self.buttongraph7.setEnabled(False)
            self.sinsquaremode = True
        else:
            self.buttongraph5.setText("Toggle to Sqare")
            self.sinsquaremode = False
            #self.buttongraph7.setEnabled(True)
        self.serth.ser_out("SINS\n")
        time.sleep(0.1)
        self.setEverithing0()



    def draw33(self,plot):
        if(self.sinsquaremode):
            self.squareCalk(plot)
        else:
            self.sinCalk(plot)


    def squareCalk(self,plot):
        self.texttoupdate2 = 'Sending data'
        if(plot):
            self.graphWidget.clear()
        a=0
        while(len(self.aquaredDataY)==0):
            time.sleep(0.2)
            a=a+1
            self.texttoupdate = 'no data '+str(a)
        self.label24.setText('LENGTH '+str(len(self.aquaredDataY)))

        my = statistics.mean(self.aquaredDataY)
        mx=0


        self.aquaredDataXX = []
        self.aquaredDataYY = []

        for i in range(0,len(self.aquaredDataY)):
            self.aquaredDataYY.append(self.aquaredDataY[i]-my)
        for i in range(0,len(self.aquaredDataX)):
            self.aquaredDataXX.append(self.aquaredDataX[i]-mx)


        del self.aquaredDataXX[0:int(self.sample_per_periode/4)]
        del self.aquaredDataYY[0:int(self.sample_per_periode/4)]
        del self.aquaredDataXX[len(self.aquaredDataXX)-self.sample_per_periode:-1]
        del self.aquaredDataYY[len(self.aquaredDataYY)-self.sample_per_periode:-1]

        self.ref = [r * (3.30/4095.0) for r in self.aquaredDataXX]
        self.dut = [d * (3.30/4095.0) for d in self.aquaredDataYY]


        del self.ref[-1]
        ref_length = len(self.ref)
        self.time_sample = ref_length / self.sf
        mx = statistics.mean(self.ref)
        a= 0
        for i in self.ref:
            if(i>mx):
                self.ref[a]=1;
            if(i<mx):
                self.ref[a]=-1;
            a=a+1


        if(plot):
            self.graphWidget.plot(range(0,len(self.dut)), self.dut,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
            self.graphWidget.plot(range(0,len(self.ref)),self.ref,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
            #vaclav.grim@fel.cvut.cz

        if(plot):
            self.graphWidget.addLegend()
        self.X=[]
        self.Y=[]
        for i in range(0,len(self.dut)):
            self.X.append(self.dut[i] * self.ref[i])
        if(len(self.X)>0):
            mX = statistics.mean(self.X)
            stdX = statistics.stdev(self.X)
            dist = int(abs(math.log10(abs(stdX))))+4
            dist2 = int(abs(math.log10(abs(mX))))+4
            dist3 = int(abs(math.log10(abs(mX/stdX))))
            dist = max(dist,dist2)
            string = "{:."+str(dist)+"f}"
            string1 = "{:."+str(dist3)+"f}"
            dist4 = int(abs(math.log10(abs(self.time_sample))))+4
            string3 = "{:."+str(dist4)+"f}"

        else:
            mX = 1
        self.aquaredData=[]
        self.aquaredDataX=[]
        self.aquaredDataY=[]
        ssttrr = string3.format(self.time_sample)
        try:
            self.texttoupdate="U\N{SUBSCRIPT TWO} = "+string.format(mX)+" V,"+" sigma ="+" "+string.format(stdX)+" V, "+"U\N{SUBSCRIPT TWO}/sigma= " + string1.format(20*math.log10(mX/stdX))+" dB\n"+ "Time duration = {0} s".format(ssttrr)
        except ValueError:
            self.texttoupdate="U\N{SUBSCRIPT TWO} = "+string.format(mX)+" V,"+" sigma ="+" "+string.format(stdX)+" V \n"+ "Time duration = {0} s".format(ssttrr)
        self.Gain.append(string.format(mX))
        #self.Phase.append(ssttrr)
        self.reader.calculated=True

    def crossings_nonzero_pos2neg(self,data):
        data = np.array(data)
        pos = data > 0
        return (pos[:-1] & ~pos[1:]).nonzero()[0]
    def crossings_nonzero_neg2pos(self,data):
        data = np.array(data)
        pos = data > 0
        return (pos[1:] & ~pos[:-1]).nonzero()[0]

    def crossings_nonzero_f(self,data):
            data = np.array(data)
            pos = data > 0
            npos = ~pos
            return ((pos[:-1] & npos[1:]) | (npos[:-1] & pos[1:])).nonzero()[0][0]
    def crossings_nonzero_l(self,data):
            data = np.array(data)
            pos = data > 0
            npos = ~pos
            return ((pos[:-1] & npos[1:]) | (npos[:-1] & pos[1:])).nonzero()[0][-1]


    def sinCalk(self,plot):
        self.texttoupdate2 = 'Sending data'
        if(plot):
            self.graphWidget.clear()
        a=0
        while(len(self.aquaredDataY)==0):
            time.sleep(0.2)
            a=a+1
            self.texttoupdate = 'no data '+str(a)
        self.label24.setText('LENGTH '+str(len(self.aquaredDataY)))
        for i in range(0,len(self.aquaredDataY)):
            if(abs(self.aquaredDataY[i])>=4096):
                self.aquaredDataY[i]=0
        for i in range(0,len(self.aquaredDataX)):
            if(abs(self.aquaredDataX[i])>=4096):
                self.aquaredDataX[i]=0
        my = statistics.mean(self.aquaredDataY)
        mx = statistics.mean(self.aquaredDataX)

        self.aquaredDataXX = []
        self.aquaredDataYY = []
        self.aquaredDataZZ = []

        for i in range(0,len(self.aquaredDataY)):
            self.aquaredDataYY.append(self.aquaredDataY[i]-my)
        for i in range(0,len(self.aquaredDataX)):
            self.aquaredDataXX.append(self.aquaredDataX[i]-mx)
            self.aquaredDataZZ.append(self.aquaredDataX[i]-mx)
        for i in range(0,int(self.sample_per_periode/4)):
            self.aquaredDataZZ.insert(0, 0)

        # remove start for angle accuacy

        del self.aquaredDataXX[0:int(self.sample_per_periode/4)]
        del self.aquaredDataYY[0:int(self.sample_per_periode/4)]
        del self.aquaredDataZZ[0:int(self.sample_per_periode/4)]
        del self.aquaredDataXX[len(self.aquaredDataXX)-self.sample_per_periode:-1]
        del self.aquaredDataYY[len(self.aquaredDataYY)-self.sample_per_periode:-1]
        del self.aquaredDataZZ[len(self.aquaredDataZZ)-int(self.sample_per_periode+self.sample_per_periode/4):-1]



        self.dut = [d * (3.30/4095) for d in self.aquaredDataYY]
        self.ref = [r * (3.30/4095) for r in self.aquaredDataXX]
        self.ref90 = [rd * (3.30/4095) for rd in self.aquaredDataZZ]


        aa = self.crossings_nonzero_pos2neg(self.ref)
        if(len(aa)<2*int(len(self.ref)/self.sample_per_periode)):
            ba = self.crossings_nonzero_neg2pos(self.ref)
            sref  = min(aa[0],ba[0])
            del self.ref[0:sref]
            del self.ref90[0:sref]
            del self.dut[0:sref]

            a = self.crossings_nonzero_pos2neg(self.ref)
            b = self.crossings_nonzero_neg2pos(self.ref)

            gofor = 0
            if (len(self.dut)>len(self.ref)):
                gofor =len(self.ref)
            if (len(self.dut)<len(self.ref)):
                gofor =len(self.dut)
            lref  = gofor
            if(aa[0]==sref):
                lref = a[-1]
            if(ba[0]==sref):
                lref = b[-1]

            del self.ref[lref:-1]
            del self.ref90[lref:-1]
            del self.dut[lref:-1]

        self.refn =  [r**2 for r in self.ref]
        mnr = math.sqrt(statistics.mean(self.refn))
        #self.texttoupdate3 = str (mnr)
        Ar = mnr
        self.refn =[r / (Ar) for r in self.ref]

        self.ref90n =  [r**2 for r in self.ref90]
        mnr90 = math.sqrt(statistics.mean(self.ref90n))
        #self.texttoupdate3 = str (mnr)
        Ar90 = mnr90
        self.ref90n =[r / (Ar90) for r in self.ref90]



        del self.ref[-1]
        del self.ref90[-1]
        ref_length = len(self.ref)
        self.time_sample = ref_length / self.sf

        if(plot):
            self.graphWidget.plot(range(0,len(self.dut)), self.dut,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
            self.graphWidget.plot(range(0,len(self.ref)),self.ref,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
            self.graphWidget.plot(range(0,len(self.ref90)),self.ref90,pen=pg.mkPen(color=(0, 100, 255)),name='ref90')


        if(plot):
            self.graphWidget.addLegend()
        self.X=[]
        self.Y=[]
        self.Xn=[]
        self.Yn=[]
        gofor = 0
        if (len(self.dut)>=len(self.ref)):
            gofor =len(self.ref)
        if (len(self.dut)<=len(self.ref)):
            gofor =len(self.dut)
        for i in range(0,gofor):
            self.X.append(self.dut[i] * self.ref[i])
            self.Xn.append(self.dut[i] * self.refn[i])
        for i in range(0,gofor):
            self.Y.append(self.dut[i] * self.ref90[i])
            self.Yn.append(self.dut[i] * self.ref90n[i])
       # self.graphWidget.plot(range(0,len(self.X)), self.X,pen=pg.mkPen(color=(255, 0, 0)),name='X')
       # self.graphWidget.plot(range(0,len(self.Y)), self.Y,pen=pg.mkPen(color=(0, 255, 0)),name='Y')
        if(len(self.X)>0):
            mX = statistics.mean(self.X)
            mY = statistics.mean(self.Y)
            mXn = statistics.mean(self.Xn)
            mYn = statistics.mean(self.Yn)
            stdX=statistics.stdev(self.Xn)
            stdY=statistics.stdev(self.Yn)
            stdX=math.sqrt((2*stdX)**2+(2*stdY)**2)
        else:
            mX,mY = 1,0
        if(plot):
            time.sleep(0.1)
            self.graphWidget.addLegend()
            time.sleep(0.1)
            self.graphWidget.addLegend()
        self.aquaredData=[]
        self.aquaredDataX=[]
        self.aquaredDataY=[]
        sa = -(180*((math.atan2( mY, mX)/math.pi)))
        dist = math.sqrt( mX**2+ mY**2)
        distn = math.sqrt( mXn**2+ mYn**2)
        if(dist>0):
            if(len(self.ref)>0):
                RRR = math.sqrt(statistics.mean([r **2 for r in self.ref]))
            else:
                RRR=1
            #self.texttoupdate3="RRR = " + str(RRR)+" dist = "  +str(dist)+" distn = "  +str(distn)
            sb = 20*math.log10((distn/RRR))
            dists = int(abs(math.log10(abs(distn))))+4
            string = "{:."+str(dists)+"f}"
            sas = int(abs(math.log10(abs(sa))))+4
            strings = "{:."+str(sas)+"f}"
            sbs = int(abs(math.log10(abs(sb))))+4
            stringbs = "{:."+str(sbs)+"f}"
            sxs = int(abs(math.log10(abs(mX))))+4
            stringxs = "{:."+str(sxs)+"f}"
            dist4 = int(abs(math.log10(abs(self.time_sample))))+4
            string3 = "{:."+str(dist4)+"f}"
            ssttrr = string3.format(self.time_sample)
            self.texttoupdate="Phase = "+strings.format(sa) +"° and  gain = "+stringbs.format(sb) +" dB,\nX: "+stringxs.format(mX)+" Y: "+stringxs.format(mY) + " U\N{SUBSCRIPT TWO} = "+string.format(dist)+" V"+ " U\N{SUBSCRIPT TWO} / U\N{SUBSCRIPT ONE} = "+string.format((distn/RRR))+" "+ "\nTime duration = {0} s".format(ssttrr)
        else:  
            self.texttoupdate="Phase = "+strings.format(sa) +"° and  gain = -Inf "+" dB X: "+stringxs.format(mX)+" Y: "+stringxs.format(mY)
        self.Gain.append(20*math.log10(dist/RRR))
        self.Phase.append(sa)
        self.reader.calculated=True




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
        self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.dut))], self.dut,pen=pg.mkPen(color=(255, 0, 0)),name='dut')
        self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.ref))],self.ref,pen=pg.mkPen(color=(0, 255, 0)),name='ref')
        #self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.refn))],self.refn,pen=pg.mkPen(color=(100, 0, 200)),name='refn')
        if(self.sinsquaremode==True):
            self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.X))],self.X,pen=pg.mkPen(color=(0, 100, 255), style=Qt.DotLine),name='U2')
        if(self.sinsquaremode==False):
            self.graphWidget.plot([x * 1/self.sf for x in range(0,len(self.ref90))],self.ref90,pen=pg.mkPen(color=(0, 100, 255)),name='ref90')
        self.graphWidget.addLegend()
        self.graphWidget.setMouseEnabled(x=True, y=True)

    def start_stop_measurment(self):
        self.graphWidget.clear()
        if(self.worker==None):
            self.worker = Worker(self,self.serth)
        self.buttongraph7.setText("Stop Measurment")
        if(self.worker.running):
            self.buttongraph7.setText("Automatic Measurment")
            self.worker.stop=True
            time.sleep(1)
            self.worker = Worker(self,self.serth)
        else:
            self.worker = Worker(self,self.serth)
            self.running = True
            self.stop = False
            self.openFileNameDialog()
            self.worker.start()
        if(self.automaticMeasurmetIsDone):
            self.automaticMeasurmetIsDone=False
            self.worker = Worker(self,self.serth)
            self.running = True
            self.stop = False
            self.worker.start()

    def draw6(self):
        self.serth.ser_out("FRQ!\n")
        self.serth.ser_out("0\n")
        self.serth.ser_out(self.edit10.text()+"\n")



    def save(self):
        if(not self.sinsquaremode):
            row_list = [["f [Hz]", "gain [dB]", "phase [°]"]]
        else:
            row_list = [["f [Hz]", "U2 [V]", "Ts [us]"]]
        for i in range(0,len(self.Gain)):
            one_row_list = [self.Freq[i],self.Gain[i],self.Phase[i]]
            row_list.append(one_row_list)
        with open(self.saveFileName, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)
        pass

    def read(self):
        if(self.reader.con_flag_stop==True):
            return
        if(self.reader.con_flag ==False):
            self.reader.con_flag=True
        else:
            self.reader.con_flag_stop=True


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
        self.reader.single_flag=True
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
        self.serth.ser_out("START\n")
        self.serth.ser_out("0\n")

    def start1(self):
        self.serth.ser_out("START\n")
        self.serth.ser_out("1\n")

    def stop0(self):
        self.serth.ser_out("STOP\n")
        self.serth.ser_out("0\n")

    def stop1(self):
        self.serth.ser_out("STOP\n")
        self.serth.ser_out("1\n")

    def sweep0(self):
        self.serth.ser_out("SWEPS\n")
        self.serth.ser_out("0\n")

    def sweep1(self):
        self.serth.ser_out("SWEPS\n")
        self.serth.ser_out("1\n")

    def setEverithing0(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.databin=False
        self.serth.a = 0
        self.serth.b = 0
        self.serth.data=[]
        self.text = []
        self.button13.setEnabled(False)
        self.serth.ser_out("FRQ!\n")
        self.serth.ser_out("0\n")
        # self.edit10.setText(self.serth.ser_out(self.edit10.text()+"\n"))
        self.serth.ser_out(self.edit10.text()+"\n")
        self.serth.ser_out("SWEP\n")
        self.serth.ser_out("0\n")
        self.serth.ser_out("D\n")
        # self.edit13.setText(self.serth.ser_out(self.edit13.text()+"\n"))
        self.serth.ser_out(self.edit13.text()+"\n")
        self.serth.ser_out("SWEP\n")
        self.serth.ser_out("0\n")
        self.serth.ser_out("U\n")
        # self.edit14.setText(self.serth.ser_out(self.edit14.text()+"\n"))
        self.serth.ser_out(self.edit14.text()+"\n")
        self.serth.ser_out("STEP\n")
        self.serth.ser_out("0\n")
        self.serth.ser_out(self.edit12.text()+"\n")
        self.serth.ser_out("AMPL\n")
        self.serth.ser_out("0\n")
        self.serth.ser_out(self.edit15.text()+"\n")
        self.serth.ser_out("OFFS\n")
        self.serth.ser_out("0\n")
        a = (int(self.edit16.text())/3300)*(2**12)
        if(a >= 4095):
            a = 4095
        if(a <= 0):
            a = 5000
        self.serth.ser_out(str(int(a))+"\n")


    def setEverithing1(self):
        self.graphWidget.setMouseEnabled(x=False, y=False)
        self.text = []
        self.serth.a = 0
        self.button23.setEnabled(False)
        self.serth.ser_out("FRQ!\n")
        self.serth.ser_out("1\n")
        # self.edit20.setText(self.serth.ser_out(self.edit20.text()+"\n"))
        self.serth.ser_out(self.edit20.text()+"\n")
        self.serth.ser_out("SWEP\n")
        self.serth.ser_out("1\n")
        self.serth.ser_out("D\n")
        # self.edit23.setText(self.serth.ser_out(self.edit23.text()+"\n"))
        self.serth.ser_out(self.edit23.text()+"\n")
        self.serth.ser_out("SWEP\n")
        self.serth.ser_out("1\n")
        self.serth.ser_out("U\n")
        # self.edit24.setText(self.serth.ser_out(self.edit24.text()+"\n"))
        self.serth.ser_out(self.edit24.text()+"\n")
        self.serth.ser_out("STEP\n")
        self.serth.ser_out("1\n")
        self.serth.ser_out(self.edit22.text()+"\n")
        self.serth.ser_out("AMPL\n")
        self.serth.ser_out("1\n")
        self.serth.ser_out(self.edit25.text()+"\n")
        self.serth.ser_out("OFFS\n")
        self.serth.ser_out("1\n")
        a = (int(self.edit26.text())/3300)*(2**12)
        if(a <= 0):
            a = 1
        if(a >= 4095):
            a = 4095
        self.serth.ser_out(str(int(a))+"\n")
# define CALL_BACK }
    def textupdate(self):
        try:
            self.labelxy.setText(self.texttoupdate)
            self.labelxy2.setText(self.texttoupdate2)
            self.labelcon.setText(self.texttoupdate3)
        except RuntimeError:
            pass



    def __init__(self, parent=None):
        self.serth = SerialThread(115200, self)   # Start serial thread
        self.serth.start()
        self.rrr = False
          # Start worker thread
        self.reader = Reader(self,self.serth)   # Start reading thread
        self.reader.start()

        super(Form, self).__init__(parent)
        self.make_gui()
        #self.setFixedSize(700,700)


if __name__ == "__main__":
    app = QApplication([])
    window = Form()
    window.show()
    sys.exit(app.exec_())
