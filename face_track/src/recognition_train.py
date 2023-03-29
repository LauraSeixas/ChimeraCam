import os
import numpy as np
from PIL import Image
import cv2
import pickle
from imgProcess import FaceTrack

face_track = FaceTrack()
### Need to install pip install opencv-contrib-python

image_dir = f"{os.path.dirname(os.path.dirname(__file__))}\images/"
recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0

## id labels for the images
label_ids = {}

# The name of the labels
y_labels = []
# Detected faces in gray
x_train = []
detected = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if (
            file.endswith("png") or
            file.endswith("jpg") or
            file.endswith("jpeg")
        ):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            
            id_ = label_ids[label]
            pil_image = Image.open(path).convert("L")
            # the normalized size to the images being processed
            base_size = (550, 550)
            # resizing image
            final_image = pil_image.resize(base_size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            faces = face_track.detect_faces(image_array)
            for face in faces:
                x,y,w,h = face['box']
                detected.append({'label': label, 'file': file})

                if face['confidence'] > 0.7:
                    print(f"image {file} detected from {label}")
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

print(label_ids)
print(len(x_train))
print(detected)
print(y_labels)