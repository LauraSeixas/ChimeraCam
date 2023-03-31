from PyQt5.QtGui import QImage, QPixmap
from .user_interface import UserInterface
from .video_face_track import VideoFaceTrack
from .register import Register
from .widgets import Screen

class ChimeraCam(UserInterface):
    def __init__(self, window_width: int):
        super().__init__(window_width)

        self.setWindowTitle(self.window_name)
        self.setCentralWidget(self.body)
        self.setObjectName("Body")
        self.setStyleSheet(self.body.css_style)
        self.move(750, 100)

        self.tracking_running: bool = False
        self.face_tracking: VideoFaceTrack = VideoFaceTrack(self.widgets_width)
        self.play_button.clicked.connect(self.operate_tracking)

        self.register: Register = Register(self.widgets_width)
        self.register.screen: Screen = self.video_screen
        self.registration_modal.operate_face_track = self.operate_tracking
        self.registration_modal_button.clicked.connect(self.registration_modal.operate_registration_modal)
        self.registration_start_button.clicked.connect(self.user_registering)
        
    def operate_tracking(self) -> None:
        if not self.tracking_running:
            self.tracking_running = True
            self.face_tracking.start()
            self.face_tracking.image_signal.connect(self.refresh_video_screen)
            self.face_tracking.face_data_signal.connect(self.refresh_face_data_list)
            self.face_tracking.child_alert.connect(self.refresh_detected_childalert)
            self.play_button.setText(self.play_button.stop)
            self.play_button.setStyleSheet(self.play_button.stop_style)
            self.registration_modal.face_track_running: bool = self.tracking_running
        else:
            self.tracking_running = False
            self.face_tracking.stop()
            self.face_tracking.image_signal.disconnect()
            self.face_tracking.face_data_signal.disconnect()
            self.face_tracking.child_alert.disconnect()
            self.play_button.setText(self.play_button.play)
            self.play_button.setStyleSheet(self.play_button.play_style)
            self.video_screen.setPixmap(QPixmap(None))
            self.face_data_list.clear()
            self.child_alert_label.setText("")
            self.registration_modal.face_track_running = self.tracking_running

    def user_registering(self):
        self.register.user_name = self.registration_modal.user_name_input.text()
        self.registration_modal.modal.hide()
        self.registration_modalmodal_closed = True
        if len(self.register.user_name) < 3:
            self.registration_modal.info_label.setText(self.registration_modal.info_text_3)
            return

        if not self.register.thread_running:
            self.registration_modal.info_label.setText(self.registration_modal.info_text_2)
            self.register.start()
            self.register.register_signal.connect(self.refresh_video_screen)
        
    def refresh_video_screen(self, image: QImage) -> None:
        self.video_screen.setPixmap(QPixmap.fromImage(image))

    def refresh_face_data_list(self, face_data: list) -> None:
        self.face_data_list.clear()
        self.face_data_list.addItems(face_data)
    
    def refresh_detected_childalert(self, alert: str) -> None:
        if alert == self.child_alert_label.detected:
            self.child_alert_label.setStyleSheet(self.child_alert_label.css_style_red)
        else:
            self.child_alert_label.setStyleSheet(self.child_alert_label.css_style_green)
        self.child_alert_label.setText(alert)