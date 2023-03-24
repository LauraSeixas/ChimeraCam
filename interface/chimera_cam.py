from PyQt5.QtGui import QImage, QPixmap
from .video_face_track import VideoFaceTrack
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget

class ChimeraCam(QMainWindow):
    def __init__(self, window_width: int):
        super().__init__()

        self.window_name: str = "ChimeraCam"

        # LARGURA DOS WIDGETS
        self.widgets_width: int = window_width

        # TELA DO VÍDEO
        self.video_screen: QLabel = QLabel()
        self.video_screen.setFixedSize(self.widgets_width, self.widgets_width)
        self.video_screen.setStyleSheet('background-color: black;')

        # INICIALIZAÇÃO DO FACE TRACK
        self.thread_is_running: bool = False
        self.face_tracking: VideoFaceTrack = VideoFaceTrack(self.widgets_width)

        # LIGA/DESLIGA O FACE TRACKING
        self.switch_button: QPushButton = QPushButton()
        self.switch_button.setText('\u25B6')
        self.switch_button.setFixedSize(50, 50)
        self.switch_button.setStyleSheet('background-color: red; color: #FFFFFF; font-size: 50px; border: none; border-radius: 24px;')
        self.switch_button.clicked.connect(self.operate_tracking)

        # BLOCO DO SWITCH-BUTTON
        self.layout_switch_button: QHBoxLayout = QHBoxLayout()
        self.layout_switch_button.addWidget(self.switch_button)
        self.widget_switch_button: QWidget = QWidget()
        self.widget_switch_button.setLayout(self.layout_switch_button)
        self.widget_switch_button.setFixedSize(self.widgets_width, 65)

        # LISTA A IDADE DAS PESSOAS RASTREADAS
        self.list_tracked_face_data: QListWidget = QListWidget()
        self.list_tracked_face_data.setFixedSize(self.widgets_width, 150)
        self.list_tracked_face_data.setStyleSheet('font: 12pt Arial; font-weight: bold; background-color: white; border: 2px solid lightgray; border-radius: 10px')

        # BOTÕES DE AÇÃO DO APLICATIVO
        self.block_car_button: QPushButton = QPushButton()
        self.block_car_button.setText("BLOQUEAR")
        self.block_car_button.setStyleSheet("color: #FFFFFF; font-weight: bold; background-color: #3F95D3; border-radius: 10px; border: 1px solid #FFFFFF;")

        self.roll_down_car_window: QPushButton = QPushButton()
        self.roll_down_car_window.setText("BAIXAR VIDROS")
        self.roll_down_car_window.setStyleSheet("color: #FFFFFF; font-weight: bold; background-color: #3F95D3; border-radius: 10px; border: 1px solid #FFFFFF;")

        self.open_car_button: QPushButton = QPushButton()
        self.open_car_button.setText("ABRIR CARRO")
        self.open_car_button.setStyleSheet("color: #FFFFFF; font-weight: bold; background-color: #3F95D3; border-radius: 10px; border: 1px solid #FFFFFF;")

        self.register_button: QPushButton = QPushButton()
        self.register_button.setText("CADASTRO")
        self.register_button.setStyleSheet("color: #FFFFFF; font-weight: bold; background-color: #533FD3; border-radius: 10px; border: 1px solid #FFFFFF;")

        self.alarm_button: QPushButton = QPushButton()
        self.alarm_button.setText("ALARME")
        self.alarm_button.setStyleSheet("color: #FFFFFF; font-weight: bold; background-color: #D33F3F; border-radius: 10px; border: 1px solid #FFFFFF;")

        # PRIMEIRO BLOCO HORIZONTAL DE BOTÕES
        self.first_action_buttons: QWidget = QWidget()
        self.first_action_buttons_layout: QHBoxLayout = QHBoxLayout()
        self.first_action_buttons.setLayout(self.first_action_buttons_layout)
        self.first_action_buttons_layout.addWidget(self.block_car_button)
        self.first_action_buttons_layout.addWidget(self.roll_down_car_window)

        # SEGUNDO BLOCO HORIZONTAL DE BOTÕES
        self.second_action_buttons: QWidget = QWidget()
        self.second_action_buttons_layout: QHBoxLayout = QHBoxLayout()
        self.second_action_buttons.setLayout(self.second_action_buttons_layout)
        self.second_action_buttons_layout.addWidget(self.open_car_button)
        self.second_action_buttons_layout.addWidget(self.register_button)

        # BLOCO VERTICAL PRINCIPAL
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.addWidget(self.video_screen)
        self.layout.addWidget(self.widget_switch_button)
        self.layout.addWidget(self.list_tracked_face_data)
        self.layout.addWidget(self.first_action_buttons)
        self.layout.addWidget(self.second_action_buttons)
        self.layout.addWidget(self.alarm_button)

        # CORPO DA JANELA CHIMERACAM
        self.body: QWidget = QWidget()
        self.body.setLayout(self.layout)
        self.body.setStyleSheet('background-color: #3E3A3A; padding: 10px 10px')

        # MONTAGEM DA JANELA DO APP
        self.setWindowTitle(self.window_name)
        self.setCentralWidget(self.body)
        self.move(500, 0)

    def operate_tracking(self) -> None:
        if not self.thread_is_running:
            self.thread_is_running = True
            self.face_tracking.start()
            self.face_tracking.image_signal.connect(self.refresh_video_screen)
            self.face_tracking.face_data_signal.connect(self.refresh_face_data_list)
            self.switch_button.setText('\u25A0')
        else:
            self.thread_is_running = False
            self.face_tracking.stop()
            self.face_tracking.image_signal.disconnect()
            self.face_tracking.face_data_signal.disconnect()
            self.switch_button.setText('\u25B6')
            self.video_screen.setPixmap(QPixmap(""))
            self.list_tracked_face_data.clear()
            
    def refresh_video_screen(self, tracked_image: QImage) -> None:
        self.video_screen.setPixmap(QPixmap.fromImage(tracked_image))

    def refresh_face_data_list(self, face_data: list) -> None:
        self.list_tracked_face_data.clear()
        self.list_tracked_face_data.addItems(face_data)
    
    def CloseChimeraCam(self) -> None:
        self.close()
