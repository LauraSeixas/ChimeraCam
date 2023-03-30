import os
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from face_track import FaceTrack

_CHIMERACAMPATH = os.path.dirname(os.path.dirname(__file__))
Mat = np.ndarray[int, np.dtype[np.generic]]

class Register(QThread):
    register_signal: pyqtSignal = pyqtSignal(QImage)

    def __init__(self, widgets_width: int) -> None:
        super().__init__()
        self.video_width: int = widgets_width
        self.register = FaceTrack()
        self.user_name: str = ""
        self.thread_running: bool = False

    def run(self) -> None:
        self.thread_running = True
        try: 
            if not os.path.exists(f'{_CHIMERACAMPATH}/face_track/images/{self.user_name}'):
                os.makedirs(f'{_CHIMERACAMPATH}/face_track/images/{self.user_name}')
            snapshotting = cv2.VideoCapture(0)
        except Exception:
            self.thread_running = False
            raise IOError("Não foi possível iniciar a captura")
        else:
            count = 0
            intervalo = 2
            fps = 30
            count_cadastro = 1

            while self.thread_running:
                ret, frame = snapshotting.read()
                if ret:
                    square_frame: np.ndarray = self.set_square_shape_frame(frame)
                    cv2_image: Mat = cv2.cvtColor(square_frame, cv2.COLOR_BGR2RGB)
                    qt_image: QImage = self.qt_image_generator(cv2_image, self.video_width)
                    self.register_signal.emit(qt_image)

                    if count > 5 and (count % (intervalo * fps) == 0 and count_cadastro <= 5):
                        faces = self.register.detect_faces(frame)
                        if faces:
                            cv2.imwrite(f'{_CHIMERACAMPATH}/face_track/images/{self.user_name}/{count_cadastro}.jpg', frame)
                            print(f'Imagem {count_cadastro} capturada')
                        count_cadastro += 1
                count += 1
                if count_cadastro > 5:
                    self.stop()
        finally:
            snapshotting.release()
            self.register.retrain()

    def stop(self) -> None:
        self.thread_running = False
        white = np.full((1000, 1000, 3), 50, dtype = np.uint8)
        cv2image: Mat = cv2.cvtColor(white, cv2.COLOR_BGR2RGB)
        qtimage: QImage = self.qt_image_generator(cv2image, self.video_width)
        self.register_signal.emit(qtimage)
        self.register_signal.disconnect()
        self.quit()
        
    
    def set_square_shape_frame(self, frame: np.ndarray) -> np.ndarray:
        if np.shape(frame)[0] < np.shape(frame)[1]:
            start: int = (np.shape(frame)[1] - np.shape(frame)[0]) // 2
            end: int = np.shape(frame)[1] - start
            new_frame: np.ndarray = frame[:, start:end, :]
        else:
            start = (np.shape(frame)[0] - np.shape(frame)[1]) // 2
            end = np.shape(frame)[0] - start
            new_frame = frame[start:end, :, :]
        return new_frame
    
    def qt_image_generator(self, image: Mat, video_width: int) -> QImage:
        qt_image: QImage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        return qt_image.scaled(video_width, video_width, Qt.KeepAspectRatio)
        