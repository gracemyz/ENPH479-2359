import sys
import random
import logging
from PyQt5.QtGui import QFont, QColor

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsTextItem, QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,  QLabel, QLineEdit, QRadioButton, QMdiArea, QMdiSubWindow, QPushButton, QCheckBox, QSpacerItem, QSizePolicy
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

        self.show_breakout = QPushButton("Break out frequencies")
        self.show_breakout.clicked.connect(self.on_pb_toggled)
        right_layout.addWidget(self.show_breakout)
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
        self.breakoutview = FreqBreakoutView(self.xs, self.ys, parent=self)
        self.breakoutview.showMaximized()

        
    
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

    def start_from_file(self, filename):
        self.xs = self.parent.time_view.xs
        self.ys = self.parent.time_view.ys
        self.graph.plot_fft(self.xs, self.ys)
        xmin, xmax, ymin, ymax = self.getRange()
        self.graph.plotItem.setLimits(xMin=xmin, xMax=xmax, yMin=ymin, yMax=ymax)
        
        
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

        self.peaks = []
        self.text = QGraphicsTextItem(parent=self.plotItem)
        self.text.setPos(180, 180)  # Adjust position as needed
        self.text.setDefaultTextColor(QColor('white'))  # Set text color
        self.text.setFont(QFont('Courier', 10))  # Set font for the text
        self.plotItem.showGrid(True, True)
    
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

                self.freqs_positive = freqs[:num_samples//2]
                ys_positive = 2.0/num_samples * np.abs(ys[:num_samples//2])
                self.plotDataItem.setData(self.freqs_positive, ys_positive)
                
                # Update metrics
                to_disp = self.find_peaks(self.freqs_positive, ys_positive)
                
                self.text.setPlainText(to_disp)
                    
                


    def find_peaks(self, freqs_positive, ys_positive):
        lower_freq_limit = 0.5  # Lower frequency limit
        upper_freq_limit = 2.5  # Upper frequency limit
        DCval = ys_positive[0]

        indices = np.where((freqs_positive >= lower_freq_limit) & (freqs_positive <= upper_freq_limit))
        try:
            max_index = np.argmax(ys_positive[indices])
            HRval, HRamp = freqs_positive[indices][max_index],np.max(ys_positive[indices])
            DCval = ys_positive[0]
            PI = HRamp / DCval
            to_disp = ""
            to_disp = to_disp + "DC amplitude: " + str(round(DCval)) + "\n"
            
            to_disp = to_disp + "HR amplitude: " + str(round(HRamp)) + " @ " + str(round(HRval*60.0)) + " bpm" + "\n"
            to_disp = to_disp + "          PI: " + str(round(PI, 5))
            return to_disp
        except:
            logging.warning("no peaks found")

            


    def timerEvent(self, event):
        xs = self.parent.xs
        ys = self.parent.ys
        self.plot_fft(xs, ys)
    
class FreqBreakoutView(QWidget):
    def __init__(self, xs, ys, parent,**kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.xs = xs
        self.ys = ys
        self.graph = FreqBreakoutGraph(parent=self)
        # self.timegraph = TimeGraph(parent=self)
        self.layout.addWidget(self.graph)

        
class FreqBreakoutGraph(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent) 
        self.parent = parent

        nptime = parent.xs
        npdata = parent.ys
        period = 0.01988
        ys = np.fft.fft(npdata)
        N = len(ys)
        freqs = np.fft.fftfreq(N, d=period)


        self.freqs_positive = freqs[:N//2]
        ys_positive = 2.0/N * np.abs(ys[:N//2])
        self.plot_item = self.addPlot(title="Delimited PPG data")
        

        freq_min_breathing = 0.16  # Minimum frequency in Hz
        freq_max_breathing = 0.5  # Maximum frequency in Hz
        filter_mask_breathing = np.logical_and(freqs >= freq_min_breathing, freqs <= freq_max_breathing)

        # Apply the filter to the FFT result
        filtered_fft_breathing = ys * filter_mask_breathing

        # Perform the inverse FFT to obtain the filtered signal
        filtered_signal_breathing = abs(np.fft.ifft(filtered_fft_breathing))

        freq_min_HR = 0.5  # Minimum frequency in Hz
        freq_max_HR = 3.75  # Maximum frequency in Hz
        filter_mask_HR = np.logical_and(freqs >= freq_min_HR, freqs <= freq_max_HR)

        # Apply the filter to the FFT result
        self.filtered_fft_HR = ys * filter_mask_HR

        # Perform the inverse FFT to obtain the filtered signal
        filtered_signal_HR = abs(np.fft.ifft(self.filtered_fft_HR))

        freq_min_1 = 0.33  # Minimum frequency for the first range
        freq_max_1 = 0.33   # Maximum frequency for the first range
        freq_min_2 = 3.75   # Minimum frequency for the second range
        filter_mask_noise = np.logical_or(np.logical_and(freqs >= freq_min_1, freqs <= freq_max_1),
                                    freqs >= freq_min_2)

        # Apply the filter to the FFT result
        self.filtered_fft_noise = ys * filter_mask_noise

        # Perform the inverse FFT to obtain the filtered signal
        filtered_signal_noise = abs(np.fft.ifft(self.filtered_fft_noise))

        # Plot the data
        time = np.linspace(nptime[0], nptime[-1], len(filtered_signal_breathing))

        snr = self.get_SNR(N)

        self.plot_item.plot(time, filtered_signal_breathing, pen = 'r', name='Respiration')
        self.plot_item.plot(time, filtered_signal_HR, pen='g', name='Heart rate')
        self.plot_item.plot(time, filtered_signal_noise, pen='b', name='Noise')
        self.plot_item.addLegend(size=(10,10),offset=(10, 10), parent=self.plot_item)

        self.text = QGraphicsTextItem(snr, parent=self.plot_item)
        self.text.setPos(180, 180)  # Adjust position as needed
        self.text.setDefaultTextColor(QColor('white'))  # Set text color
        self.text.setFont(QFont('Courier', 50))  # Set font for the text


        # Add legend


        # Set labels, title, and other properties
        self.plot_item.setLabel('bottom', text='Time (s)')
        self.plot_item.setLabel('left', text='ADC output')
        self.plot_item.setTitle("Raw PPG Data in frequency bands delimited at 0.5Hz and 3.75Hz")
        # self.plot_item.setLimits(xMin=690, xMax=710, yMin=-100, yMax=130)
        self.plot_item.showGrid(True, True)

    
    def get_SNR(self, N):
        filtered_fft_noise_positive = 2.0/N * np.abs(self.filtered_fft_noise[:N//2])
        filtered_fft_HR_positive = 2.0/N * np.abs(self.filtered_fft_HR[:N//2])
        SNR = 10 * np.log10(np.trapz(filtered_fft_HR_positive,self.freqs_positive)/np.trapz(filtered_fft_noise_positive,self.freqs_positive))
        return "SNR: " + str(round(SNR, 5))
