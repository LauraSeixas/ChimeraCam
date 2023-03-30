from PyQt5.QtGui import QImage, QPixmap
from .user_interface import UserInterface
from .video_face_track import VideoFaceTrack
from .register import Register

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

        self.register_running: bool = False
        self.register: Register = Register(self.widgets_width)
        self.register_button.clicked.connect(self.registration_modal.operate_modal)
        self.registration_button.clicked.connect(self.user_registering)
        self.register.user_name = "something"

    def operate_tracking(self) -> None:
        if not self.tracking_running:
            self.tracking_running = True
            self.face_tracking.start()
            self.face_tracking.image_signal.connect(self.refresh_video_screen)
            self.face_tracking.face_data_signal.connect(self.refresh_face_data_list)
            self.play_button.setText(self.play_button.stop)
            self.play_button.setStyleSheet(self.play_button.stop_style)
        else:
            self.tracking_running = False
            self.face_tracking.stop()
            self.face_tracking.image_signal.disconnect()
            self.face_tracking.face_data_signal.disconnect()
            self.play_button.setText(self.play_button.play)
            self.play_button.setStyleSheet(self.play_button.play_style)
            self.video_screen.setPixmap(QPixmap(None))
            self.face_data_list.clear()

    def user_registering(self):
        if self.tracking_running == True:
            self.operate_tracking()

        self.register.user_name = self.registration_modal.user_name_input.text()

        if not self.register.thread_running:
            self.register.start()
            self.register.register_signal.connect(self.refresh_video_screen)
        else:
            #self.register_running = False
            self.video_screen.setPixmap(QPixmap.fromImage(None))
        """ self.register.stop()
            self.register.register_signal.disconnect()
            self.video_screen.setPixmap(QPixmap(None)) """
        
    def refresh_video_screen(self, image: QImage) -> None:
        self.video_screen.setPixmap(QPixmap.fromImage(image))

    def refresh_face_data_list(self, face_data: list) -> None:
        self.face_data_list.clear()
        self.face_data_list.addItems(face_data)