import os
import numpy as np
from PIL import Image
import cv2
import pickle
from imgProcess import FaceTrack

face_track = FaceTrack()
### Need to install pip install opencv-contrib-python
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
image_dir = os.path.join(BASE_DIR, "images")
recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0

## id labels for the images
label_ids = {}

# The name of the labels
y_labels = []
# Detected faces in gray
x_train = []

for root, dirs, files in os.walk(image_dir):

    for file in files:
        print(f'testing {file}')
        if (
            file.endswith("png") or
            file.endswith("jpg") or
            file.endswith("jpeg")
        ):
            print(f'{file} has passed')
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            
            id_ = label_ids[label]
            # pil_image = Image.open(path).convert("L")
            img = cv2.imread(path)

            ###################################################################
            #### here is using pill, and recising, but i get some error in the model
            # the normalized size to the images being processed
            # base_size = (550, 550)
            # resizing image
            # final_image = pil_image.resize(base_size, Image.ANTIALIAS)
            # image_array = np.array(final_image, "uint8")
            ###################################################################

            faces = face_track.detect_faces(img)
            for face in faces:
                x,y,w,h = face['box']

                if face['confidence'] > 0.7:
                    roi = img[y:y+h, x:x+w]
                    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    x_train.append(roi_gray)
                    y_labels.append(id_)

models_dir = os.path.join(BASE_DIR, "models")
with open(f"{models_dir}/labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save(f"{models_dir}/trainner.yml")
