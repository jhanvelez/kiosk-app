# screens/video_screen.py

import cv2
import time
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.uix.screen import MDScreen

class VideoScreen(MDScreen):
    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.recording = False
        self.out = None
        Clock.schedule_interval(self.update_camera, 1.0 / 30)

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_view.texture = img_texture

            if self.recording and self.out:
                self.out.write(frame)

    def start_recording(self):
        if not self.recording:
            filename = f"video_{int(time.time())}.avi"
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.out = cv2.VideoWriter(
                filename,
                cv2.VideoWriter_fourcc(*'XVID'),
                30.0,
                (width, height)
            )
            self.recording = True
            self.ids.camera_view.opacity = 1
            self.ids.status_label.text = f"🎥 Grabando: {filename}"
        else:
            self.recording = False
            self.out.release()
            self.out = None
            self.ids.status_label.text = "Grabación finalizada."

    def on_leave(self):
        if self.capture.isOpened():
            self.capture.release()
        if self.out:
            self.out.release()
        self.recording = False
