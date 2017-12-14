import os
from os.path import join
"""
    Data labeling tool for Windows. For other operating systems, the os.system
    commands have to be modified accordingly
"""
cwd = os.getcwd()

f = open('labels_%d.txt' % int(time()), 'w')

for item in os.listdir(cwd):
    if '.png' in item:
        os.system(item)
        label = int(raw_input('select label for %s: ' % item))
        f.write('%s,%d\n' % (item, label))
        os.system('taskkill /f /im Microsoft.Photos.exe')
