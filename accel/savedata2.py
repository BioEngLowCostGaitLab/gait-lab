import serial

import time


name = raw_input("Please enter the name of the port the bluetooth is connectet to (out). Example: COM5 \n")

locations=[name]  
  
for device in locations:  
	try:  
		print "Trying...",device
		arduino = serial.Serial(device, 9600) 
		break
	except:  
		print "Failed to connect on",device   

text_file = open("C:\\Users\\Adriensv37\\Desktop\\year_2\\GitProjects\\gait-lab\\accel\\anttigabor1.txt", 'w')

try:
	arduino.write('\n') 

	for i in range(301):
		#text_filewrite(time.time())
		text_file.write(arduino.readline())
		text_file.flush()

	text_file.close()
	arduino.close()
	
except:  
    print "Failed to send!" 

print 'Please remember to press the reset button on the arduino between every measurement'

	