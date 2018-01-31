import cv2 as cv
import tensorflow as tf
import numpy as np

import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3";
	
image = cv.imread("clouds.jpg");
cv.imshow("Clouds", image);
cv.waitKey(0);
cv.destroyAllWindows();

	
	

	
	
	
	
wait = input("Press enter to continue");