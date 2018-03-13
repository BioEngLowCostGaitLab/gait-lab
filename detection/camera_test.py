import os
from time import time


os.system('adb devices > temp.txt')

devices = list()

f = open('temp.txt', 'r').readlines()


for line in f:
    if 'device' in line and not 'devices' in line:
        devices.append(line.split('\t')[0])

for i in range(100):
    T = float(time())
    os.system('adb -s %s shell input tap 0 0 ' % (devices[0]))
    T1 = time()
    print(float(T1) - T)
