from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, central_widget):
        super(MainWindow, self).__init__()

        self.setCentralWidget(central_widget)
        self.resize(500, 500)
        self.move(100, 100)
        self.setWindowTitle("ChimeraCam")
        # self.setWindowIcon(QtGui.QIcon("icon.png"))
