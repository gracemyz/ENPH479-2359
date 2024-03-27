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
from plottime import TimeGraph, TimeView, PORT
from plotfreq import FFTView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Heart-rate monitoring')

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        # Set up the layout
        self.mdi_area = QMdiArea(main_widget)
        self.init_ui()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.mdi_area)

    
    def init_ui(self):
        # self.create_menu_bar()
        self.options_view = UserOptions(parent=self)
        self.time_view = TimeView(parent=self)
        self.fft_view = FFTView(parent=self)

        self.options_view.start_plots.connect(self.time_view.start_plots)
        self.options_view.reset_plots.connect(self.time_view.reset_plots)

        options_window = QMdiSubWindow()
        options_window.setWidget(self.options_view)
        options_window.setWindowTitle("Details")
        

        time_window = QMdiSubWindow()
        time_window.setWidget(self.time_view)
        time_window.setWindowTitle("Time view")

        fft_window = QMdiSubWindow()
        fft_window.setWidget(self.fft_view)
        fft_window.setWindowTitle("Frequency view")

        for w in [options_window, time_window, fft_window]:
            self.mdi_area.addSubWindow(w)    
        # self.mdi_area.tileSubWindows()
        
        height = 950
        optionswidth = 400
        timewidth = 1000
        freqwidth = 500
        self.mdi_area.subWindowList()[0].setGeometry(0, 0, optionswidth, height)
        self.mdi_area.subWindowList()[1].setGeometry(optionswidth, 0, timewidth, height)
        self.mdi_area.subWindowList()[2].setGeometry(optionswidth+timewidth, 0, freqwidth, height)
        
        self.showMaximized()





    
