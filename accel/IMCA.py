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
"""
#Define function ZUPT integration
def integrate_zupt(x, y, z, level, variance):
    #Create filtered x, y and z data structures
    x_filter = data_centering(kalman_filter(x, level, variance))
    y_filter = data_centering(kalman_filter(y, level, variance))
    z_filter = data_centering(kalman_filter(z, level, variance))

    #Find out when ZUPT should be applied for velocity
    t_temp_x = []
    for i in range(0, len(a)-1):
        if x_filter[i-1]<x_filter[i] and x_filter[i+1]<x_filter[i] or x_filter[i-1]>x_filter[i] and x_filter[i+1]>x_filter[i]:
            t_temp_x.append(i)
        else:
            t_temp_x.append(0)
    t_temp_y = []
    for i in range(0, len(a)-1):
        if y_filter[i-1]<y_filter[i] and y_filter[i+1]<y_filter[i] or y_filter[i-1]>y_filter[i] and y_filter[i+1]>y_filter[i]:
            t_temp_y.append(i)
        else:
            t_temp_y.append(0)
    t_temp_z = []
    for i in range(0, len(a)-1):
        if z_filter[i-1]<z_filter[i] and z_filter[i+1]<z_filter[i] or z_filter[i-1]>z_filter[i] and z_filter[i+1]>z_filter[i]:
            t_temp_z.append(i)
        else:
            t_temp_z.append(0)
            
    #Integrate with discrete summation for velocity
    v_x = np.zeros(len(a))
    v_y = np.zeros(len(a))
    v_z = np.zeros(len(a))
    for i in range(1, len(a)-1): #Need to consider that x direction should not be put to zero, since it is movement forwards. Find out what is x, y and z on IMU
        if t_temp_x[i] == i:
            v_x[i] = 0
            v_y[i] = v_y[i-1] + y_filter[i-1]
            v_z[i] = v_z[i-1] + z_filter[i-1]
            
        elif t_temp_y[i] == i:
            v_x[i] = v_x[i-1] + x_filter[i-1]
            v_y[i] = 0
            v_z[i] = v_z[i-1] + z_filter[i-1]

        elif t_temp_z[i] == i:
            v_x[i] = v_x[i-1] + x_filter[i-1]
            v_y[i] = v_y[i-1] + y_filter[i-1]
            v_z[i] = 0

        else:
            v_x[i] = v_x[i-1] + x_filter[i-1]
            v_y[i] = v_y[i-1] + y_filter[i-1]
            v_z[i] = v_z[i-1] + z_filter[i-1]
			
    return x_int2, y_int2, z_int2
			
	"""
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
#Lists containing acceleration and gyroscope data 
t1 = []
x1 = []
y1 = []
z1 = []
g1v = [] #yaw
g2v = [] #pitch
g3v = [] #roll

g1 = [] #yaw
g2 = [] #pitch
g3 = [] #roll


#open file
f = open(r'calibratedIMUdata.txt')

file = f.readlines()

#read in each column containing time, acceleration and gyrsocope data
for i, line in enumerate(file):
    if i < 0:
        continue
    else:
        t1.append(int(line.split('\t')[0]))
        x1.append(int(line.split('\t')[1]))
        y1.append(int(line.split('\t')[2]))
        z1.append(int(line.split('\t')[3]))
        g1v.append(int(line.split('\t')[4]))
        g2v.append(int(line.split('\t')[5]))
        g3v.append(int(line.split('\t')[6]))

#initialisation with acceleration while immobile, allows us to calculate initial angles. calculate the mean over 10 measures for better accuracy		
in_mean_x=0
in_mean_y=0
in_mean_z=0
for i in range (0,10):
	in_mean_x+=x1[i]
	in_mean_y+=y1[i]
	in_mean_z+=z1[i]
in_mean_x=in_mean_x/10
in_mean_x=in_mean_x/10
in_mean_x=in_mean_x/10
	
g1 = it.cumtrapz(g1v, t1, initial = 0)
g2 = it.cumtrapz(g2v, t1, initial = math.acos(in_mean_x/in_mean_z))
g3 = it.cumtrapz(g3v, t1, initial = math.acos(in_mean_y/in_mean_z))

#Store the resolved acceleration data
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

plt.plot(t1, r_x) #Data is very very noisy
plt.plot(t1, r_y)
plt.plot(t1, r_z)
plt.show()
plt.clf()
plt.cla()
plt.close()

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(r_x, r_y, r_z, 'gray')

plt.show()


