import csv
import numpy as np
import os
import matplotlib.pyplot as plt

title = "20240324_ambient_neweval"


def get_data_from_csv(path, timecol, datacol):
    time = []
    data = []
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        
        next(csv_reader) # skip first row
        for row in csv_reader:
            # Process each row
            time.append(row[timecol])
            data.append(row[datacol])
    return time, data

def plot_fft(data, T):

    ys = np.fft.fft(data)
    N = len(data)
    freqs = np.fft.fftfreq(N, d=T)


    freqs_positive = freqs[1:N//2]
    ys_positive = 2.0/N * np.abs(ys[1:N//2])
    
    plt.plot(freqs_positive, ys_positive)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.grid(True)
    filepath = os.path.join('plots', title)
    plt.savefig(filepath)
    plt.show()
    
PATH = 'data/' + title + '.csv'
# PATH = 'data/1led_finger_blackout.csv'
timecol = 0
datacol = 1
period = 0.01988
# period = 0.03125/1000
time, data = get_data_from_csv(PATH, timecol, datacol)
# data = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 1000)) 
plot_fft(data, period)
