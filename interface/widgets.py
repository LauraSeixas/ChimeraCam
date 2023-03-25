from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget

__all__ = ["Screen", "PlayButton", "FaceData", "ActionButton", "PlaybuttonWidget", "ActionbuttonWidget", "Body"]

class Screen(QLabel):
    css_style: str = """
    Screen {
        background-color: #2E2A2A;
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
        font: 12pt Arial; 
        font-weight: bold; 
        background-color: white; 
        border: 2px solid lightgray; 
        border-radius: 10px
    }
    """
    def __init__(self, widgets_width: int):
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
    def __init__(self, btn_name: str, bg_color: str):
        super().__init__()
        self.setText(btn_name)
        self.setStyleSheet(self.css_style.replace("bgcolor", bg_color))

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
        self.setLayout(self.action_btn_layout)

class Body(QWidget):
    css_style: str = """
    QWidget {
        padding: 10px 10px;
        background-color: #3E3A3A;
    }
    """
    def __init__(
            self, 
            screen: Screen,
            play_btn: PlaybuttonWidget,
            face_data: FaceData,
            first_action_btns: ActionbuttonWidget,
            secton_action_btns: ActionbuttonWidget,
            alarm_btn: ActionButton):
        super().__init__()
        self.body_layout: QVBoxLayout = QVBoxLayout()
        self.body_layout.addWidget(screen)
        self.body_layout.addWidget(play_btn)
        self.body_layout.addWidget(face_data)
        self.body_layout.addWidget(first_action_btns)
        self.body_layout.addWidget(secton_action_btns)
        self.body_layout.addWidget(alarm_btn)
        self.body_layout.setSpacing(0)
        self.setLayout(self.body_layout)