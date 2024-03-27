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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("This is where the fft chart will go"))

        # Create the main horizontal layout for left and right layouts
        bottomwidget = QWidget()
        main_horizontal_layout = QHBoxLayout()
        
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        right_widget.setFixedSize(400, 100)

        self.specify_range_button = QPushButton("Specify range")
        self.specify_range_button.toggled.connect(self.on_pb_toggled)
        right_layout.addWidget(self.specify_range_button)
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
        main_horizontal_layout.addWidget(right_widget)

        # Add the main horizontal layout to the main layout
        bottomwidget.setLayout(main_horizontal_layout)
        bottomwidget.setMaximumHeight(150)
        self.layout.addWidget(bottomwidget)


        self.setLayout(self.layout)

    def on_pb_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            print(f"Selected option: {sender.text()}")



    def update_plot(self):
        pass
        
    
