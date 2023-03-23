from sys import path
from os.path import dirname
path.append(dirname(dirname(__file__)))
import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from face_track import FaceTrack

face_track = FaceTrack('age_net.caffemodel', 'age_deploy.prototxt')

Matrix = np.ndarray[int, np.dtype[np.generic]]

class VideoFaceTrack(QThread):
    image_signal: pyqtSignal = pyqtSignal(QImage)
    face_data_signal: pyqtSignal = pyqtSignal(list)

    def __init__(self, widgets_width: int) -> None:
        super().__init__()
        # LARGURA DO VÍDEO
        self.video_width: int = widgets_width

    def run(self) -> None:
        self.thread_running: bool = True
        try: 
            snapshotting = cv2.VideoCapture(0)
        except Exception:
            print(Exception)
            self.thread_running = False
        else:
            while self.thread_running:
                ret, frame = snapshotting.read()                
                if ret:
                    frame: np.ndarray = self.set_new_frame_shape(frame, self.video_width)
                    cv2_image: Matrix = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    cv2_tracked_image, face_data = face_track.process_img(cv2_image)
                    qt_image: QImage = self.qt_image_generator(cv2_tracked_image, self.video_width)
                    tracked_face_data: list = self.face_data_modeler(face_data)
                    self.emit_signals(qt_image, tracked_face_data)
        finally:
            snapshotting.release()

    def stop(self) -> None:
        self.thread_running = False
        self.quit()

    def set_new_frame_shape(self, frame: np.ndarray, video_width: int) -> np.ndarray:
        start: int = int(np.shape(frame)[1]/2 - video_width*2/3)
        end: int = int(np.shape(frame)[1]/2 + video_width*2/3)
        new_frame: np.ndarray = frame[:, start:end, :]
        return new_frame
    
    def qt_image_generator(self, tracked_image: Matrix, video_width: int) -> QImage:
        qt_image: QImage = QImage(tracked_image.data, tracked_image.shape[1], tracked_image.shape[0], QImage.Format_RGB888)
        return qt_image.scaled(video_width, video_width, Qt.KeepAspectRatio)
    
    def face_data_modeler(self, face_data: list) -> list:
        if len(face_data) > 0:
            face_data_list: list = []
            for item in face_data:
                person: str = item["age"].replace("(","").replace(")","")
                face_data_str: str = f"Anônimo, idade: {person}"
                face_data_list.append(face_data_str)
            return face_data_list
        else:
            return ["Nenhuma pessoa detectada"]
    
    def emit_signals(self, qt_image: QImage, face_data: list) -> None:
        self.image_signal.emit(qt_image)
        self.face_data_signal.emit(face_data)