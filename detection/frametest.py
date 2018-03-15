import cv2
import sys
from time import sleep

cap1 = cv2.VideoCapture(sys.argv[1])
cap2 = cv2.VideoCapture(sys.argv[2])
n_frame = 0
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    input()
    sys.stdout.write('\r%d' % n_frame)
    sys.stdout.flush()
    cv2.imshow("out1", cv2.resize(frame1, (640, 360)))
    cv2.imshow("out2", cv2.resize(frame2, (640, 360)))
    n_frame += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
