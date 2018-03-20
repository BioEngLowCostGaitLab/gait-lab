import os
import sys
from os.path import join, isfile
import argparse
from time import sleep, time
import shutil
import cv2
from functions import compute_rotation_angle
from math import ceil
import numpy as np

def get_args(root):
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--time", type=int,
    required=True,
    help="Seconds to record video"),
    ap.add_argument("-dir", "--directory", type=str,
    default=os.getcwd(),
    help="Directory to store recorded videos"),
    ap.add_argument("-p", "--prototxt", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.prototxt'),
	help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", type=str,
    default=join(root, 'resources', 'MobileNetSSD_deploy.caffemodel'),
	help="path to Caffe pre-trained model")


    return ap.parse_args()

root = os.getcwd()
try:
    dirs = sys.argv[0].split('\\')[1:-1]
    if len(dirs) > 0:
        root = 'C:\\'
        for i in range(len(dirs)):
            root = join(root, dirs[i])
except:
    pass

opts = get_args(root)


# List all connected devices
os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe kill-server')
os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe devices > temp.txt')

devices = list()

f = open('temp.txt', 'r').readlines()


for line in f:
    if 'device' in line and not 'devices' in line:
        devices.append(line.split('\t')[0])



# Record video on all devices
print('[INFO] Starting video recording')
video_times = list()
runs = list()
for device in devices:
    T = float(time())
    os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe -s %s shell input tap 0 0' % (device))
    video_times.append(time() )
    runs.append(float(video_times[-1]) - T)
print('[INFO] All videos recording')
sleep(opts.time)
for device in devices:
    os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe -s %s shell input tap 0 0' % (device))
print('[INFO] Saving videos')
sleep(5)

print('[INFO] Pulling videos')


# Retrieve videos
video_names = list()
for i in range(len(devices)):
    os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe -s %s pull /sdcard/Android/data/com.example.android.camera2video/files %s' %
              (devices[i], opts.directory))
    video_time = 0
    correct_video = None
    for f in os.listdir(join(opts.directory, 'files')):
        if int(f.split('.')[0]) > video_time:
            video_time = int(f.split('.')[0])
            correct_video = f
    video_names.append(join(opts.directory,
                            correct_video))  #'%i.mp4' % (int(1000 * float(video_times[i])))))
    shutil.copy(join(opts.directory, 'files', correct_video),
                video_names[-1])
    shutil.rmtree(join(opts.directory, 'files'))
    os.system('C:\\Gait-Lab\\resources\\adb\\platform-tools\\adb.exe -s %s shell rm -r /sdcard/Android/data/com.example.android.camera2video/files'
                % (devices[i]))

ssd = cv2.dnn.readNetFromCaffe(opts.prototxt, opts.model)
frame_rate = 30.0
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

for i, video_name in enumerate(video_names):
    print('[INFO] Opening video: %s' % (video_name))
    print('[INFO] Computing rotation angle')
    sys.stdout.flush()
    angle = compute_rotation_angle(str(video_name), ssd)
    print('[INFO] Computed rotation angle of %d degrees' % (angle * 90))
    total_start_frame_difference = ceil((float(video_times[-1]) -
                                        float(video_times[i]) -
                                        runs[-1] +
                                        runs[i]) * frame_rate)
    print('[INFO] %d frames will be cropped from the start' %
            (total_start_frame_difference))
    cap = cv2.VideoCapture(str(video_name))
    if i is 0: length = (int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) -
                        total_start_frame_difference)
    frame_count, written_frame_count = 0, 0
    out_video_name = 'video' + str(i) + '.avi'
    out = cv2.VideoWriter(out_video_name, fourcc, frame_rate, (1280,720))
    print('[INFO] Length of videos %d frames' % (length))

    while True:
        ret, frame = cap.read()
        if ret and written_frame_count < length:
            if frame_count >= total_start_frame_difference:
                frame = np.rot90(frame, angle)
                out.write(frame)
                written_frame_count += 1
                sys.stdout.write('\r[INFO] %d/%d frames written' %
                                (written_frame_count, length))
                sys.stdout.flush()
        else:
            print()
            break
        frame_count += 1
    cap.release()
    out.release()
    cv2.destroyAllWindows()
