import io
import random
import cairosvg

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.metrics import dp


class SvgImage(Image):
    _cache = {}

    def __init__(self, source=None, angle=0, **kwargs):
        super().__init__(**kwargs)
        self.angle = angle
        if source:
            self.set_source(source)
        self.bind(pos=self.update_rotation, size=self.update_rotation)

    def set_source(self, value):
        if value in SvgImage._cache:
            self.texture = SvgImage._cache[value]
            return

        svg_data = open(value, 'rb').read()
        png_data = cairosvg.svg2png(bytestring=svg_data)
        image = PILImage.open(io.BytesIO(png_data)).convert("RGBA")

        texture = Texture.create(size=image.size, colorfmt='rgba')
        texture.blit_buffer(image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture = texture
        SvgImage._cache[value] = texture  # Guardar en cache

    def update_rotation(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()
        with self.canvas.before:
            PushMatrix()
            Rotate(angle=self.angle, origin=self.center)
        with self.canvas.after:
            PopMatrix()



class PatternBackground(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fondo rojo sólido
        with self.canvas.before:
            Color(221 / 255, 83 / 255, 64 / 255, 1)  # Rojo
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_background, pos=self._update_background)

        # Crear íconos iniciales
        Clock.schedule_once(self.add_icons, 0.1)

    def _update_background(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

        # Regenerar íconos cuando cambia el tamaño
        self.regenerate_icons()

    def regenerate_icons(self):
        # Primero eliminar todos los widgets previos (los íconos viejos)
        self.clear_widgets()

        # Luego volver a crear el patrón
        self.add_icons()

    def add_icons(self, *args):
        spacing = dp(120)
        for i in range(0, int(self.width), int(spacing)):
            for j in range(0, int(self.height), int(spacing)):

                # good.svg
                icon = SvgImage(
                    source="assets/icons/good.svg",
                    angle=random.uniform(-15, 15)
                )
                icon.size_hint = (None, None)
                icon.size = (dp(50), dp(50))
                icon.pos = (i, j)
                self.add_widget(icon)

                # party.svg
                icon2 = SvgImage(
                    source="assets/icons/party.svg",
                    angle=random.uniform(-15, 15)
                )
                icon2.size_hint = (None, None)
                icon2.size = (dp(50), dp(50))
                icon2.pos = (i + dp(60), j + dp(60))
                self.add_widget(icon2)

                # music.svg
                icon3 = SvgImage(
                    source="assets/icons/music.svg",
                    angle=random.uniform(-15, 15)
                )
                icon3.size_hint = (None, None)
                icon3.size = (dp(50), dp(50))
                icon3.pos = (i + dp(60), j + dp(30))
                self.add_widget(icon3)
