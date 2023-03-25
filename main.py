import sys
from interface.chimera_cam import ChimeraCam
from PyQt5.QtWidgets import QApplication
    
if __name__ == '__main__':
    app: QApplication = QApplication(sys.argv)
    window_width: int = 380
    chimeracam_window: ChimeraCam = ChimeraCam(window_width)
    chimeracam_window.show()
    sys.exit(app.exec())
    