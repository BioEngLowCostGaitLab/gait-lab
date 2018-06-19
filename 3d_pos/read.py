import json
import numpy
import matplotlib.pyplot as plt


d = json.load(open('C:/Gait-Lab/resources/JSONfiles/angles.json'))

data= d["anglesave"]

x=range(len(data))
x=numpy.array(x)
plt.xlabel('Time (s)')
plt.ylabel('Joint angle ''(''$^\circ$'')''')
plt.title('Joint angle ''(''$^\circ$'')'' vs Time (s)') 
x=x*0.033


plt.plot(x, data)
plt.savefig('C:/Gait-Lab/resources/JSONfiles/angles.png')

print(data)