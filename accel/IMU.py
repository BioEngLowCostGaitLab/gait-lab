import matplotlib.pyplot as plt
import scipy.integrate as it
import numpy as np
import math

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


#Lists containing acceleration and gyroscope data 
t1 = []
x1 = []
y1 = []
z1 = []
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
        g1.append(int(line.split('\t')[4]))
        g2.append(int(line.split('\t')[5]))
        g3.append(int(line.split('\t')[6]))

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

#Plot acceleration applying filtering
plt.plot(t1, kalman_filter(x, 5, 17)) #Data is very very noisy
plt.plot(t1, kalman_filter(y, 5, 17))
plt.plot(t1, kalman_filter(z, 5, 17))
plt.show()

#Integrate with discrete summation
v_x = np.zeros(len(a))
v_y = np.zeros(len(a))
v_z = np.zeros(len(a))
for i in range(1, len(a)):
    v_x[i] = v_x[i-1] + x[i-1]
    v_y[i] = v_y[i-1] + y[i-1]
    v_z[i] = v_z[i-1] + z[i-1]

plt.plot(t1, kalman_filter(v_x, 5, 17)) #Data is very very noisy
plt.plot(t1, kalman_filter(v_y, 5, 17))
plt.plot(t1, kalman_filter(v_z, 5, 17))
plt.show()
