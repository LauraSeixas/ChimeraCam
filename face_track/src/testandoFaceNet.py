import cv2
import numpy as np
from keras_facenet import FaceNet
import tensorflow as tf

# Carregar a rede FaceNet
model = FaceNet()

# Carregar imagem
img = cv2.imread('../test_imgs/test.jpeg')
imagem = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(imagem.shape)

# Detectar faces na imagem
faces = model.extract(imagem, threshold=0.7)

# Mostrar o número de faces detectadas
print(f'Foram detectadas {len(faces)} faces.')

# Mostrar as coordenadas das caixas delimitadoras das faces
for face in faces:
    x1, y1, x2, y2 = face['box']

    # Expandir as caixas delimitadoras para cobrirtodo o rosto
    y1 = max(0, y1 - 10)
    y2 = min(imagem.shape[0], y2 + 10)
    x1 = max(0, x1 - 10)
    x2 = min(imagem.shape[1], x2 + 10)
    print(f'Face encontrada nas coordenadas ({x1}, {y1}), ({x2}, {y2})')

    # Mostrar as caixas delimitadoras das faces
    cv2.rectangle(imagem, (x1, y1), (x1 + x2, y1 + y2), (0, 255, 0), 2)

cv2.imshow('Imagem com faces detectadas', imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()


