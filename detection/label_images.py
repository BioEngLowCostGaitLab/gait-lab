import os
from os.path import join
from PIL import Image
import matplotlib.pyplot as plt
from time import time

cwd = os.getcwd()

f = open('labels_%d.txt' % int(time()), 'w')

for item in os.listdir(cwd):
    if '.png' in item:
        os.system(item)
        label = int(raw_input('select label for %s: ' % item))
        f.write('%s,%d\n' % (item, label))
        os.rename(join(cwd, item), join(cwd, item.split('.')[0]) + '_done.png')
