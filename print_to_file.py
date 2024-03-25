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

#IF WE HAVE DATA AND WANT TO REMOVE FIRST 5 SEC MANUALLY
# def remove_first_5_sec(data, period):
#      # Calculate the number of data points in the first 5 seconds
#     num_points_to_remove = int(5 / period) 
#     # Return the data without the first 5 seconds
#     return data[num_points_to_remove:]


def plot_fft(data, T, title, time):

    ys = np.fft.fft(data)
    N = len(data)
    freqs = np.fft.fftfreq(N, d=T)

    freqs_positive = freqs[1:N//2]
    ys_positive = 2.0/N * np.abs(ys[1:N//2])

    # Create a low-pass filter
    cutoff_freq = 5  # Cutoff frequency in Hz
    filter_mask = np.abs(freqs) <= cutoff_freq

    # Apply the filter to the FFT result
    filtered_fft = ys * filter_mask

    # Perform the inverse FFT to obtain the filtered signal
    filtered_signal = np.fft.ifft(filtered_fft)
    
    plt.plot(freqs_positive, ys_positive)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title(title)
    plt.grid(True)
    # plt.ylim([0, 500])
    filepath = os.path.join('plots', title)
    plt.savefig(filepath)

    # plt.plot(time, filtered_signal)
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.title(title)
    # plt.grid(True)
    # # Adjust x-axis ticks
    # num_ticks = 10  # Number of ticks you want to display
    # x_values = np.linspace(0, len(filtered_signal), num_ticks)
    # x_labels = np.linspace(0, len(data) * T, num_ticks)  # Adjust this according to your data
    # plt.xticks(x_values, x_labels, rotation=45)  # Rotate the labels for better readability
    
    # filepath = os.path.join('plots', title)
    # plt.savefig(filepath)

    return freqs_positive, ys_positive

def write_fft_to_file(freqs, ys, fileName):
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(freqs)):
            writer.writerow([freqs[i], ys[i]])


def main():
    if len(sys.argv) < 4:
        print("Usage: python print_to_file.py <output_file> <file length> <5 sec cutoff 'T' or 'F'>")
        return

    title = sys.argv[1]
    seconds = sys.argv[2] 
    print("saving to " + title + ".csv")
    fileName = os.path.join('data', title+'.csv')
    period = 0.01988

    ser = serial.Serial(arduino_port, baud)
    print("Connected to Arduino port:" + arduino_port)
    file = open(fileName, "w") # write to a new file
    print("Created file")

    # samples = 500
    
    with open(fileName, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        for i in range(int(seconds) * 50):
            print(i)
            samples_to_skip = 5 // period  # Integer division, Define the number of samples to be taken in the first 5 seconds
            if i < samples_to_skip and five_sec_cutoff == 'T':
                 continue  # Skip the first few samples if we are cutting out the first 5second 
            getData=ser.readline()
            readings = getData.decode('utf-8').strip().split(",")

            writer.writerow(readings)

    print("Data collection complete!")
    file.close()

    timecol = 0
    datacol = 1
    PATH = 'data/' + title + '.csv'
    time, data = get_data_from_csv(PATH, timecol, datacol)
    freq, y = plot_fft(data, period, title, time)
    # Can save to file if we want
    fftfile = "fft" + title + ".csv"
    # write_fft_to_file(freq, y, fftfile)


if __name__ == "__main__":
    main()