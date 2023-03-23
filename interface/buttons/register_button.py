from PyQt5.QtWidgets import QPushButton

class RegisterButton(QPushButton):
    def __init__(self, button_text: str):
        super(RegisterButton, self).__init__()
        
        self.setText(button_text)
        self.setStyleSheet("background-color: #533FD3; border-radius: 10px; border: 1px solid #FFFFFF")
