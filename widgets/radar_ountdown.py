from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse

class RadarCountdown(Widget):
    countdown = NumericProperty(15)
    wave_radius = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(countdown=self.update_canvas)
        Clock.schedule_interval(self.animate_wave, 1/30)

    def animate_wave(self, dt):
        self.wave_radius += 8
        if self.wave_radius > self.width:
            self.wave_radius = 0
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        # Fondo blanco
        with self.canvas:
            Color(1, 1, 1, 1)
            Ellipse(pos=self.pos, size=self.size)
            # Círculo blanco
            Color(1, 1, 1, 1)
            Ellipse(pos=(self.center_x-40, self.center_y-40), size=(80, 80))
            # Onda tipo radar
            Color(0.8, 0.8, 0.8, 0.3)
            Ellipse(pos=(self.center_x-self.wave_radius/2, self.center_y-self.wave_radius/2), size=(self.wave_radius, self.wave_radius))
            # Número del contador
            Color(0, 0, 0, 1)
            self.canvas.add(Color(0, 0, 0, 1))