import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage

Matrix = np.ndarray[int, np.dtype[np.generic]]

class VideoFaceTrack(QThread):
    image_signal: pyqtSignal = pyqtSignal(QImage)
    face_data_signal: pyqtSignal = pyqtSignal(int)
    face_data_atributo_teste = 0 # atributo de teste

    def __init__(self, widgets_width: int) -> None:
        super().__init__()
        # LARGURA DO VÍDEO
        self.video_width: int = widgets_width

    def run(self) -> None:   # função herdada de Qthread e iniciada com o método .start()
        self.thread_running: bool = True
        try: 
            snapshotting = cv2.VideoCapture(0)    # arg(0): Captura imagens da webcam;   arg("./path/to/video.mp4"): captura imagens de um vídeo
        except Exception:
            print(Exception)
            self.thread_running = False
        else:
            while self.thread_running:
                ret, frame = snapshotting.read()                
                if ret:
                    frame: np.ndarray = self.set_new_frame_shape(frame, self.video_width)
                    cv2_image: Matrix = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    """ Inserir método/classe de rastreio de face. Atribuir o método/classe a uma variável, por exemplo, cv2TrackedImage """
                    qt_image: QImage = self.qt_image_generator(cv2_image, self.video_width)  # o arg cv2Image deve ser substituido pela imagem resultande do rastreio, a cv2TrackedImage
                    tracked_face_data = self.face_data_modeler(self.face_data_atributo_teste)  # o arg self.faceDataAtributoTeste é só para testes, ele dever ser substituido pelos dados das faces rastreadas
                    self.emit_signals(qt_image, tracked_face_data)
        finally:
            snapshotting.release()

    def stop(self) -> None:
        self.thread_running = False
        self.quit()

    def set_new_frame_shape(self, frame: np.ndarray, video_width: int) -> np.ndarray:
        start: int = int(np.shape(frame)[1]/2 - video_width*2/3)
        end: int = int(np.shape(frame)[1]/2 + video_width*2/3)
        new_frame: np.ndarray = frame[:, start:end, :]    # muda o shape de (480, 640, 3) para (480, 480, 3), depende da webcam
        return new_frame
    
    def qt_image_generator(self, tracked_image: Matrix, video_width: int) -> QImage:
        qt_image: QImage = QImage(tracked_image.data, tracked_image.shape[1], tracked_image.shape[0], QImage.Format_RGB888)
        return qt_image.scaled(video_width, video_width, Qt.KeepAspectRatio)
    
    def face_data_modeler(self, face_data):
        self.face_data_atributo_teste += 1   # atributo de teste
        """ Aqui deve ser feita a formatação dos dados de faces coletados. 
            O ideal é retornar uma lista com os dados das faces por pessoa """
        return face_data
    
    def emit_signals(self, qt_image: QImage, face_data) -> None:
        self.image_signal.emit(qt_image)
        self.face_data_signal.emit(face_data)