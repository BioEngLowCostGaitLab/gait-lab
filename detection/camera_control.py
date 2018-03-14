import os
import argparse
from time import sleep, time
from os.path import join
import shutil

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--time", type=int,
    required=True,
	help="Seconds to record video")
    ap.add_argument("-dir", "--directory", type=str,
    required=True,
    help="Directory to store recorded videos")


    return ap.parse_args()

opts = get_args()

def tapping_event(devices, dims, index):
    return 'adb -s %s shell input tap 0 0' % (devices[index])

# List all connected devices
os.system('adb kill-server')
os.system('adb devices > temp.txt')

devices = list()

f = open('temp.txt', 'r').readlines()


for line in f:
    if 'device' in line and not 'devices' in line:
        devices.append(line.split('\t')[0])


# Get screen sizes for connected devices
dims = list()

for device in devices:
    os.system('adb -s %s shell wm size > temp.txt' % (device))
    f = open('temp.txt', 'r').readlines()
    for line in f:
        if any('Override size' in line for line in f):
            if 'Override size' in line:
                width = int(line.split(' ')[-1].split('x')[0])
                height = int(line.split(' ')[-1].split('x')[1])
                dims.append((width, height))
                break
        else:
            if 'Physical size' in line:
                width = int(line.split(' ')[-1].split('x')[0])
                height = int(line.split(' ')[-1].split('x')[1])
                dims.append((width, height))
                break

# Record video on all devices
print('[INFO] Starting video recording')
video_times = list()

for device in devices:
    os.system('adb -s %s shell input tap 0 0' % (device))
    video_times.append(time())
print('[INFO] All videos recording')
sleep(opts.time)
for device in devices:
    os.system('adb -s %s shell input tap 0 0' % (device))
    print(float(time()) - float(video_times[0]))

print('[INFO] Saving videos')


# Retrieve videos
for i in range(len(devices)):
    os.system('adb -s %s pull /sdcard/Android/data/com.example.android.camera2video/files %s' %
              (devices[i], opts.directory))
    video_time = 0
    correct_video = None
    for f in os.listdir(join(opts.directory, 'files')):
        if int(f.split('.')[0]) > video_time:
            video_time = int(f.split('.')[0])
            correct_video = f

    shutil.copy(join(opts.directory, 'files', correct_video),
                join(opts.directory, '%i.mp4' % (int(1000 * float(video_times[i])))))
    shutil.rmtree(join(opts.directory, 'files'))
    os.system('adb -s %s shell rm -r /sdcard/Android/data/com.example.android.camera2video/files'
                % (devices[i]))
