import cv2
import numpy as np
from keras_facenet import FaceNet
import tensorflow as tf
from typing import List, Tuple
from imgProcess import FaceTrack
import os

chimera = FaceTrack('age_net.caffemodel', 'age_deploy.prototxt')
#getting image and transforming
path = f"{os.path.dirname(os.path.dirname(__file__))}/images/"
img = cv2.imread(f'{path}gabi/2.jpeg')
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
image, persons = chimera.process_img(image)
print(persons)

cv2.imshow('test', image)
cv2.waitKey(0)
cv2.destroyAllWindows()