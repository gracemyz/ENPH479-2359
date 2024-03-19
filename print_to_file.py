import serial
import csv
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

arduino_port = "COM3" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud



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
    file.close()
    return time, data

def plot_fft(data, T, title):

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
    return freqs_positive, ys_positive

def write_fft_to_file(freqs, ys, fileName):
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(freqs)):
            writer.writerow([freqs[i], ys[i]])



def main():
    if len(sys.argv) < 3:
        print("Usage: python print_to_file.py <output_file> <file length>")
        return

    title = sys.argv[1]
    samples = sys.argv[2]
    fileName = os.path.join('data', title)

    ser = serial.Serial(arduino_port, baud)
    print("Connected to Arduino port:" + arduino_port)
    file = open(fileName, "w") # write to a new file
    print("Created file")

    # samples = 500
    
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(samples):
            getData=ser.readline()
            readings = getData.decode('utf-8').strip().split(",")

            writer.writerow(readings)

    print("Data collection complete!")
    file.close()

    timecol = 0
    datacol = 1
    period = 0.01988
    PATH = 'data/' + title + '.csv'
    time, data = get_data_from_csv(PATH, timecol, datacol)
    freq, y = plot_fft(data, period)
    # Can save to file if we want
    # write_fft_to_file(freqs, y, fftfile)


if __name__ == "__main__":
    main()