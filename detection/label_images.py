import os
from os.path import join
from time import time
import argparse
import shutil

root = os.getcwd()

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dir', type=str, required=True,
    help='image folder')
    #ap.add_argument('-f', '--file', type=str, default='labels.txt',
    #help='label file')

    return vars(ap.parse_args())



"""
    Data labeling tool for Windows. For other operating systems, the os.system
    commands have to be modified accordingly
"""

opts = get_args()

#f = open(opts['file'], 'a')
#file = f.readlines()

for item in os.listdir(opts['dir']):
    if '.png' in item and item[1] is not '_':#any(item in line for line in file):
        os.system(join(opts['dir'], item))
        print('False marker: 0, White: 1, Yellow: 2')
        label = int(input('select label for %s: ' % item))
        shutil.move(join(opts['dir'], item), join(opts['dir'], '%d_' % (label) + item))
        #f.write('%s,%d\n' % (item, label))
        os.system('taskkill /f /im Microsoft.Photos.exe')

print('No more images to label in this folder')
