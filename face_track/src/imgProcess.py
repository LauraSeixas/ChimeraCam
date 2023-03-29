from os.path import dirname
import cv2
import numpy as np
import tensorflow as tf
from keras_facenet import FaceNet
import pickle

class FaceTrack:
    _ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    _model_mean = (78.4263377603, 83.7689143744, 114.895847746)
    BASE_DIR = dirname(dirname(__file__))
    def __init__(
                self, 
                age_config = 'age_net.caffemodel',
                age_weights = 'age_deploy.prototxt'
            ):
        model_src = f"{self.BASE_DIR}/models/"

        age_config = model_src + age_config
        age_weights = model_src + age_weights

        self.age_model = cv2.dnn.readNet(age_config, age_weights)
        self.face_model = FaceNet()
        self.labels = self.get_labels()
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(f"{model_src}/trainner.yml")

    def get_labels(self):
        with open(f"{self.BASE_DIR}/models/labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            ## reverting the labels to be id: label, instead of label:id
            labels = {v:k for k,v in og_labels.items()}
            return labels

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
    
    def recognize_face(self, face):
        roi_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        id_, conf = self.recognizer.predict(roi_gray)
        if conf > 0.6:
            return self.labels[id_]
        else:
            return "desconhecido"
    
    def process_img(self, img):
        faces = self.detect_faces(img)
        persons = []
        for face in faces:
            x, y, w, h = face['box']
            if face['confidence'] > 0.7:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = img[y:y+h, x:x+w]
            
            identification = self.recognize_face(face)
            age = self.detect_age(face)
            credentials = {
                "face" : [x,y,w,h],
                "age" : age,
                "identification": identification
            }
            persons.append(credentials)
            cv2.putText(img, f'Age:{age}, name: {identification}', (x,
                                                y - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 255), 2, cv2.LINE_AA)

        return img, persons