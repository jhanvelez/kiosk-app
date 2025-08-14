import os
import cv2
import time
import json
import tempfile
import subprocess

from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen
from threading import Thread

from services.video_api import store_video

with open("config.json", "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

class VideoScreen(MDScreen):
    countdown_time = NumericProperty(15)

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        self.recording = False
        self.out = None
        self.countdown_time = 15

        Clock.schedule_once(self.start_camera, 0.5)

    def start_camera(self, *args):
        Clock.schedule_interval(self.update_camera, 1.0 / 30)
        self.start_recording_with_audio()

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf = cv2.flip(frame, 0).tobytes()
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_view.texture = img_texture

            if self.recording and self.out:
                self.out.write(frame)
                
    def start_recording_with_audio(self):
        temp_dir = tempfile.gettempdir()
        self.filename = os.path.join(temp_dir, f"video_{int(time.time())}.mp4")
        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-f", "avfoundation",          # SOLO para la entrada
            "-framerate", "30",
            "-video_size", "640x480",      # Usa una resolución soportada
            "-i", "0:0",                   # cámara y micrófono por defecto en Mac
            "-t", "15",                    # Graba solo 15 segundos
            "-c:v", "libx264",
            "-c:a", "aac",
            self.filename                  # archivo de salida
        ]
        self.ffmpeg_process = subprocess.Popen(ffmpeg_cmd)
        self.recording = True
        self.ids.status_label.text = "Grabando..."
        self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)

    def stop_recording_with_audio(self):
        if hasattr(self, 'ffmpeg_process'):
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
        self.recording = False
        Clock.unschedule(self.countdown_event)
        self.ids.status_label.text = "Procesando video..."

        # Espera activa hasta que el archivo exista (máx 5 segundos)
        timeout = 5
        waited = 0
        while not (self.filename and os.path.exists(self.filename)) and waited < timeout:
            time.sleep(0.2)
            waited += 0.2

        if not self.filename or not os.path.exists(self.filename) or os.path.getsize(self.filename) < 1000:
            self.ids.status_label.text = "El video es demasiado pequeño o está corrupto."
            return

        Thread(target=self.send_video_to_server, args=(self.filename,)).start()

    def start_recording(self):
        if not self.recording:
            temp_dir = tempfile.gettempdir()
            self.filename = os.path.join(temp_dir, f"video_{int(time.time())}.mp4")
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.out = cv2.VideoWriter(
                self.filename,
                cv2.VideoWriter_fourcc(*'X264'),
                30.0,
                (width, height)
            )
            self.recording = True
            self.ids.status_label.text = "Grabando..."

            self.countdown_event = Clock.schedule_interval(self.update_countdown, 1)
            
    def update_countdown(self, dt):
        self.countdown_time -= 1
        self.ids.countdown_label.text = str(self.countdown_time)
        if self.countdown_time <= 0:
            self.stop_recording_with_audio()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            if self.out:
                self.out.release()
                self.out = None
            Clock.unschedule(self.countdown_event)
            self.ids.status_label.text = "Procesando video..."
            
            time.sleep(1)
            
            if os.path.getsize(self.filename) < 1000:
                self.ids.status_label.text = "El video es demasiado pequeño o está corrupto."
                return
            
            # Iniciar envío en segundo plano
            Thread(target=self.send_video_to_server, args=(self.filename,)).start()

    def send_video_to_server(self, file_path):
        try:
            kiosk_id = CONFIG.get("kiosk_id")
            if not kiosk_id:
                self.ids.status_label.text = "Falta kiosk_id en config.json"
                return

            result = store_video(file_path, kiosk_id)

            if result:
                self.show_confetti_and_thanks()
            else:
                self.ids.status_label.text = "Error al subir el video."
        except Exception as e:
            self.ids.status_label.text = f"Error: {e}"

    def show_confetti_and_thanks(self):
        self.ids.status_label.text = "¡Gracias por grabar el video!"
        
        # Esperar 3 segundos y volver a "adds"
        Clock.schedule_once(self.go_to_ads, 3)

    def on_leave(self):
        if self.capture.isOpened():
            self.capture.release()
        if self.out:
            self.out.release()
        self.recording = False

    def go_to_ads(self, dt):
        self.manager.current = "ads"