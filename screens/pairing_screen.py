from kivymd.uix.screen import MDScreen
from services.pairing_service import pair_device
from services.config import save_config
from kivy.clock import Clock

class PairingScreen(MDScreen):

    def on_enter(self):
        self.ids.status_label.text = ""

    def on_pair(self):
        code = self.ids.code_input.text.strip()
        if len(code) != 6 or not code.isdigit():
            self.ids.status_label.text = "[color=ff0000]Código inválido.[/color]"
            return

        result = pair_device(code)
        if result:
            save_config({
                "name": result["name"],
                "location": result["location"],
                "description": result["description"],
                "device_id": result["device_id"],
                "auth_token": result["auth_token"],
                "registered": True
            })
            self.ids.status_label.text = "[color=31C950]¡✅ Dispositivo emparejado exitosamente, redirigiendo...![/color]"

            Clock.schedule_once(self.go_to_video_screen, 3)
        else:
            self.ids.status_label.text = "[color=ff0000]Código incorrecto o expirado.[/color]"
    
    def go_to_video_screen(self, dt):
        self.manager.current = "video"