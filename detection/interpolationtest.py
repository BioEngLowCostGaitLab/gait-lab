from functions import *
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(10)
y = np.exp(x)


ms = marker_sequence('blue', 10, 1)

for i in range(10):
    if i % 2 <= 0:
        ms.set_coordinates(x[i], y[i], i)

print(ms.coordinates)

ms._interpolate()
print(ms.coordinates)

plt.plot(ms.coordinates[:-2, 0], ms.coordinates[:-2, 1])
plt.savefig('interpolate.png')
