import os
from time import time

os.system('adb kill-server')
os.system('adb devices > temp.txt')

devices = list()

f = open('temp.txt', 'r').readlines()


for line in f:
    if 'device' in line and not 'devices' in line:
        devices.append(line.split('\t')[0])

for i in range(100):
    for device in devices:
        T = float(time())
        os.system('adb -s %s shell input tap 0 0 ' % (device))
        print(float(time()) - T)
