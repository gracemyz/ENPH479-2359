import sys
import random
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,  QLabel, QLineEdit, QRadioButton, QMdiArea, QMdiSubWindow, QPushButton, QCheckBox, QSpacerItem, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from collections import deque
import serial
import time
from PyQt5.QtCore import Qt, pyqtSignal
import threading
import pyqtgraph as pg
import numpy as np
import csv


class SerialDataReader(threading.Thread):
    
    def __init__(self, serial_port, x_queue, y_queue, xs, ys, stop_event, num_samples, num=0):
        super().__init__()
        self.serial_port = serial_port
        self.ys = ys
        self.xs = xs
        self.x_queue = x_queue
        self.y_queue = y_queue
        self.stop_event = stop_event
        self.num_samples = num_samples

        self.num = num
        if self.num == 0:
            self.fakex, self.fakey = self.fake_it()
        else:
            
            self.ser = serial.Serial("COM3", 9600)
            



    def run(self):
        x = 0.0
        # with serial.Serial(self.serial_port, 9600) as ser:
        i = 0

        while not self.stop_event.is_set():
            # line = ser.readline().strip().decode()/
            
            
            try:
                if self.num == 0:
                    
                    # data = float(line)
                    if len(self.xs) > self.num_samples or i+1 >= len(self.fakex):
                        self.stop_event.set()
                    # new_x = x
                    
                        
                    new_x = 0.02 * float(i)
                    # new_y = 16 * np.sin(2 * np.pi * new_x ) + 8 * np.sin(6 * np.pi * new_x ) + 3 * random.random()
                    new_y = float(self.fakey[i])
                    i += 1

                    self.x_queue.append(new_x)
                    self.xs.append(new_x)
                    self.y_queue.append(new_y)
                    self.ys.append(new_y)
                    time.sleep(0.02)
                else:
                    if len(self.xs) > self.num_samples:
                        self.stop_event.set()   
                    try:
                        getData=self.ser.readline()
                        readings = getData.decode('utf-8').strip().split(",")
                        logging.warning(readings)
                        new_x, new_y = float(readings[0]), float(readings[1])
                        
                        self.x_queue.append(new_x)
                        self.xs.append(new_x)
                        self.y_queue.append(new_y)
                        self.ys.append(new_y)
                    except:
                        logging.warning("skip a line")
                        pass
                    
                
                # logging.warning(str(new_x) + ", " + str(self.fakey[i]))
            except ValueError:
                pass


        
    def stop(self):
        if self.num == 1:
            self.ser.close()
        self.stop_event.set()
        self.join()

    def fake_it(self):
        time = []
        data = []
        path = "..\\data\\20240324\\20240324_100kO_10mA_noBC_finger_neweval.csv"

        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            
            next(csv_reader) # skip first row
            for row in csv_reader:
                # Process each row
                time.append(row[0])
                data.append(row[1])
        file.close()
        return time[500:], data[500:]
        
    