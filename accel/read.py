import json
import numpy
import matplotlib.pyplot as plt


d = json.load(open('angles.json'))

data= d["anglesave"]

x=range(len(data))
x=numpy.array(x)
plt.xlabel('Time (s)')
plt.ylabel('Joint angle (degrees)')
x=x*0.033


plt.plot(x, data)
plt.show()
plt.savefig('angles.jpg')

print(data)