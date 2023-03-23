import sys
from os.path import dirname
sys.path.append(dirname(__file__))
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QTableView, QWidget, QLabel
from buttons.action_button import ActionButton
from buttons.register_button import RegisterButton
from buttons.alarm_button import AlarmButton

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        interface_layout = QHBoxLayout()
        interface_layout.addLayout(self.__addButtons())
        interface_layout.addWidget(QTableView())

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__addVideoWidget())
        main_layout.addLayout(interface_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)
        self.setFixedSize(360, 640)
        self.move(100, 100)
        self.setWindowTitle("ChimeraCam")
        self.setStyleSheet("background-color: #3E3A3A; padding: 10px 10px")
        # self.setWindowIcon(QtGui.QIcon("icon.png"))

    def __addVideoWidget(self):
        video = QLabel()
        video.setPixmap(QPixmap("assets/video.png"))

        return video
    
    def __addButtons(self):
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(ActionButton("BLOQUEAR"))
        buttons_layout.addWidget(ActionButton("ABRIR CARRO"))
        buttons_layout.addWidget(ActionButton("BAIXAR VIDROS"))
        buttons_layout.addWidget(RegisterButton("CADASTRO"))
        buttons_layout.addWidget(AlarmButton("ALARME"))

        return buttons_layout
    