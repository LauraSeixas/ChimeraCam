from PyQt5.QtWidgets import QPushButton

class AlarmButton(QPushButton):
    def __init__(self, button_text: str):
        super(AlarmButton, self).__init__()
        
        self.setText(button_text)
        self.setStyleSheet("background-color: #D33F3F; border-radius: 10px; border: 1px solid #FFFFFF")
