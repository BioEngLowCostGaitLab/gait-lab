from functions import *
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1000)
y = np.sin(x / 20)


ms = marker_sequence('blue', 1000, 1)

for i in range(1000):
    if i % 40 <= 20:
        ms.set_coordinates(x[i], y[i], i)

print(ms.coordinates)

ms._interpolate()
#
print(ms.coordinates[1,:])

plt.plot(ms.coordinates[0, :], ms.coordinates[1, :])
#plt.hold(True)
#plt.plot(x, y)
plt.show()
