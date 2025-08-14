from kivymd.uix.screen import MDScreen

class TermsScreen(MDScreen):
    def accept(self):
        self.get_app().accept_policies_and_go_video()

    def decline(self):
        self.get_app().back_to_ads()

    def get_app(self):
        from kivy.app import App
        return App.get_running_app()
