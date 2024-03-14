import csv
import numpy as np
import matplotlib.pyplot as plt



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
    freqs = np.fft.fftfreq(len(data), d=T)


    plt.plot(freqs, np.abs(ys))
    plt.xlabel("freq")
    plt.ylabel('fft')
    plt.xlim([0,10])
    # plt.ylim([0,1000])
    plt.show()

PATH = 'data/James data.csv'
# PATH = 'data/1led_finger_blackout.csv'
timecol = 1
datacol = 3
# period = 0.01988
period = 0.03125/1000
time, data = get_data_from_csv(PATH, timecol, datacol)
# data = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 1000)) 
plot_fft(data, period)
