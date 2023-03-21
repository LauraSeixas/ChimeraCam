import cv2
import numpy as np
from keras_facenet import FaceNet
import tensorflow as tf
from typing import List, Tuple
class ChimeraCam:
    _ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    _model_mean = (78.4263377603, 83.7689143744, 114.895847746)

    def __init__(self, age_config: str, age_weights: str) -> None:
        age_model_src = '../models/age_detection/'

        age_config = age_model_src + age_config
        age_weights = age_model_src + age_weights

        self.age_model = cv2.dnn.readNet(age_config, age_weights)
        self.face_model = FaceNet()

    def detect_faces(self,img: np.ndarray) -> List[dict]:
        converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = self.face_model.extract(converted_img, threshold=0.8)

        return faces
    
    def detect_age(self, face):
        blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), self._model_mean, swapRB=False
        )
        self.age_model.setInput(blob)
        age_preds = self.age_model.forward()
        age = self._ageList[age_preds[0].argmax()]
        return age
    
chimera = ChimeraCam('age_net.caffemodel', 'age_deploy.prototxt')
#getting image and transforming
img = cv2.imread('../test_imgs/test2.jpg')
image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
faces = chimera.detect_faces(image)
print(faces)
# obtaining coordinates of each face
for face in faces:
    x, y, w, h = face['box']
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    face = image[y:y+h, x:x+w]
    
    age = chimera.detect_age(face)
    cv2.putText(image, f'Age:{age}', (x,
                                        y - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 255, 255), 2, cv2.LINE_AA)

cv2.imshow('test', image)
cv2.waitKey(0)
cv2.destroyAllWindows()