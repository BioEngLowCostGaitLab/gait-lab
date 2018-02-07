# Call with three arguments
# 1 = port
# 2 = Baudrate
# 3 = output file name
# ex: python tempsensor.py /dev/ttyACM0 9600 readings.csv


import serial, sys, datetime


with open("readings.csv", "w") as f:
  with serial.Serial("COM5", 9600) as ser:
    if ser.isOpen():
      ser.readline()
    while ser.isOpen():
      f.write('{}, {}'.format(datetime.datetime.now().strftime('%c'), ser.readline()))
	  
"""
	  
## import the serial library
import serial

## Boolean variable that will represent 
## whether or not the arduino is connected
connected = False

## establish connection to the serial port that your arduino 
## is connected to.

locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','COM4']

for device in locations:
    try:
        print ("Trying...",device)
        ser = serial.Serial(device, 9600)
        break
    except:
        print ("Failed to connect on", device)
ser = serial.Serial("COM5",9600)

		
## loop until the arduino tells us it is ready
while not connected:
    serin = ser.read()
    connected = True

## open text file to store the current 
##gps co-ordinates received from the rover    
text_file = open("position4.txt", 'w')
## read serial data from arduino and 
## write it to the text file 'position.txt'
while 1:
    if ser.inWaiting():
        x=ser.read()
        print(x) 
        text_file.write(x)
        if x=="\n":
             text_file.seek(0)
             text_file.truncate()
        text_file.flush()	

## close the serial connection and text file
text_file.close()
ser.close()
"""