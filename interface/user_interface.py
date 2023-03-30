from PyQt5.QtWidgets import QMainWindow
from .widgets import *

class UserInterface(QMainWindow):
    def __init__(self, window_width: int):
        super().__init__()
        self.window_name: str = "ChimeraCam"
        self.widgets_width: int = window_width
        self.video_screen: Screen = Screen(self.widgets_width)
        self.play_button: PlayButton = PlayButton()
        self.face_data_list: FaceData = FaceData(self.widgets_width)
        self.block_car_button: ActionButton = ActionButton("BLOQUEAR", "#3F95D3", "Carro bloqueado com sucesso")
        self.roll_down_car_window: ActionButton = ActionButton("BAIXAR VIDROS", "#3F95D3", "Vidros baixados")
        self.open_car_button: ActionButton = ActionButton("ABRIR CARRO", "#3F95D3", "Carro aberto com sucesso")
        self.register_button: ActionButton = ActionButton("CADASTRO", "#533FD3")
        self.alarm_button: ActionButton = ActionButton("ALARME", "#D33F3F", "Alarme ligado")
        self.registration_button: ActionButton = ActionButton("INICIAR", "#533FD3")

        self.play_btn_widget: PlaybuttonWidget = PlaybuttonWidget(self.play_button)
        self.first_action_buttons: ActionbuttonWidget = ActionbuttonWidget(self.block_car_button, self.roll_down_car_window)
        self.second_action_buttons: ActionbuttonWidget = ActionbuttonWidget(self.open_car_button, self.register_button)
        self.body: Body = Body(self.video_screen, self.play_btn_widget, self.face_data_list, 
                               self.first_action_buttons, self.second_action_buttons, self.alarm_button)
        self.registration_modal: RegistrationModal = RegistrationModal(self.body, self.registration_button)