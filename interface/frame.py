import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QFrame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.button = QPushButton()
        self.button.setText("INICIAR CAPTURA")
        self.button.clicked.connect(self.hideframe)
        self.button.setStyleSheet(""" QPushButton{ height: 40; background-color: #BBB; border: none; padding: 2px;} """)
        self.button.setDisabled(False)

        self.button2 = QPushButton()
        self.button2.setText("CADASTRO")
        self.button2.clicked.connect(self.showframe)
        self.button2.setStyleSheet(""" QPushButton{ height: 40; background-color: #BBB; border: none; padding: 2px;} """)
        self.button2.setDisabled(False)

        self.frame2 = QFrame()
        self.frame2.setMaximumSize(200, 200)
        self.framelay2 = QHBoxLayout()
        self.framelay2.addWidget(self.button2)
        self.frame2.setLayout(self.framelay2)
        self.frame2.setStyleSheet(""" QFrame { background-color: #448844; border: none;} """)

        self.body = QWidget()
        self.bodylay = QVBoxLayout()
        self.bodylay.addWidget(self.frame2)
        self.body.setLayout(self.bodylay)
        self.body.setStyleSheet(""" QWidget { padding: 0} """)
        self.body.setContentsMargins(0,0,0,0)

        self.frame = QFrame(self.body)
        self.frame.setMaximumSize(200, 200)
        self.framelay = QHBoxLayout()
        self.framelay.addWidget(self.button)
        self.frame.setLayout(self.framelay)
        self.frame.setStyleSheet(""" QFrame { background-color: #880088; border: none;} """)
        self.frame.setGeometry(100,200, 200,200)
        self.frame.hide()

        self.setWindowTitle("Janela")
        self.setCentralWidget(self.body)
        self.setMinimumSize(400, 500)
        self.move(600, 100)

    def hideframe(self):
        self.frame.hide()
        self.button2.setDisabled(True)

    def showframe(self):
        self.frame.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())