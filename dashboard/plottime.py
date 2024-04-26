import sys, csv
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

PORT = 'COM3'

class FullTimeView(QWidget):
    def __init__(self, xs, ys, parent,**kwargs):
        super().__init__(**kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.xs = xs
        self.ys = ys
        self.lims = [parent.x_min_edit.text(),
                     parent.x_max_edit.text(),
                     parent.y_min_edit.text(),
                     parent.y_max_edit.text()]
        for i in range(4):
            if len(self.lims[i]) == 0:
                self.lims[i] = None
            else:
                self.lims[i] = int(self.lims[i])
        # logging.warning(self.lims)
        self.timegraph = FullTimeGraph(parent=self)
        # self.timegraph = TimeGraph(parent=self)
        self.layout.addWidget(self.timegraph)


class TimeView(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.timegraph = TimeGraph(parent=self)
        # self.timegraph = TimeGraph(parent=self)
        self.layout.addWidget(self.timegraph)

        # Create the main horizontal layout for left and right layouts
        bottomwidget = QWidget()
        main_horizontal_layout = QHBoxLayout()
        

        # Create the left layout for "Moving plot" radio button
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_widget.setFixedSize(400, 100)
        # self.moving_plot_button = QPushButton("Moving plot")
        window_label = QLabel("Specify window length (s)")
        self.window_line_edit = QLineEdit("10")
        # left_layout.addWidget(self.moving_plot_button)
        left_layout.addWidget(window_label)
        left_layout.addWidget(self.window_line_edit)
        left_layout.addStretch(1) 

        # Create the right layout for "Full plot" radio button and QLineEdits
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        right_widget.setFixedSize(400, 100)
        self.specify_range_button = QPushButton("Show full plot")
        right_layout.addWidget(self.specify_range_button)
        right_layout.addStretch(1)

        # Add QLineEdits
        self.x_min_edit = QLineEdit()
        self.x_max_edit = QLineEdit()
        self.y_max_edit = QLineEdit()
        self.y_min_edit = QLineEdit()

        xlayout = QHBoxLayout()
        ylayout = QHBoxLayout()
        xlayout.addWidget(QLabel("x min, x max"))
        xlayout.addWidget(self.x_min_edit)
        xlayout.addWidget(self.x_max_edit)
        ylayout.addWidget(QLabel("y min, y max"))
        ylayout.addWidget(self.y_max_edit)
        ylayout.addWidget(self.y_min_edit)

        right_layout.addLayout(xlayout)
        right_layout.addLayout(ylayout)
        # Add left and right layouts to the main horizontal layout
        main_horizontal_layout.addWidget(left_widget)
        main_horizontal_layout.addWidget(right_widget)

        # Add the main horizontal layout to the main layout
        bottomwidget.setLayout(main_horizontal_layout)
        bottomwidget.setMaximumHeight(150)
        self.layout.addWidget(bottomwidget)

        # Connect signals to slots
        # self.moving_plot_button.toggled.connect(self.on_pb_toggled)
        self.specify_range_button.clicked.connect(self.on_pb_toggled)


    def replace_graph(self):

        new_widget = TimeGraph(parent=self)
        to_replace = self.layout.itemAt(0).widget()
        self.layout.insertWidget(0, new_widget)
        to_replace.deleteLater()
        self.timegraph = new_widget

    def pop_up_full(self):
        self.fulltimeview = FullTimeView(self.xs, self.ys, parent=self)
        self.fulltimeview.showMaximized()


    def on_pb_toggled(self):
        logging.warning("toggled")
        self.pop_up_full()

    def reset_plots(self):
        if hasattr(self, "serial_reader"):
            self.serial_reader.stop()
        # self.timegraph.killTimer(self.timegraph.timer_id) 
        self.replace_graph()
        self.xs = []
        self.ys = []


    def start_from_file(self, path):
        time = []
        data = []
        # path = "20240406_2ledpd_thinbaffle_currentsweep\\20240406_2ledpd_thinbaffle_2mA_100kO_2uspulsewidth.csv"
        # path = "..\\data\\20240324\\20240324_100kO_10mA_noBC_finger_neweval.csv"

        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            
            next(csv_reader) # skip first row
            next(csv_reader) # skip first row
            next(csv_reader) # skip first row
            for row in csv_reader:
                # Process each row
                time.append(float(row[0]))
                data.append(float(row[1]))
                # logging.warning(row)
        file.close()
        
        self.num_samples = len(time)
        self.xs = time
        self.ys = data
        self.timegraph.plotDataItem.setData(self.xs ,self.ys)

    def start_plots(self, total_s=60, sample_rate=50, plot_update_rate=100):
        logging.warning("Init time plot")

        # self.timegraph = TimeGraph(parent=self)
        self.total_s = total_s
        window_len = int(self.window_line_edit.text()) * sample_rate
        self.num_samples = total_s * sample_rate
        self.x_queue, self.y_queue = deque(maxlen=window_len), deque(maxlen=window_len)  # Buffer for incoming data
        self.xs, self.ys = [], []
        self.stop_event = threading.Event()
        self.serial_reader = SerialDataReader(PORT, self.x_queue, self.y_queue, self.xs, self.ys, self.stop_event, self.num_samples, 1)
        self.serial_reader.start()
        self.timegraph.start(plot_update_rate)


class TimeGraph(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.plotItem = self.addPlot(title="ADC output vs time")
        pen = pg.mkPen(color=(0, 255, 255), width=1)  # Blue pen with width 2

        # Create the plotDataItem with the specified pen
        self.plotDataItem = self.plotItem.plot([], pen=pen, 
                                            symbolBrush=(0, 255, 255), 
                                            symbolSize=2, 
                                            symbolPen=None)
        self.plotItem.showGrid(True, True)
    
    def start(self, plot_update_rate):
        self.timer_id = self.startTimer(plot_update_rate) # number of seconds

    def clear(self):
        pass
        # self.plotItem.clear()
    
    def timerEvent(self, event):
        xs = list(self.parent().x_queue)
        ys = list(self.parent().y_queue)
        self.plotDataItem.setData(xs, ys)
        


class FullTimeGraph(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent) 
        lims = parent.lims

        self.plotItem = self.addPlot(title="ADC output vs time")
        self.set_limits(lims)
        pen = pg.mkPen(color=(0, 255, 255), width=1)  # Blue pen with width 2

        # Create the plotDataItem with the specified pen
        self.plotDataItem = self.plotItem.plot([], pen=pen, 
                                            symbolBrush=(0, 255, 255), 
                                            symbolSize=2, 
                                            symbolPen=None)
        xs = list(parent.xs)
        ys = list(parent.ys)
        self.plotDataItem.setData(xs, ys)
        self.plotItem.showGrid(True, True)
        
        

    def set_limits(self, lims):
        self.plotItem.setLimits(xMin=lims[0], xMax=lims[1], yMin=lims[2], yMax=lims[3])