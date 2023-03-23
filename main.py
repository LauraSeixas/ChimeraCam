import sys
#from src.interface.main_window import MainWindow
from src.interface.chimera_cam import ChimeraCam
from PyQt5.QtWidgets import QApplication
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_width: int = 360
    chimeracam_window: ChimeraCam = ChimeraCam(window_width)
    chimeracam_window.show()
    sys.exit(app.exec())