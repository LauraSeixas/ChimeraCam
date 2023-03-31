from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore

__all__ = ["ChildAlert", "Screen", "PlayButton", "FaceData", "ActionButton", "PlaybuttonWidget", "ActionbuttonWidget", "RegistrationModal", "Body"]

class ChildAlert(QLabel):
    css_style_red = """
        ChildAlert {
            background-color: #2E2A2A;
            font: 11pt Roboto;
            font-weight: bold;
            color: red;
        }
    """
    css_style_green = """
        ChildAlert {
            background-color: #2E2A2A;
            font: 11pt Roboto;
            font-weight: bold;
            color: lightgreen;
        }
    """
    detected: str = "Criança detecatada!"
    not_detected: str = "Nenhuma criança detecatada!"
    def __init__(self, widgets_width):
        super().__init__()
        self.setFixedSize(widgets_width, 30)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        #self.setStyleSheet(self.css_style)
        self.setContentsMargins(0, 0, 0, 0)

class Screen(QLabel):
    css_style: str = """
    Screen {
        background-color: #2E2A2A;
        padding: 2 2
    }
    """
    def __init__(self, widgets_width: int):
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
        border-radius: 24px;
        padding: 0 0 4 2
    }
    """
    play_style: str = css_style.replace("14 0", "4 2")
    stop_style: str = css_style.replace("4 2", "14 0")
    play: str = "\u25B6"
    stop: str = "\u25A0"
    def __init__(self):
        super().__init__()
        self.setFixedSize(50, 50)
        self.setText(self.play)
        self.setStyleSheet(self.play_style)

class FaceData(QListWidget):
    css_style: str = """
    FaceData {
        font: 10pt Roboto;
        font-weight: bold;
        color: #555555;
        background-color: #D8D7DA; 
        border-radius: 10;
        margin: 0 10;
        padding: 10 3 3 10;
    }

    QScrollBar:vertical {              
        border: none;
        background: #FFFFFF;
        width: 10;
        margin: 0 0 0 0;
    }
    QScrollBar::handle:vertical {
        background: #3E3A3A;
        min-height: 20;
    }

    QScrollBar:horizontal {              
        border: none;
        background: #FFFFFF;
        height: 10;
        margin: 0 0 0 0;
    }
    QScrollBar::handle:horizontal {
        background: #3E3A3A;
        min-width: 20;
    }
    
    """
    def __init__(self, widgets_width: int):
        super().__init__()
        self.setFixedSize(widgets_width, 130)
        self.setStyleSheet(self.css_style)

class ActionButton(QPushButton):
    css_style: str = """
    ActionButton {
        color: #FFFFFF;
        font: 9pt Roboto;
        font-weight: bold;
        background-color: bgcolor;
        border-radius: 10px;
        padding: 10 10;
        margin: 15 10 5;
    }
    """
    def __init__(self, btn_name: str, bg_color: str, message_str: str = ""):
        super().__init__()
        if btn_name != "ALARME":
            self.css_style = self.css_style.replace("margin: 15 10 5;", "")

        self.setText(btn_name)
        self.setStyleSheet(self.css_style.replace("bgcolor", bg_color))
        
        if btn_name != "CADASTRO" and btn_name != "INICIAR":
            self.message = message_str
            self.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
       if self.message:
            msg = MessageBox(self.message)
            msg.exec()

class MessageBox(QMessageBox):
    css_style: str = """
    QMessageBox {
        background-color: #2E2A2A;
    }

    QMessageBox QLabel {
        color: #FFFFFF;
        font: 9pt Roboto;
        font-weight: bold;
    }

    QMessageBox QPushButton {
        color: #FFFFFF;
        font: 9pt Roboto;
        font-weight: bold;
        background-color: #3F95D3;
        border-radius: 10px;
        padding: 10 10;
        margin: 15 10 5;
    }
    """
    def __init__(self, message: str = ""):
        super().__init__()
        self.setText(message)
        self.setIcon(QMessageBox.Warning)
        self.setStyleSheet(self.css_style)

class RegistrationModal():
    info_text_1: str = "Informe seu nome e \ninicie a identificação"
    info_text_2: str = "Mova seu rosto a\ncada 2 segundos"
    info_text_3: str = "Informe um nome com\n3 ou mais caracteres"
    info_label_css: str = "QLabel {font: 11pt Roboto; font-weight: bold; color: #D8D7DA}"
    user_name_css: str = "QLineEdit {font: 11pt Roboto; font-weight: bold; padding: 0 10; background-color: #D8D7DA}"
    modal_css: str = "QFrame {background-color: #4E4A4A; border: none;}"

    def __init__(self, body, registration_btn: ActionButton):
        super().__init__()
        self.face_track_running: bool = False
        self.operate_face_track = ""

        self.info_label = QLabel()
        self.info_label.setFixedSize(220, 50)
        self.info_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.info_label.setStyleSheet(self.info_label_css)
        self.info_label.setContentsMargins(0, 0, 0, 0)

        self.user_name_input = QLineEdit()
        self.user_name_input.setFixedSize(220, 40)
        self.user_name_input.setStyleSheet(self.user_name_css)

        self.registration_btn: ActionButton = registration_btn

        self.modal_layout = QVBoxLayout()
        self.modal_layout.addWidget(self.info_label)
        self.modal_layout.addWidget(self.user_name_input)
        self.modal_layout.addWidget(self.registration_btn)
        self.modal_layout.setSpacing(0)
        self.modal_layout.setContentsMargins(30, 0, 30, 0)

        self.modal = QFrame(body)
        self.modal.setLayout(self.modal_layout)
        self.modal.setStyleSheet(self.modal_css)
        self.modal.setGeometry(60,350, 280,200)
        self.modal.hide()
        self.modal_closed = True

    def operate_registration_modal(self):
        if self.face_track_running == True:
                self.operate_face_track()
        if self.modal_closed:
            self.info_label.setText(self.info_text_1)
            self.modal.show()
            self.modal_closed = False
        else:
            self.user_name_input.clear()
            self.modal.hide()
            self.modal_closed = True

class PlaybuttonWidget(QWidget):
    def __init__(self, play_button: PlayButton):
        super().__init__()
        self.horizontal_layout: QHBoxLayout = QHBoxLayout()
        self.horizontal_layout.addWidget(play_button)
        self.setLayout(self.horizontal_layout)

class ActionbuttonWidget(QWidget):
    def __init__(self, first_button: ActionButton, second_button: ActionButton):
        super().__init__()
        self.action_btn_layout: QHBoxLayout = QHBoxLayout()
        self.action_btn_layout.addWidget(first_button)
        self.action_btn_layout.addWidget(second_button)
        self.action_btn_layout.setSpacing(30)
        self.action_btn_layout.setContentsMargins(10, 15, 10, 0)
        self.setLayout(self.action_btn_layout)

class Body(QWidget):
    css_style: str = """
    QWidget#Body {
        padding: 10 10;
        background-color: #3E3A3A;
    }
    """
    def __init__(
            self,
            child_alert: ChildAlert,
            screen: Screen,
            play_btn: PlaybuttonWidget,
            face_data: FaceData,
            first_action_btns: ActionbuttonWidget,
            secton_action_btns: ActionbuttonWidget,
            alarm_btn: ActionButton):
        super().__init__()
        self.body_layout: QVBoxLayout = QVBoxLayout()
        self.body_layout.addWidget(child_alert)
        self.body_layout.addWidget(screen)
        self.body_layout.addWidget(play_btn)
        self.body_layout.addWidget(face_data)
        self.body_layout.addWidget(first_action_btns)
        self.body_layout.addWidget(secton_action_btns)
        self.body_layout.addWidget(alarm_btn)
        self.body_layout.setSpacing(0)
        self.setLayout(self.body_layout)