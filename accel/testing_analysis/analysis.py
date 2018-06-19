import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import pickle

imu_data = pd.read_csv("imu_data.csv")
lab_data = pd.read_csv("x-y_data.csv")

print(imu_data)
print(lab_data)

plt.plot(imu_data)
plt.show()
#plt.plot(lab_data)
#plt.show()

x, y = lab_data['x'], lab_data['y']

plt.plot(x)
plt.plot(y)
plt.plot(x,y)
plt.show()
