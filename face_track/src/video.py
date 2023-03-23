import cv2
import numpy as np
import tensorflow as tf
from imgProcess import FaceTrack

chimera = FaceTrack('age_net.caffemodel', 'age_deploy.prototxt')
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame_tr = np.asarray(frame, dtype=np.uint8)
    frame_tr, persons = chimera.process_img(frame_tr)
    cv2.imshow('test', frame_tr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()