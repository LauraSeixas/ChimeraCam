import cv2
import numpy as np

# ------------ Model for Age detection --------#
age_weights = "../models/age_detection/age_deploy.prototxt"
age_config = "../models/age_detection/age_net.caffemodel"
age_Net = cv2.dnn.readNet(age_config, age_weights)

# Model requirements for image
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
model_mean = (78.4263377603, 83.7689143744, 114.895847746)

video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('../opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faces_sliced = []
face_coordinates = []
while True:
    ret, frame = video.read()
    frame_tr = np.asarray(frame, dtype=np.uint8)
    gray_image = cv2.cvtColor(frame_tr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=9)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame_tr, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_coordinates.append([x,y, x + w, y + h])
        face = frame_tr[y:y+h, x:x+w]
        faces_sliced.append(face)
        # ----- Image preprocessing --------#
        blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), model_mean, swapRB=False
            )
        # -------Age Prediction---------#
        age_Net.setInput(blob)
        age_preds = age_Net.forward()
        age = ageList[age_preds[0].argmax()]
        cv2.putText(frame_tr, f'Age:{age}', (x,
                                            y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('test', frame_tr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()