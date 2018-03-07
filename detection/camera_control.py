import os
import argparse
from time import sleep

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--time", type=int,
    required=True,
	help="Seconds to record video")

    return ap.parse_args()

opts = get_args()

os.system('adb shell wm size > temp.txt') # write screen dimensions to file

f = open('temp.txt', 'r').readlines()

for line in f:
    if 'Physical size' in line:
        width = int(line.split(' ')[-1].split('x')[0])
        height = int(line.split(' ')[-1].split('x')[1])
        break

tapping_event = 'adb shell input tap %i %i' % (0.5 * width, int(0.875 * height))

os.system(tapping_event)
print('Im recording this video from my phone')
sleep(opts.time)
os.system(tapping_event)
