from PyQt5.QtWidgets import QPushButton

class ActionButton(QPushButton):
    def __init__(self, button_text: str):
        super(ActionButton, self).__init__()
        
        self.setText(button_text)
        self.setStyleSheet("background-color: #3F95D3; border-radius: 10px; border: 1px solid #FFFFFF")
