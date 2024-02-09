import serial
import csv

arduino_port = "COM5" #serial port of Arduino
baud = 9600 #arduino uno runs at 9600 baud
fileName="finger_covering4_morepulses.csv" #name of the CSV file generated

ser = serial.Serial(arduino_port, baud)
print("Connected to Arduino port:" + arduino_port)
file = open(fileName, "w") # write to a new file
print("Created file")

photodiode_data = []

samples = 500

for i in range(samples):
    getData=ser.readline()
    readings = getData.decode('utf-8')
    readings = readings.split(",")
    print(readings)

    photodiode_data.append(readings)


# create the CSV
with open(fileName, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    for item in photodiode_data:
            # Write each item as a separate row in the CSV file
            writer.writerow([item])

print("Data collection complete!")
file.close()