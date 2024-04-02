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
from options import UserOptions
from serialreader import SerialDataReader

class FFTView(QWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.layout = QVBoxLayout()
        self.parent = parent
        self.graph = FreqGraph(parent=self)
        self.layout.addWidget(self.graph)

        # Create the main horizontal layout for left and right layouts
        bottomwidget = QWidget()
        main_horizontal_layout = QHBoxLayout()
        
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        right_widget.setFixedSize(400, 100)

        self.specify_range_button = QPushButton("Specify range")
        self.specify_range_button.clicked.connect(self.on_pb_toggled)
        right_layout.addWidget(self.specify_range_button)
        self.x_min_edit = QLineEdit("0")
        self.x_max_edit = QLineEdit("5")
        self.y_max_edit = QLineEdit("100")
        self.y_min_edit = QLineEdit("0")

        xlayout = QHBoxLayout()
        ylayout = QHBoxLayout()
        xlayout.addWidget(QLabel("x min, x max"))
        xlayout.addWidget(self.x_min_edit)
        xlayout.addWidget(self.x_max_edit)
        ylayout.addWidget(QLabel("y min, y max"))
        ylayout.addWidget(self.y_min_edit)
        ylayout.addWidget(self.y_max_edit)

        right_layout.addLayout(xlayout)
        right_layout.addLayout(ylayout)
        # Add left and right layouts to the main horizontal layout
        main_horizontal_layout.addWidget(right_widget)

        # Add the main horizontal layout to the main layout
        bottomwidget.setLayout(main_horizontal_layout)
        bottomwidget.setMaximumHeight(150)
        self.layout.addWidget(bottomwidget)


        self.setLayout(self.layout)

    def on_pb_toggled(self):

        self.reset_plots()
    
    def getRange(self):
        xmin, xmax, ymin, ymax = None, None, None, None
        if self.x_min_edit.text() != "":
            xmin = int(self.x_min_edit.text())

        if self.x_max_edit.text() != "":
            xmax = int(self.x_max_edit.text())

        if self.y_min_edit.text() != "":
            ymin = int(self.y_min_edit.text())

        if self.y_max_edit.text() != "":
            ymax = int(self.y_max_edit.text())
        return xmin, xmax, ymin, ymax

    def replace_graph(self):

        new_widget = FreqGraph(parent=self)
        to_replace = self.layout.itemAt(0).widget()
        self.layout.insertWidget(0, new_widget)
        to_replace.deleteLater()
        self.graph = new_widget


    def reset_plots(self):
        self.replace_graph()
        xmin, xmax, ymin, ymax = self.getRange()
 
        self.graph.setRange(xmin, xmax, ymin, ymax)


    def start_plots(self, total_s=60, sample_rate=50, plot_update_rate=100):
        self.xs = self.parent.time_view.xs
        self.ys = self.parent.time_view.ys



        # self.timegraph = TimeGraph(parent=self)
        self.total_s = total_s
        self.num_samples = total_s * sample_rate
        xmin, xmax, ymin, ymax = self.getRange()
        self.graph.start(plot_update_rate, xmin, xmax, ymin, ymax)
        
        
# TODO Repetitive... should probably subclass with TimeGraph
class FreqGraph(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent=parent
        self.plotItem = self.addPlot(title="FFT")

        pen = pg.mkPen(color=(0, 255, 255), width=1)  # Blue pen with width 2

        # Create the plotDataItem with the specified pen
        self.plotDataItem = self.plotItem.plot([], pen=pen, 
                                            symbolBrush=(0, 255, 255), 
                                            symbolSize=2, 
                                            symbolPen=None)
    
    def start(self, plot_update_rate, xmin, xmax, ymin, ymax):
        self.timer_id = self.startTimer(plot_update_rate) # number of seconds
        self.setRange(xmin, xmax, ymin, ymax)
    
    def setRange(self, xmin, xmax, ymin, ymax):
        self.plotItem.setLimits(xMin=xmin, xMax=xmax, yMin=ymin, yMax=ymax)


    def clear(self):
        pass
        # self.plotItem.clear()


    def plot_fft(self, xs, ys):

        if len(ys) < 2:
            logging.warning("too few to plot")
            pass
        else:
            ys = np.fft.fft(ys)
            num_samples = len(ys)
            sample_spacing = (xs[num_samples-1] - xs[num_samples-2])
            if num_samples < 2 or sample_spacing == 0:
                pass
            else:
                
                freqs = np.fft.fftfreq(num_samples, sample_spacing)

                freqs_positive = freqs[1:num_samples//2]
                ys_positive = 2.0/num_samples * np.abs(ys[1:num_samples//2])
                self.plotDataItem.setData(freqs_positive, ys_positive)

        # # Create a low-pass filter
        # cutoff_freq = 5  # Cutoff frequency in Hz
        # filter_mask = np.abs(freqs) <= cutoff_freq

        # # Apply the filter to the FFT result
        # filtered_fft = ys * filter_mask

        # # Perform the inverse FFT to obtain the filtered signal
        # filtered_signal = np.fft.ifft(filtered_fft)



            


    def timerEvent(self, event):
        xs = self.parent.xs
        ys = self.parent.ys
        self.plot_fft(xs, ys)
        
