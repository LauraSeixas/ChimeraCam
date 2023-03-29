import os
import cv2
import numpy as np
import tensorflow as tf
from keras_facenet import FaceNet
import pickle

class FaceTrack:
    _ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
           '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    _model_mean = (78.4263377603, 83.7689143744, 114.895847746)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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

    def retrain(self):
        ### Need to install pip install opencv-contrib-python
        image_dir = os.path.join(self.BASE_DIR, "images")
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

                    faces = self.detect_faces(img)
                    for face in faces:
                        x,y,w,h = face['box']

                        if face['confidence'] > 0.7:
                            roi = img[y:y+h, x:x+w]
                            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                            x_train.append(roi_gray)
                            y_labels.append(id_)

        models_dir = os.path.join(self.BASE_DIR, "models")
        with open(f"{models_dir}/labels.pickle", "wb") as f:
            pickle.dump(label_ids, f)

        self.recognizer.train(x_train, np.array(y_labels))
        self.recognizer.save(f"{models_dir}/trainner.yml")

    def registration(self, name):
        # Criar a pasta "imagens com o nome da pessoa que está se cadastrando" se ela não existir
        if not os.path.exists(f'{self.BASE_DIR}/images/{name}'):
            os.makedirs(f'{self.BASE_DIR}/images/{name}')
        cap = cv2.VideoCapture(0)

        # Verificar se a webcam foi aberta corretamente
        if not cap.isOpened():
            raise IOError("Não foi possível abrir a webcam")

        # Inicializa o contador de imagens capturadas
        count = 0
        intervalo = 2  # segundos
        fps = 30
        count_cadastro = 1
        # Loop para captura de frames da webcam
        while True:
            ret, frame = cap.read()

            # Mostrar o frame na janela
            # cv2.imshow('Webcam', frame)

            # Verificar se o tempo de intervalo passou para capturar uma nova imagem
            if count > 5 and (count % (intervalo * fps) == 0 and count_cadastro <= 5):
                # Captura a imagem e salva em um arquivo

                faces = self.detect_faces(frame)
                if faces:
                    cv2.imwrite('{}/images/{}/{}.jpg'.format(self.BASE_DIR, name, count_cadastro), frame)
                    print('Imagem {} capturada'.format(count_cadastro))
                count_cadastro += 1
            elif count_cadastro > 5:
                break
            # Incrementa o contador de imagens capturadas
            count += 1

            # Espera por uma tecla (1 milissegundo), aperte "q" quando quiser parar a captura 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Encerra o loop quando 5 imagens foram capturadas
            if count_cadastro > 5:
                break


        #Finaliza a captura de vídeo
        cap.release()
        # cv2.destroyAllWindows()
        self.retrain()


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
            if face['confidence'] > 0.9:
                print(face['confidence'])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = img[y:y+h, x:x+w]
            
            identification = self.recognize_face(face)
            print(identification)
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