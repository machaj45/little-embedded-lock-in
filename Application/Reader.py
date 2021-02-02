#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
import time


class Reader(QtCore.QThread):

    def __init__(self, gui, serth):  # Initialise with serial port details
        QtCore.QThread.__init__(self)
        self.running = True
        self.stop = False
        self.gui = gui
        self.serth = serth
        self.counter = 0
        self.dataporbe = 0
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
        self.nextMeasurment = True
        self.con_init = True
        self.calculated = False
    def reading(self):
        self.gui.texttoupdate2 = 'Reading number ' + str(self.dataporbe)
        self.dataporbe = self.dataporbe + 1
        self.serth.ser_out('DATA\n')

    def single(self):
        if(self.single_flag):
            self.single_flag=False
            self.single_running =True
            self.serth.data=[]
            self.serth.ser_out("MEAS\n")
            self.gui.aquaredData=[]
            self.serth.notread = 0
            self.gui.sf = self.gui.sample_per_periode*self.gui.frek1
            self.time_sample = 10000 / self.gui.sf
            self.time_single = 0
        if(self.single_running):
            self.time_single = self.time_single+0.1
            if(self.time_sample>10 and self.single_running):
                self.gui.texttoupdate2="Time elapsed {0:.2f} s, Time for sampling = {1:.2f} s".format(float(self.time_single),float(self.time_sample))
            if(self.time_single>= self.time_sample+self.time_sample*0.2+0.5):
                self.serth.ser_out('DATA\n')
                self.single_running = False
            self.calculated = False
    def con(self):
        if(self.con_flag):
            if(self.con_init):
                self.con_running =True
                self.gui.sf = self.gui.sample_per_periode*self.gui.frek1
                self.time_sample = 10000 / self.gui.sf
                if(self.time_sample<=1):
                    self.time_sample=1
                self.time_con = 0
                self.con_init =False
                self.calculated = True
            if(self.nextMeasurment and self.calculated):
                if(self.con_flag_stop ==True):
                    self.con_flag = False
                    self.gui.texttoupdate2="con end"
                    self.con_flag_stop=False
                    return
                self.calculated = False
                self.serth.data=[]
                self.time_con = 0
                self.serth.ser_out("MEAS\n")
                self.gui.aquaredData=[]
                self.serth.notread = 0
                self.nextMeasurment=False
            if(self.con_running):
                self.time_con = self.time_con+0.1
                if(self.time_sample>10 and not self.nextMeasurment):
                    self.gui.texttoupdate2="Time elapsed {0:.2f} s, Time for sampling = {1} s".format(float(self.time_con),str(self.time_sample))
                if(self.time_con>= self.time_sample+self.time_sample*0.2):
                    self.serth.ser_out('DATA\n')
                    self.time_con = 0
                    self.nextMeasurment=True
            if(self.nextMeasurment and not self.calculated):
                self.time_con = 0
        else:
           self.con_init =True
           self.con_running = False

    def run(self):
        self.stop = False
        self.counter = 0
        self.dataporbe = 0
        while True:
            time.sleep(0.01)
            self.counter = self.counter + 1
            if self.counter % 5 == 0:
                self.gui.textupdate()
            if self.counter % 50 == 0 and self.read:
                self.reading()
            if self.counter % 10 == 0:
                self.single()
                self.con()
            if self.counter >=1000000:
                self.counter=0

