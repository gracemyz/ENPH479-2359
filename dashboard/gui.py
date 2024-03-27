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

PORT = 'COM3'

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


class TimeView(QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('ADC output (bits)')
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Create the main horizontal layout for left and right layouts
        bottomwidget = QWidget()
        main_horizontal_layout = QHBoxLayout()
        

        # Create the left layout for "Moving plot" radio button
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        left_widget.setFixedSize(400, 100)
        self.moving_plot_button = QPushButton("Moving plot")
        left_layout.addWidget(self.moving_plot_button)
        left_layout.addStretch(1) 

        # Create the right layout for "Full plot" radio button and QLineEdits
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        right_widget.setFixedSize(400, 100)
        self.specify_range_button = QPushButton("Specify range")
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
        self.moving_plot_button.toggled.connect(self.on_pb_toggled)
        self.specify_range_button.toggled.connect(self.on_pb_toggled)

    def on_pb_toggled(self):
        sender = self.sender()
        if sender.isChecked():
            print(f"Selected option: {sender.text()}")

    def reset_plots(self):
        self.serial_reader.stop()
        self.killTimer(self.timer_id) 

    def start_plots(self, total_s=60, window_s=15, sample_rate=50, plot_update_rate=1000):
        self.total_s = total_s
        window_len = window_s * sample_rate
        self.num_samples = total_s * sample_rate
        self.x_queue, self.y_queue = deque(maxlen=window_len), deque(maxlen=window_len)  # Buffer for incoming data
        self.xs, self.ys = [], []
        self.stop_event = threading.Event()
        self.serial_reader = SerialDataReader(PORT, self.x_queue, self.y_queue, self.xs, self.ys, self.stop_event, self.num_samples)
        self.serial_reader.start()
        self.timer_id = self.startTimer(plot_update_rate) # number of seconds


    def timerEvent(self, event):
        # Generate random data for the plot
        self.ax.clear()
        # Update the plot
        self.ax.scatter(list(self.x_queue), list(self.y_queue))
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        logging.warning(len(self.x_queue))
        # logging.warning(str(self.x_queue[-1]) + ", " + str(self.y_queue[-1]))


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
        
    
    def update_plot(self):
        pass

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
        self.reset_plots.emit()

    def on_plot_click(self):
        self.plotPB.setEnabled(False)
        self.start_plots.emit(int(self.length_line_edit.text()))

    def on_pause_state_changed(self, state):
        self.pause_plots.emit(state)
    
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
                    self.stop()
                new_x = x
                new_y = random.random()

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
    