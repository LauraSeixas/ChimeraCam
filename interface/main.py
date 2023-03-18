import sys
from main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_layout = QVBoxLayout()
    main_layout.addWidget(QPushButton("VIDEO"))

    buttons_layout = QVBoxLayout()

    interface_layout = QHBoxLayout()
    interface_layout.addLayout(buttons_layout)
    interface_layout.addWidget(QTableView())

    main_layout.addLayout(interface_layout)

    buttons_layout.addWidget(QPushButton("BLOQUEAR"))
    buttons_layout.addWidget(QPushButton("ABRIR CARRO"))
    buttons_layout.addWidget(QPushButton("BAIXAR VIDROS"))
    buttons_layout.addWidget(QPushButton("CADASTRO"))
    buttons_layout.addWidget(QPushButton("ALARME"))
    
    central_widget = QWidget()
    central_widget.setLayout(main_layout)

    window = MainWindow(central_widget)
    window.show()

    sys.exit(app.exec_())
    