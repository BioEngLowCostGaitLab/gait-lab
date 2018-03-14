import serial
import time

locations=['/dev/ttyUSB0','/dev/ttyUSB1','/dev/ttyUSB2','/dev/ttyUSB3',
'/dev/ttyS0','/dev/ttyS1','/dev/ttyS2','COM7']  
  
for device in locations:  
	try:  
		print "Trying...",device
		arduino = serial.Serial(device, 9600) 
		break
	except:  
		print "Failed to connect on",device   

try:  
    arduino.write('Hello darkness my old friend \n')  
    time.sleep(1)
    print arduino.readline()
except:  
    print "Failed to send!" 