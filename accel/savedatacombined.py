import serial

import time


name1 = raw_input("Please enter the name of the first port the bluetooth is connected to (out). Example: COM5 \n")

name2 = raw_input("Please enter the name of the second port \n")


 
try:  
	print "Trying...",name1
	arduino1 = serial.Serial(name1, 9600) 
	
except:  
	print "Failed to connect on",name1  
	
	
try:  
	print "Trying...",name2
	arduino2 = serial.Serial(name2, 9600) 
	
except:  
	print "Failed to connect on",name2 

text_file1 = open("C:\\Users\\Adriensv37\\Desktop\\year_2\\GitProjects\\gait-lab\\accel\\combined1.txt", 'w')

text_file2 = open("C:\\Users\\Adriensv37\\Desktop\\year_2\\GitProjects\\gait-lab\\accel\\combined2.txt", 'w')

try:
	arduino1.write('\n') 
	arduino2.write('\n')

	for i in range(301):
		#text_filewrite(time.time())
		text_file1.write(arduino1.readline())
		text_file1.flush()

		text_file2.write(arduino2.readline())
		text_file2.flush()

	text_file1.close()
	arduino1.close()

	text_file2.close()
	arduino2.close()
	
except:  
    print "Failed to send!" 

print 'Measurement over, please remember to press the reset button on the arduinos between every measurement'

	