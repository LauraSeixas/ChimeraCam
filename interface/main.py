import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
    