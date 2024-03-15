import serial
import csv
import os

arduino_port = "COM3" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
title="evalboard_led_off_bc.csv" #name of the CSV file generated
fileName = os.path.join('data', title)

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w") # write to a new file
print("Created file")

photodiode_data = []

samples = 500




# create the CSV
with open(fileName, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(samples):
        getData=ser.readline()
        readings = getData.decode('utf-8').strip().split(",")
        print(readings)

        writer.writerow(readings)

print("Data collection complete!")
file.close()