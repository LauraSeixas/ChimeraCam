from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget
from .video_face_track import VideoFaceTrack

class ChimeraCam(QMainWindow):
    def __init__(self, window_width: int):
        super().__init__()

        self.window_name: str = "ChimeraCam"

        # LARGURA DOS WIDGETS
        self.widgets_width: int = window_width

        # TELA DO VÍDEO
        self.video_screen: QLabel = QLabel()
        self.video_screen.setFixedSize(self.widgets_width, self.widgets_width)
        self.video_screen.setStyleSheet('QLabel {background-color: black}')

        # INICIALIZAÇÃO DO FACE TRACK
        self.thread_is_running: bool = False
        self.face_tracking: VideoFaceTrack = VideoFaceTrack(self.widgets_width)

        # LIGA/DESLIGA O FACE TRACKING
        self.switcht_button: QPushButton = QPushButton()
        self.switcht_button.setText('PLAY')
        self.switcht_button.setFixedSize(100, 50)
        self.switcht_button.setStyleSheet('QPushButton {background-color: red; color: white; font-weight: bold; font-size: 25px; border-radius: 10px}')
        self.switcht_button.clicked.connect(self.operate_tracking)

        # BLOCO DO SWITCH-BUTTON
        self.layout_switch_button: QHBoxLayout = QHBoxLayout()
        self.layout_switch_button.addWidget(self.switcht_button)
        self.widget_switch_button: QWidget = QWidget()
        self.widget_switch_button.setLayout(self.layout_switch_button)
        self.widget_switch_button.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.widget_switch_button.setStyleSheet('QWidget {}')

        # LISTA A IDADE DAS PESSOAS RASTREADAS
        self.list_tracked_face_data: QListWidget = QListWidget()
        self.list_tracked_face_data.setFixedSize(self.widgets_width, 150)
        self.list_tracked_face_data.setStyleSheet('QListWidget {font: 12pt Arial; font-weight: bold; padding: 7; background-color: white; border: 2px solid lightgray; border-radius: 10px}')

        # BLOCO VERTICAL PRINCIPAL
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.addWidget(self.video_screen)
        self.layout.addWidget(self.widget_switch_button)
        self.layout.addWidget(self.list_tracked_face_data)

        # CORPO DA JANELA CHIMERACAM
        self.body: QWidget = QWidget()
        self.body.setLayout(self.layout)
        self.body.setStyleSheet('QWidget {background-color: lightblue;}')

        # MONTAGEM DA JANELA DO APP
        self.setWindowTitle(self.window_name)
        self.setGeometry(760, 100, self.widgets_width+22, 740)
        self.setFixedSize(self.widgets_width+22, 740)
        self.setCentralWidget(self.body)

    def operate_tracking(self) -> None:
        if not self.thread_is_running:
            self.thread_is_running = True
            self.face_tracking.start()
            self.face_tracking.image_signal.connect(self.refresh_video_screen)
            self.face_tracking.face_data_signal.connect(self.refresh_face_data_list)
            self.switcht_button.setText('STOP')
        else:
            self.thread_is_running = False
            self.face_tracking.stop()
            self.face_tracking.image_signal.disconnect()
            self.face_tracking.face_data_signal.disconnect()
            self.switcht_button.setText('PLAY')

    def refresh_video_screen(self, tracked_image: QImage) -> None:
        self.video_screen.setPixmap(QPixmap.fromImage(tracked_image))

    def refresh_face_data_list(self, face_data: list) -> None:
        self.list_tracked_face_data.clear()
        self.list_tracked_face_data.addItems(face_data)
    
    def CloseChimeraCam(self) -> None:
        self.close()