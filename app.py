from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from services.config import load_config
from screens.pairing_screen import PairingScreen
from screens.video_screen import VideoScreen
from widgets.pattern_background import PatternBackground

class KioskoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Light"

        self.sm = ScreenManager()
        self.load_kv_files()
        self.register_screens()
        
        config = load_config()
        if config and config.get("registered"):
            self.sm.current = "video"
        else:
            self.sm.current = "pairing"

        return self.sm

    def load_kv_files(self):
        Builder.load_file("kv/pairing_screen.kv")
        Builder.load_file("kv/video_screen.kv")

    def register_screens(self):
        self.sm.add_widget(PairingScreen(name="pairing"))
        self.sm.add_widget(VideoScreen(name="video"))
