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


class SerialDataReader(threading.Thread):
    def __init__(self, serial_port, x_queue, y_queue, xs, ys, stop_event, num_samples):
        super().__init__()
        self.serial_port = serial_port
        self.ys = ys
        self.xs = xs
        self.x_queue = x_queue
        self.y_queue = y_queue
        self.stop_event = stop_event
        self.num_samples = num_samples

    def run(self):
        x = 0.0
        # with serial.Serial(self.serial_port, 9600) as ser:
        while not self.stop_event.is_set():
            # line = ser.readline().strip().decode()/

            try:
                # data = float(line)
                if len(self.xs) > self.num_samples:
                    self.stop_event.set()
                new_x = x
                new_y = 16 * np.sin(2 * np.pi * new_x ) + 10 * np.sin(0.1 * np.pi * new_x ) + 5 * random.random()

                self.x_queue.append(new_x)
                self.xs.append(new_x)
                self.y_queue.append(new_y)
                self.ys.append(new_y)
                x += 0.02
                time.sleep(0.02)
                # logging.warning(str(new_x) + ", " + str(new_y))
            except ValueError:
                pass
        
    def stop(self):
        self.stop_event.set()
        self.join()
    