import serial
import time

locations=['COM6']  
  
for device in locations:  
	try:  
		print "Trying...",device
		arduino = serial.Serial(device, 9600) 
		break
	except:  
		print "Failed to connect on",device   

text_file = open("position8.txt", 'w')
try:  
    arduino.write('\n')  
    print arduino.readline()
except:  
    print "Failed to send!" 