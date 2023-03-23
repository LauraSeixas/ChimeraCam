import cv2
import numpy as np
from keras_facenet import FaceNet
import tensorflow as tf
from typing import List, Tuple
from imgProcess import FaceTrack

chimera = FaceTrack('age_net.caffemodel', 'age_deploy.prototxt')
#getting image and transforming
img = cv2.imread('../test_imgs/test2.jpg')
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
image, persons = chimera.process_img(image)
print(persons)

cv2.imshow('test', image)
cv2.waitKey(0)
cv2.destroyAllWindows()