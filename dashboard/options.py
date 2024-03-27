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

class UserOptions(QWidget):
    pause_plots = pyqtSignal(bool)
    start_plots = pyqtSignal(int)
    reset_plots = pyqtSignal()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = QVBoxLayout()

        layout = QVBoxLayout()
        topwidget = QWidget()
        topwidget.setLayout(layout)

        subjectlabel = QLabel("Subject:")
        layout.addWidget(subjectlabel)
        self.subjectlineedit = QLineEdit("CM / GZ / JD / CA ...")
        layout.addWidget(self.subjectlineedit)
        
        boardlabel = QLabel("Board:")
        layout.addWidget(boardlabel)
        self.boardlineedit = QLineEdit("Eval board / LED-PD board")
        layout.addWidget(self.boardlineedit)
        
        seplabel = QLabel("Separation distance:")
        layout.addWidget(seplabel)
        self.seplineedit = QLineEdit("")
        layout.addWidget(self.seplineedit)

        gain_label = QLabel("Gain:")
        layout.addWidget(gain_label)
        self.gain_line_edit = QLineEdit("100kO / 200kO...")
        layout.addWidget(self.gain_line_edit)
        
        # Add QLabel and QLineEdit for Pulse Width
        pulse_width_label = QLabel("Pulse Width:")
        layout.addWidget(pulse_width_label)
        self.pulse_width_line_edit = QLineEdit("2 us / 3 us")
        layout.addWidget(self.pulse_width_line_edit)
        
        # Add QLabel and QLineEdit for Integration Mode
        int_mode_label = QLabel("Integration Mode:")
        layout.addWidget(int_mode_label)
        self.int_mode_line_edit = QLineEdit("single / 2 / 3...")
        layout.addWidget(self.int_mode_line_edit)
        
        # Add QLabel and QLineEdit for Current
        current_label = QLabel("Current:")
        layout.addWidget(current_label)
        self.current_line_edit = QLineEdit("x mA")
        layout.addWidget(self.current_line_edit)
        
        # Add QLabel and QTextEdit for Notes
        notes_label = QLabel("Notes:")
        layout.addWidget(notes_label)
        self.notes_line_edit = QLineEdit("")
        layout.addWidget(self.notes_line_edit)
        
        length_label = QLabel("Length (s):")
        layout.addWidget(length_label)
        self.length_line_edit = QLineEdit("60")
        layout.addWidget(self.length_line_edit)

        bottomwidget = QWidget()
        plot_options_layout = QHBoxLayout()
        bottomwidget.setLayout(plot_options_layout)
        
        self.plotPB = QPushButton("Plot", self)
        plot_options_layout.addWidget(self.plotPB)
        # self.pauseCB = QCheckBox("Pause plots", self)
        # plot_options_layout.addWidget(self.pauseCB)
        self.resetPB = QPushButton("Reset plots", self)
        plot_options_layout.addWidget(self.resetPB)

        # Set layout
        main_layout.addWidget(topwidget)
        main_layout.addWidget(bottomwidget)
        self.setLayout(main_layout)

        self.plotPB.clicked.connect(self.on_plot_click)
        # self.pauseCB.stateChanged.connect(self.on_pause_state_changed)
        self.resetPB.clicked.connect(self.on_reset_click)
    
    def on_reset_click(self):
        self.plotPB.setEnabled(True)
        self.resetPB.setEnabled(False)
        self.reset_plots.emit()

    def on_plot_click(self):
        self.plotPB.setEnabled(False)
        self.resetPB.setEnabled(True)
        self.start_plots.emit(int(self.length_line_edit.text()))

    def on_pause_state_changed(self, state):
        self.pause_plots.emit(state)