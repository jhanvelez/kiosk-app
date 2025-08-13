from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp
import cairosvg
import io
from PIL import Image as PILImage

class SvgImage(Image):
    def __init__(self, source=None, **kwargs):
        super().__init__(**kwargs)
        if source:
            self.set_source(source)

    def set_source(self, value):
        svg_data = open(value, 'rb').read()
        png_data = cairosvg.svg2png(bytestring=svg_data)
        image = PILImage.open(io.BytesIO(png_data)).convert("RGBA")

        texture = Texture.create(size=image.size, colorfmt='rgba')
        texture.blit_buffer(image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture = texture

class PatternBackground(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_icons, 0.1)

    def add_icons(self, *args):
        spacing = dp(120)
        for i in range(0, int(self.width), int(spacing)):
            for j in range(0, int(self.height), int(spacing)):
                icon = SvgImage(source="assets/icons/good.svg")
                icon.size_hint = (None, None)
                icon.size = (dp(50), dp(50))
                icon.pos = (i, j)
                icon.color = [1, 1, 0, 0.1]
                self.add_widget(icon)

                icon2 = SvgImage(source="assets/icons/good.svg")
                icon2.size_hint = (None, None)
                icon2.size = (dp(50), dp(50))
                icon2.pos = (i + dp(60), j + dp(60))
                icon2.color = [1, 1, 0, 0.1]
                self.add_widget(icon2)