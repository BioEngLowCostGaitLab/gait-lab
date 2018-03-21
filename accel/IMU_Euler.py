import matplotlib.pyplot as plt
import scipy.integrate as it
import numpy as np
import math
from mpl_toolkits import mplot3d

lower_limit = 0
upper_limit = 1000

#Lists containing acceleration and gyroscope data 
t1 = []
x1 = []
y1 = []
z1 = []
g1 = [] #yaw
g2 = [] #pitch
g3 = [] #roll


#open file
def readfile(f_in):
    f = open(f_in)

    file = f.readlines()

    #read in each column containing time, acceleration and gyrsocope data
    for i, line in enumerate(file):

        if i > lower_limit and i%2 == 0 and i < upper_limit:
            t1.append(int(line.split('\t')[0]))
            x1.append(int(line.split('\t')[1]))
            y1.append(int(line.split('\t')[2]))
            z1.append(int(line.split('\t')[3]))
            g1.append(int(line.split('\t')[4]))
            g2.append(int(line.split('\t')[5]))
            g3.append(int(line.split('\t')[6]))
            if i == len(file):
                break
            
    return t1, x1, y1, z1, g1, g2, g3

#Define rotation matrices for finding 3D position
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

#DC blocker takes away drift in data
def dc_blocker(xin, yin, zin):
	xout= np.zeros(len(xin))
	for i in range(1,len(xin)):
		xout[i]=(0.95*xout[i-1])+xin[i]-xin[i-1]
	yout= np.zeros(len(yin))
	for i in range(1,len(yin)):
		yout[i]=(0.95*yout[i-1])+yin[i]-yin[i-1]
	zout= np.zeros(len(zin))
	for i in range(1,len(zin)):
		zout[i]=(0.95*zout[i-1])+zin[i]-zin[i-1]
	return xout, yout, zout

def dc_blocker_single(xin):
    xout= np.zeros(len(xin))
    for i in range(1,len(xin)):
        xout[i]=(0.95*xout[i-1])+xin[i]-xin[i-1]

    return xout

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
def integrate_zupt(x, y, z):
    x_filter = data_centering(kalman_filter(x, 10, 15))
    y_filter = data_centering(kalman_filter(y, 10, 15))
    z_filter = data_centering(kalman_filter(z, 10, 15))
    
    #Find out when ZUPT should be applied for velocity
    t_temp_x = []
    for i in range(0, len(x_filter)-1):
        if x_filter[i-1]<x_filter[i] and x_filter[i+1]<x_filter[i] or x_filter[i-1]>x_filter[i] and x_filter[i+1]>x_filter[i]:
            t_temp_x.append(i)
        else:
            t_temp_x.append(0)
    t_temp_y = []
    for i in range(0, len(y_filter)-1):
        if y_filter[i-1]<y_filter[i] and y_filter[i+1]<y_filter[i] or y_filter[i-1]>y_filter[i] and y_filter[i+1]>y_filter[i]:
            t_temp_y.append(i)
        else:
            t_temp_y.append(0)
    t_temp_z = []
    for i in range(0, len(z_filter)-1):
        if z_filter[i-1]<z_filter[i] and z_filter[i+1]<z_filter[i] or z_filter[i-1]>z_filter[i] and z_filter[i+1]>z_filter[i]:
            t_temp_z.append(i)
        else:
            t_temp_z.append(0)
            
    #Integrate with discrete summation for velocity
    v_x = np.zeros(len(x_filter))
    v_y = np.zeros(len(y_filter))
    v_z = np.zeros(len(z_filter))
    for i in range(1, len(x_filter)-1):
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

    return v_x, v_y, v_z

#Regular integration
def integrate_normal(v_x, v_y, v_z):
    r_x = np.zeros(len(v_x))
    r_y = np.zeros(len(v_y))
    r_z = np.zeros(len(v_z))
    for i in range(1, len(v_x)-1):
            r_x[i] = r_x[i-1] + v_x[i-1]
            r_y[i] = r_y[i-1] + v_y[i-1]
            r_z[i] = r_z[i-1] + v_z[i-1]

    return r_x, r_y, r_z
    
#Store data from file
t,x,y,z,g1,g2,g3 = readfile(r'NathanTest2.txt')

#Saving data into correct coordinate frame
new_x = x
new_y = z
for i in range(0, len(y)):
    y[i] = -y[i]
new_z = y
new_g1 = g1
new_g2 = g3
for i in range(0, len(g2)):
    g2[i] = -g2[i]
new_g3 = g2

#Filtering data and integrating data
x_block, y_block, z_block = dc_blocker(new_x, new_y, new_z)
g1_block, g2_block, g3_block = dc_blocker(new_g1, new_g2, new_g3)

g1_filter = kalman_filter(g1_block, 5, 15)
g2_filter = kalman_filter(g2_block, 5, 15)
g3_filter = kalman_filter(g3_block, 5, 15)

x_filter = kalman_filter(x_block, 5, 15)
y_filter = kalman_filter(y_block, 5, 15)
z_filter = kalman_filter(z_block, 5, 15)

v_x_temp, v_y_temp, v_z_temp = integrate_zupt(x_filter, y_filter, z_filter)

v_x = kalman_filter(v_x_temp, 10, 15)
v_y = kalman_filter(v_x_temp, 10, 15)
v_z = kalman_filter(v_x_temp, 10, 15)

r_x_temp, r_y_temp, r_z_temp = integrate_normal(v_x, v_y, v_z)

r_x_temp2, r_y_temp2, r_z_temp2 = dc_blocker(r_x_temp, r_y_temp, r_z_temp)

r_x = kalman_filter(r_x_temp, 10, 15)
r_y = kalman_filter(r_x_temp, 10, 15)
r_z = kalman_filter(r_x_temp, 10, 15)

#Test test data
v_x_test = kalman_filter(dc_blocker_single(kalman_filter(v_x, 6, 15)), 6, 16)

r_x_test = it.cumtrapz(v_x_test, t, initial = 0)

#Resolving data for inertial frame

a = [] #a is the general resolved acceleration matrix
for i in range(0, len(t)):
    a.append(a_I(x_filter[i], y_filter[i], z_filter[i], g1_filter[i], g2_filter[i], g3_filter[i]))

#Store the data from matrix a in lists for plotting
x_res = []
y_res = []
z_res = []

for i in range(0, len(a)):
    x_res.append(int(a[i][0]))
    y_res.append(int(a[i][1]))
    z_res.append(int(a[i][2]))

#Integrate to obtain resolved data
    v_x_res, v_y_res, v_z_res = integrate_zupt(x_res, y_res, z_res)
    r_x_res, r_y_res, r_z_res = integrate_normal(v_x_res, v_y_res, v_z_res)

#Plotting functions

fig = plt.figure(1, figsize=(16,9))
ax1 = plt.subplot()

ax1.plot(t, x_filter, label = 'x')
ax1.plot(t, new_x, label = 'new x')

plt.ylabel('Acceleration [\u221Dm/s^2]', size = 25)
plt.xlabel('Time [\u221Ds]', size = 25)
ax1.legend(loc=2, prop={'size': 25})

#plt.show()

fig = plt.figure(2, figsize=(16,9))
ax2 = plt.subplot()

ax2.plot(t, v_x, label = 'Velocity')
ax2.plot(t, v_x_test, label = 'Velocity double Kalman')

plt.ylabel('Velocity [\u221Dm/s]', size = 25)
plt.xlabel('Time [\u221Ds]', size = 25)
ax2.legend(loc=2, prop={'size': 25})

#plt.show()

fig = plt.figure(3, figsize=(16,9))
ax3 = plt.subplot()

#ax2.plot(t, v_x, label = 'Velocity')
ax3.plot(t, r_x_test, label = 'Position')

plt.ylabel('Velocity [\u221Dm/s]', size = 25)
plt.xlabel('Time [\u221Ds]', size = 25)
ax3.legend(loc=2, prop={'size': 25})
plt.show()
"""

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(r_x_res, r_y_res, r_z_res, 'gray')

plt.show()
"""
