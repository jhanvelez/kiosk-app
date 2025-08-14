# screens/ad_screen.py
import os, itertools
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.video import Video

ADS_DIR = "assets/ads"

class AdScreen(MDScreen):
    def on_pre_enter(self, *a):
        self._cycle = self._iter_ads()
        self._swap_ad(None)
        # rota cada 20 s
        self._evt = Clock.schedule_interval(self._swap_ad, 20)

    def on_leave(self, *a):
        if hasattr(self, "_evt") and self._evt:
            self._evt.cancel()
        cont = self.ids.ad_container
        cont.clear_widgets()

    def on_touch_down(self, touch):
        # si el usuario toca, mostramos términos
        if self.collide_point(*touch.pos):
            self.get_app().go_terms()
            return True
        return super().on_touch_down(touch)

    def _iter_ads(self):
        files = []
        if os.path.isdir(ADS_DIR):
            for f in os.listdir(ADS_DIR):
                p = os.path.join(ADS_DIR, f)
                if os.path.isfile(p) and (f.lower().endswith((".png",".jpg",".jpeg",".webp",".mp4",".mov",".avi"))):
                    files.append(p)
        if not files:
            files = [None]
        return itertools.cycle(files)

    def _swap_ad(self, *a):
        cont = self.ids.ad_container
        cont.clear_widgets()
        src = next(self._cycle)
        if not src:
            cont.add_widget(Image(source="", allow_stretch=True, keep_ratio=True))
            return
        if src.lower().endswith((".mp4",".mov",".avi")):
            v = Video(source=src, state="play", options={"eos": "loop"})
            v.allow_stretch = True
            v.keep_ratio = True
            cont.add_widget(v)
        else:
            cont.add_widget(Image(source=src, allow_stretch=True, keep_ratio=True))

    def get_app(self):
        from kivy.app import App
        return App.get_running_app()
