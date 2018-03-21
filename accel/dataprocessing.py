import matplotlib.pyplot as plt
import scipy.integrate as it
import numpy as np
import math
from mpl_toolkits import mplot3d


#Define rotation matrices
def R_v1_I(psi):
    return np.matrix([[math.cos(psi), math.sin(psi), 0], [-math.sin(psi), math.cos(psi), 0], [0, 0, 1]])

def R_v2_v1(theta):
    return np.matrix([[math.cos(theta), 0, -math.sin(theta)], [0, 1, 0], [math.sin(theta), 0, math.cos(theta)]])

def R_B_v2(phi):
    return np.matrix([[1, 0, 0], [0, math.cos(phi), math.sin(phi)], [0, -math.sin(phi), math.cos(phi)]])

#Combine rotation matrices to matrix rotating body frame to inertial frame
def R_I_B(psi, theta, phi):
    return R_v1_I(-psi)*R_v2_v1(-theta)*R_B_v2(-phi)

#Convert accelerometer data to inertial frame (frame with reference to earth)
def a_I(a_x, a_y, a_z, psi, theta, phi):
    a_m = np.matrix([[a_x], [a_y], [a_z]])
    R = R_I_B(psi, theta, phi)
    g = np.matrix([[0], [0], [1]]) #1 refers to 1g, which is 9.81   
    return R*a_m+g
	

#Kalman filter adapted from online resources
def kalman_filter(x, level, variance): #x is data to be smoothed, level is blending factor, variance is process variance
   n_iter = len(x)
   sz = (n_iter,) #size of array
   Q = math.exp(-variance) #process variance

   xhat = np.zeros(sz)
   P = np.zeros(sz)
   xhatminus = np.zeros(sz)
   Pminus = np.zeros(sz)
   K = np.zeros(sz)
   #x2 = np.random.normal(x, 0.1, size = sz)

   R = 0.1**level

   xhat[0] = 0.0
   P[0] = 1.0

   for k in range(1, n_iter):
      xhatminus[k] = xhat[k-1]
      Pminus[k] = P[k-1]+Q
      K[k] = Pminus[k]/(Pminus[k]+R)
      xhat[k] = xhatminus[k]+K[k]*(x[k]-xhatminus[k])
      P[k] = (1-K[k])*Pminus[k]

   return xhat
#Data centering

def data_centering(x):
   xsum = 0
   xcent = np.zeros(len(x))  
   for i in range(0, len(x)):
      xsum = x[i]+xsum 
   xavg = xsum/len(x)
   for i in range(0, len(x)):
      xcent[i] = x[i] - xavg

   return xcent
   
#Define function ZUPT integration
def integrate_zupt(x, y, z, level, variance):
	#Create filtered x, y and z data structures
	x_filter = data_centering(kalman_filter(x, level, variance))
	y_filter = data_centering(kalman_filter(y, level, variance))
	z_filter = data_centering(kalman_filter(z, level, variance))
	
	x_int = it.cumtrapz(x_filter, t1, initial = 0)
	y_int = it.cumtrapz(y_filter, t1, initial = 0)
	z_int = it.cumtrapz(z_filter, t1, initial = 0)
	x_int2 = it.cumtrapz(x_int, t1, initial = 0)
	y_int2 = it.cumtrapz(y_int, t1, initial = 0)
	z_int2 = it.cumtrapz(z_int, t1, initial = 0)

	
	return x_int2, y_int2, z_int2
	
def readfile(filename):
#open file

	t = []
	x = []
	y = []
	z = []
	yaw = [] #yaw
	pitch = [] #pitch
	roll = [] #roll
	
	f = open(filename)

	file = f.readlines()

	#read in each column containing time, acceleration and gyrsocope data
	for i, line in enumerate(file):
		if i < 0:
			continue
		else:
			t.append(int(line.split('\t')[0]))
			x.append(int(line.split('\t')[1]))
			y.append(int(line.split('\t')[2]))
			z.append(int(line.split('\t')[3]))
			yaw.append(int(line.split('\t')[4]))
			pitch.append(int(line.split('\t')[5]))
			roll.append(int(line.split('\t')[6]))

	return t,x,y,z,yaw,pitch,roll
#Lists containing acceleration and gyroscope data 

t1,x1,y1,z1,g1v0,g2v0,g3v0= readfile('anttigabor.txt')


#initialisation with acceleration while immobile, allows us to calculate initial angles. calculate the mean over 10 measures for better accuracy	
def get_angles(yaw, pitch, roll):
	in_mean_x=0
	in_mean_y=0
	in_mean_z=0
	for i in range (0,10):
		in_mean_x+=x1[i]
		in_mean_y+=y1[i]
		in_mean_z+=z1[i]
	in_mean_x=in_mean_x/10
	in_mean_y=in_mean_y/10
	in_mean_z=in_mean_z/10
	
	g1v = data_centering(kalman_filter(yaw, 5, 10))
	g2v = data_centering(kalman_filter(pitch, 5, 10))
	g3v = data_centering(kalman_filter(roll, 5, 10))
	
	
	if in_mean_x==0 and in_mean_y==0 and in_mean_z==0:
		print("The IMU is not functionning properly")
		
	elif in_mean_x==0 and in_mean_y==0:	
		g1 = it.cumtrapz(g1v, t1, initial = 0)
		g2 = it.cumtrapz(g2v, t1, initial = np.sign(in_mean_x)*math.acos(in_mean_z/math.sqrt(in_mean_x**2+in_mean_z**2)))
		g3 = it.cumtrapz(g3v, t1, initial = np.sign(in_mean_z)*math.acos(in_mean_y/math.sqrt(in_mean_z**2+in_mean_y**2)))
	
	elif in_mean_z==0 and in_mean_x==0:
		g1 = it.cumtrapz(g1v, t1, initial = np.sign(in_mean_y)*math.acos(in_mean_x/math.sqrt(in_mean_x**2+in_mean_y**2)))
		g2 = it.cumtrapz(g2v, t1, initial = 0)
		g3 = it.cumtrapz(g3v, t1, initial = np.sign(in_mean_z)*math.acos(in_mean_y/math.sqrt(in_mean_z**2+in_mean_y**2)))
	
	elif in_mean_z==0 and in_mean_y==0:
		g1 = it.cumtrapz(g1v, t1, initial = np.sign(in_mean_y)*math.acos(in_mean_x/math.sqrt(in_mean_x**2+in_mean_y**2)))
		g2 = it.cumtrapz(g2v, t1, initial = np.sign(in_mean_x)*math.acos(in_mean_z/math.sqrt(in_mean_x**2+in_mean_z**2)))
		g3 = it.cumtrapz(g3v, t1, initial = 0)
		
	else:
		g1 = it.cumtrapz(g1v, t1, initial = np.sign(in_mean_y)*math.acos(in_mean_x/math.sqrt(in_mean_x**2+in_mean_y**2)))
		g2 = it.cumtrapz(g2v, t1, initial = np.sign(in_mean_x)*math.acos(in_mean_z/math.sqrt(in_mean_x**2+in_mean_z**2)))
		g3 = it.cumtrapz(g3v, t1, initial = np.sign(in_mean_z)*math.acos(in_mean_y/math.sqrt(in_mean_z**2+in_mean_y**2)))
	return g1,g2,g3
	
#Store the resolved acceleration data
g1,g2,g3= get_angles(g1v0,g2v0,g3v0)
a = []

for i in range(0, len(t1)):
    a.append(a_I(x1[i], y1[i], z1[i], g1[i], g2[i], g3[i]))

#Store x y and z acceleration data in lists
x = []
y = []
z = []
for i in range(0, len(a)):
    x.append(int(a[i][0]))
    y.append(int(a[i][1]))
    z.append(int(a[i][2]))

#Define positions
r_x, r_y, r_z = integrate_zupt(x1, y1, z1, 5, 10)
r_x= r_x*60/93310.8432708
r_y= r_y*60/93310.8432708
r_z= r_z*60/93310.8432708
#Plot data
#plt.plot(t1, x_filter) #Data is very very noisy
#plt.plot(t1, y_filter)
#plt.plot(t1, z_filter)

#plt.plot(t1, kalman_filter(x1, 5, 15)) #Data is very very noisy
#plt.plot(t1, y1)
#plt.plot(t1, z1)

#plt.plot(t1, v_x_filter) #Data is very very noisy
#plt.plot(t1, v_y)
#plt.plot(t1, v_z)

def dc_blocker(xin):
	xout= xin*0
	for i in range(1,len(xin)):
		xout[i]=(0.95*xout[i-1])+xin[i]-xin[i-1]
	return xout	

def get_sway(xin):
	indicator=0
	slope=0
	maxima=[]
	sway=[]
	for i in range(1,len(xin)):
		if xin[i-1]>xin[i]:
			slope=0
		elif xin[i-1]<xin[i]:
			slope = 1
		if slope != indicator:
			maxima.append(i)
			indicator=slope
	average=0
	for i in range(1,len(maxima)):
		sway.append(abs(xin[maxima[i]]-xin[maxima[i-1]]))
	for i in range(len(sway)):
		average+=sway[i]
	average=average/len(sway)

		
		
	return maxima,sway,average

def remove_outlying_data(poi,sway,average):
	acceptable= False
	avg=average
	i = 0
	while i < len(sway):
		if sway[i]<0.5*avg or sway[i]> avg*1.5:
			sway.pop(i)
			poi.pop(i+1)
		else:
			i += 1
	#sway = [x for x in sway if x < avg*1.3 and x> avg* 0.7]
	"""while acceptable == False:
		
	acceptable= True
		print len(sway)
		for i in xrange(0,len(sway)):
			print i
			if sway[i] > avg*1.3 or sway[i] < avg*0.7:
				acceptable= False
				del sway[i]
				del poi[i]"""
	avg= np.mean(sway)
	
	return poi, sway, avg
	
r_xAC= dc_blocker(r_x)
r_yAC= dc_blocker(r_y)
r_zAC= dc_blocker(r_z)

poi0,sway0,avg0=get_sway(r_xAC)
poi,sway,avg=remove_outlying_data(poi0,sway0,avg0)
#poi,sway,avg=remove_outlying_data(poi0,sway0,avg0)

plt.plot(t1, r_xAC, '-gD', markevery=poi) #Data is very very noisy
#plt.plot(t1, r_y)
#plt.plot(t1, r_z)
plt.title('SWAY (average={})'.format(avg))
plt.xlabel('Time (seconds*sample rate)')
plt.ylabel('Position (cm)')

plt.show()
plt.clf()
plt.cla()
plt.close()

plt.plot(t1, g1, '-gD', markevery=poi) #Data is very very noisy
plt.plot(t1, g2, 'r', markevery=poi) #Data is very very noisy
plt.plot(t1, g3, 'b', markevery=poi) #Data is very very noisy

#plt.plot(t1, r_y)
#plt.plot(t1, r_z)
plt.title('SWAY (average={})'.format(avg))
plt.xlabel('Time (seconds*sample rate)')
plt.ylabel('Position (cm)')

plt.show()
plt.clf()
plt.cla()
plt.close()





fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(r_xAC, r_yAC, r_zAC, 'gray')

plt.show()


