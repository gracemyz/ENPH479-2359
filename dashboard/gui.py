import sys
import random
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,  QLabel, QLineEdit, QRadioButton, QMdiArea, QMdiSubWindow, QPushButton, QCheckBox, QSpacerItem, QSizePolicy
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
    def __init__(self, app):
        super().__init__()
        self.app = app
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

        self.options_view.start_plots.connect(self.fft_view.start_plots)
        self.options_view.reset_plots.connect(self.fft_view.reset_plots)

        self.options_view.start_from_file.connect(self.time_view.start_from_file)
        self.options_view.start_from_file.connect(self.fft_view.start_from_file)

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
        
        options_fraction = 0.18  # 20% of screen width
        time_fraction = 0.5     # 50% of screen width
        freq_fraction = 0.3     # 30% of screen width

        # Calculate widths based on fractions
        screen_geometry = self.app.desktop().screenGeometry()

        options_width = int(screen_geometry.width() * options_fraction)
        time_width = int(screen_geometry.width() * time_fraction)
        freq_width = int(screen_geometry.width() * freq_fraction)
        height = int(0.8*screen_geometry.height())

        # Set the geometry of subwindows
        self.mdi_area.subWindowList()[0].setGeometry(0, 0, options_width, height)
        self.mdi_area.subWindowList()[1].setGeometry(options_width, 0, time_width, height)
        self.mdi_area.subWindowList()[2].setGeometry(options_width + time_width, 0, freq_width, height)
        
        self.showMaximized()


    
