import serial
import csv

arduino_port = "COM3" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
fileName="finger long.csv" #name of the CSV file generated

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w") # write to a new file
print("Created file")

photodiode_data = []

samples = 10000




# create the CSV
with open(fileName, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for i in range(samples):
        getData=ser.readline()
        readings = getData.decode('utf-8').strip().split(",")
        # print(readings)

        writer.writerow(readings)

print("Data collection complete!")
file.close()