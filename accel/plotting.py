import matplotlib.pyplot as plt
from scipy import integrate
import scipy.integrate as it
import numpy as np

f = open(r'calibratedIMUdata.txt')

#length = int(input("How many lines?: "))


#for i in range(0, length):
#line = f.read().splitlines()
#for j in range(0, 3*length, 4):      
#   t.append(float(line[j]))
   
#for j in range(1, 3*length, 4):      
#   x.append(float(line[j]))
   
#for j in range(2, 3*length, 4):      
#   y.append(float(line[j]))

#for j in range(3, 3*length, 4):      
#   z.append(float(line[j]))

t1 = []
x1 = []
y1 = []
z1 = []

file = f.readlines()

#t = np.zeros(len(file))
#x, y, z = t, t, t

for line in file:
   t1.append(int(line.split('\t')[0]))
   x1.append(int(line.split('\t')[1]))
   y1.append(int(line.split('\t')[2]))
   z1.append(int(line.split('\t')[3]))

t = np.array(t1)
x = np.array(x1)
y = np.array(y1)
z = np.array(z1)
x0 = np.zeros(len(file))
   
"""
print(y)
print(z)
"""

#Kalman filter
def kalman_filter(x, level):
   n_iter = 1001
   sz = (n_iter,) #size of array
   Q = 1e-5 #process variance

   xhat = np.zeros(sz)
   P = np.zeros(sz)
   xhatminus = np.zeros(sz)
   Pminus = np.zeros(sz)
   K = np.zeros(sz)
   x3=0
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

#print(t, xhat)
#plt.plot(z)
#plt.plot(t, xhat)
#plt.axhline(x,color='g',label='truth value')
#plt.legend()
#plt.title('Estimate vs. iteration step', fontweight='bold')
#plt.xlabel('Iteration')
#plt.ylabel('Voltage')

"""
#Assumption of 0 velocity


x_int = it.cumtrapz(x, t, initial = 0)

for i in range(0, 1000):
   if x[i-1]<x[i] and x[i+1]<x[i] or x[i-1]>x[i] and x[i+1]>x[i]:
      t_temp.append(int(i))

for i in range(0, len(t_temp)):
   x_int[t_temp[i]] = 0

for i in range(0, len(t_temp)):
   print(x[i-1], x[i], x[i+1])



y_int = it.cumtrapz(y, t, initial = 0)
z_int = it.cumtrapz(z, t, initial = 0)

x_int2 = it.cumtrapz(x_int, t, initial = 0)
y_int2 = it.cumtrapz(y_int, t, initial = 0)
z_int2 = it.cumtrapz(z_int, t, initial = 0)
"""
xfilter = kalman_filter(x, 3)
yfilter = kalman_filter(y, 2)
zfilter = kalman_filter(z, 2)

#print(x, xhat)

x_int = it.cumtrapz(xfilter, t, initial = 0)
y_int = it.cumtrapz(yfilter, t, initial = 0)
z_int = it.cumtrapz(zfilter, t, initial = 0)

x_int2 = it.cumtrapz(x_int, t, initial = 0)

#plt.plot(t, x_int)
#plt.plot(t, xfilter)
plt.plot(t, zfilter)
#plt.plot(t, z_int)
#plt.plot(t, zfilter)
#plt.plot(t, x_int2)
plt.plot(t, z)
#plt.plot(t, x)
#plt.plot(t, z)

plt.ylabel('Gaitsway')
plt.show()

