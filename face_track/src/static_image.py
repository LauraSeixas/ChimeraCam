import cv2
from PIL import Image
import numpy as np

#getting image and transforming
image = Image.open('../test_imgs/_bb.jpg')
image_tr = np.asarray(image, dtype=np.uint8)
# image_tr = cv2.resize(image_tr, (720, 640))
gray_image = cv2.cvtColor(image_tr, cv2.COLOR_BGR2GRAY)

# ------------ Model for Face detection --------#
face_cascade = cv2.CascadeClassifier('../opencv/data/haarcascades/haarcascade_frontalface_default.xml')

# ------------ Model for Age detection --------#
# age_weights = "../models/age_detection/age_deploy.prototxt"
# age_config = "../models/age_detection/age_net.caffemodel"

#### try 2
age_weights = "../models/age_detection/deploy_age2.prototxt"
age_config = "../models/age_detection/age_net2.caffemodel"
age_Net = cv2.dnn.readNet(age_config, age_weights)

# Model requirements for image
# ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
#            '(25-32)', '(38-43)', '(48-53)', '(60-100)']
ageList=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
model_mean = (78.4263377603, 83.7689143744, 114.895847746)


# --------------------------------------------------------- #
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.03, minNeighbors=6)
face_coordinates = []
faces_sliced = []
# obtaining coordinates of each face
for (x, y, w, h) in faces:
    cv2.rectangle(image_tr, (x, y), (x+w, y+h), (0, 255, 0), 2)
    face_coordinates.append([x,y, x + w, y + h])
    face = image_tr[y:y+h, x:x+w]
    faces_sliced.append(face)
    # ----- Image preprocessing --------#
    blob = cv2.dnn.blobFromImage(
            face, 1.0, (227, 227), model_mean, swapRB=False
        )
    # -------Age Prediction---------#
    age_Net.setInput(blob)
    age_preds = age_Net.forward()
    age = ageList[age_preds[0].argmax()]
    cv2.putText(image_tr, f'Age:{age}', (x,
                                        y - 10), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (0, 255, 255), 2, cv2.LINE_AA)


cv2.imshow('test', image_tr)
cv2.waitKey(0)
cv2.destroyAllWindows()