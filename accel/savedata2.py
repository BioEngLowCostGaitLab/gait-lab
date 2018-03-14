import serial

import time

locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',
'/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','/dev/ttyS3','COM6','COM7']  
  
for device in locations:  
	try:  
		print "Trying...",device
		arduino = serial.Serial(device, 9600) 
		break
	except:  
		print "Failed to connect on",device   

text_file = open("position7.txt", 'w')

try:  
    print arduino.read()
except:  
    print "Failed to send!" 
	
for i in range(1001):
	
	text_file.write(arduino.readline())
text_file.flush()

text_file.close()
arduino.close()
	