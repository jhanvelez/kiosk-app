from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from services.config import load_config
from screens.pairing_screen import PairingScreen
from screens.ad_screen import AdScreen
from screens.terms_screen import TermsScreen
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
            self.sm.current = "ads"
        else:
            self.sm.current = "pairing"

        return self.sm

    def load_kv_files(self):
        Builder.load_file("kv/pairing_screen.kv")
        Builder.load_file("kv/ad_screen.kv")
        Builder.load_file("kv/terms_screen.kv")
        Builder.load_file("kv/video_screen.kv")

    def register_screens(self):
        self.sm.add_widget(PairingScreen(name="pairing"))
        self.sm.add_widget(AdScreen(name="ads"))
        self.sm.add_widget(TermsScreen(name="terms"))
        self.sm.add_widget(VideoScreen(name="video"))
        
    def mark_registered_and_go_ads(self):
        self.config_state["registered"] = True
        save_config(self.config_state)
        self.sm.current = "ads"

    def go_terms(self):
        self.sm.current = "terms"

    def accept_policies_and_go_video(self):
        # self.config_state["accepted_policies"] = True
        # save_config(self.config_state)
        self.sm.current = "video"

    def back_to_ads(self):
        self.sm.current = "ads"
