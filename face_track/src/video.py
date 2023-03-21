import cv2
import numpy as np
from keras_facenet import FaceNet
import tensorflow as tf
class ChimeraCam:
    _ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    _model_mean = (78.4263377603, 83.7689143744, 114.895847746)

    def __init__(self, age_config, age_weights):
        age_model_src = '../models/age_detection/'

        age_config = age_model_src + age_config
        age_weights = age_model_src + age_weights

        self.age_model = cv2.dnn.readNet(age_config, age_weights)
        self.face_model = FaceNet()

    def detect_faces(self,img):
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
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame_tr = np.asarray(frame, dtype=np.uint8)
    faces = chimera.detect_faces(frame_tr)
    
    # print(faces)
    for face in faces:
        x, y, w, h = face['box']
        if face['confidence'] > 0.7:
            cv2.rectangle(frame_tr, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face = frame_tr[y:y+h, x:x+w]

        age = chimera.detect_age(face)
        cv2.putText(frame_tr, f'Age:{age}', (x,
                                            y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('test', frame_tr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()