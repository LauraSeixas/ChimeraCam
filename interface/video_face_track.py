import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from face_track import FaceTrack

Mat = np.ndarray[int, np.dtype[np.generic]]

class VideoFaceTrack(QThread):
    image_signal: pyqtSignal = pyqtSignal(QImage)
    face_data_signal: pyqtSignal = pyqtSignal(list)
    child_alert: pyqtSignal = pyqtSignal(str)

    def __init__(self, widgets_width: int) -> None:
        super().__init__()
        self.video_width: int = widgets_width
        self.face_track = FaceTrack()

    def run(self) -> None:
        self.thread_running: bool = True
        try: 
            snapshotting = cv2.VideoCapture(0)
            #snapshotting.open("https://10.0.0.104:8080/video")
        except Exception:
            print(Exception)
            self.thread_running = False
        else:
            while self.thread_running:
                ret, frame = snapshotting.read()                
                if ret:
                    square_frame: np.ndarray = self.set_square_shape_frame(frame)
                    cv2_image: Mat = cv2.cvtColor(square_frame, cv2.COLOR_BGR2RGB)
                    cv2_tracked_image, face_data = self.face_track.process_img(cv2_image)
                    qt_image: QImage = self.qt_image_generator(cv2_tracked_image, self.video_width)
                    tracked_face_data: list = self.face_data_modeler(face_data)
                    self.emit_signals(qt_image, tracked_face_data)
        finally:
            snapshotting.release()

    def stop(self) -> None:
        self.thread_running = False
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
    
    def qt_image_generator(self, tracked_image: Mat, video_width: int) -> QImage:
        qt_image: QImage = QImage(tracked_image.data, tracked_image.shape[1], tracked_image.shape[0], QImage.Format_RGB888)
        return qt_image.scaled(video_width, video_width, Qt.KeepAspectRatio)
    
    def face_data_modeler(self, face_data: list) -> list:
        if len(face_data) > 0:
            face_data_list: list = []
            for item in face_data:
                user: str = item["identification"]
                age: str = item["age"].replace("(","").replace(")","").replace("-"," a ")
                face_data_list.append(f"{user}, idade aprox. {age} anos")

                if age == "0 a 2" or age == "4 a 6" or age == "8 a 12":
                    self.child_alert.emit("Criança detecatada!")
                else:
                    self.child_alert.emit("Nenhuma criança detecatada!")
            return face_data_list
        else:
            return ["Nenhuma pessoa detectada"]
    
    def emit_signals(self, qt_image: QImage, face_data: list) -> None:
        self.image_signal.emit(qt_image)
        self.face_data_signal.emit(face_data)