from PyQt5.QtGui import QImage, QPixmap
from .video_face_track import VideoFaceTrack
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget

class Screen(QLabel):
    css_style: str = """
    Screen {
        background-color: #2E2A2A;
    }
    """
    def __init__(self, widgets_width):
        super().__init__()
        self.setFixedSize(widgets_width, widgets_width)
        self.setStyleSheet(self.css_style)

class PlayButton(QPushButton):
    css_style: str = """
    PlayButton {
        background-color: #FF0000; 
        color: #FFFFFF; 
        border: none; 
        font-size: 50px; 
        border-radius: 24px
    }
    """
    def __init__(self):
        super().__init__()
        self.setText('\u25B6')
        self.setFixedSize(50, 50)
        self.setStyleSheet(self.css_style)

class FaceData(QListWidget):
    css_style: str = """
    FaceData {
        font: 12pt Arial; 
        font-weight: bold; 
        background-color: white; 
        border: 2px solid lightgray; 
        border-radius: 10px
    }
    """
    def __init__(self, widgets_width):
        super().__init__()
        self.setFixedSize(widgets_width, 150)
        self.setStyleSheet(self.css_style)

class ActionButton(QPushButton):
    css_style = """
    ActionButton {
        color: #FFFFFF;
        font-weight: bold;
        background-color: bgcolor;
        border-radius: 10px;
        border: 1px solid #FFFFFF;
    }
    """
    def __init__(self, btn_name, bg_color):
        super().__init__()
        self.setText(btn_name)
        self.setStyleSheet(self.css_style.replace("bgcolor", bg_color))

    

class UserInterface(QMainWindow):
    def __init__(self, window_width):
        super().__init__()

        self.window_name: str = "ChimeraCam"

        self.widgets_width: int = window_width

        self.video_screen: Screen = Screen(self.widgets_width)

        self.play_button: PlayButton = PlayButton()

        self.face_data_list: FaceData = FaceData(self.widgets_width)

        self.block_car_button: ActionButton = ActionButton("BLOQUEAR", "#3F95D3")

        self.roll_down_car_window: ActionButton = ActionButton("BAIXAR VIDROS", "#3F95D3")

        self.open_car_button: ActionButton = ActionButton("ABRIR CARRO", "#3F95D3")

        self.register_button: ActionButton = ActionButton("CADASTRO", "#533FD3")

        self.alarm_button: ActionButton = ActionButton("ALARME", "#D33F3F")

        # BLOCO DO SWITCH-BUTTON
        self.play_btn_layout: QHBoxLayout = QHBoxLayout()
        self.play_btn_layout.addWidget(self.play_button)
        self.play_btn_widget: QWidget = QWidget()
        self.play_btn_widget.setLayout(self.play_btn_layout)
        self.play_btn_widget.setFixedSize(self.widgets_width, 65)

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
        self.body_layout: QVBoxLayout = QVBoxLayout()
        self.body_layout.addWidget(self.video_screen)
        self.body_layout.addWidget(self.play_btn_widget)
        self.body_layout.addWidget(self.face_data_list)
        self.body_layout.addWidget(self.first_action_buttons)
        self.body_layout.addWidget(self.second_action_buttons)
        self.body_layout.addWidget(self.alarm_button)

        # CORPO DA JANELA CHIMERACAM
        self.body: QWidget = QWidget()
        self.body.setLayout(self.body_layout)
        self.body.setStyleSheet('background-color: #3E3A3A; padding: 10px 10px')

class ChimeraCam(UserInterface):
    def __init__(self, window_width):
        super().__init__(window_width)

        self.setWindowTitle(self.window_name)
        self.setCentralWidget(self.body)
        self.move(500, 0)

        self.thread_is_running: bool = False
        self.face_tracking: VideoFaceTrack = VideoFaceTrack(self.widgets_width)

        self.play_button.clicked.connect(self.operate_tracking)

    def operate_tracking(self) -> None:
        if not self.thread_is_running:
            self.thread_is_running = True
            self.face_tracking.start()
            self.face_tracking.image_signal.connect(self.refresh_video_screen)
            self.face_tracking.face_data_signal.connect(self.refresh_face_data_list)
            self.play_button.setText('\u25A0')
        else:
            self.thread_is_running = False
            self.face_tracking.stop()
            self.face_tracking.image_signal.disconnect()
            self.face_tracking.face_data_signal.disconnect()
            self.play_button.setText('\u25B6')
            self.video_screen.setPixmap(QPixmap(""))
            self.face_data_list.clear()
            
    def refresh_video_screen(self, tracked_image: QImage) -> None:
        self.video_screen.setPixmap(QPixmap.fromImage(tracked_image))

    def refresh_face_data_list(self, face_data: list) -> None:
        self.face_data_list.clear()
        self.face_data_list.addItems(face_data)
    
    def close_chimera_cam(self) -> None:
        self.close()

