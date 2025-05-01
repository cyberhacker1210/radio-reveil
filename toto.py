# kivy_radio_reveil.py
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime

# Fullscreen et sans bord
Window.fullscreen = True

# === Fonctions de gestion de l'heure ===
def curent_hour():
    return datetime.now().strftime("%I:%M %p")

def check_alarm(alarm_time):
    print(f"[Alarm] Checking alarm for {alarm_time}")

def stop_sound():
    print("[Alarm] Stopping sound")

# === Ecrans ===
class ClockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.label_hour = Label(
            text=curent_hour(),
            font_size='120sp',
            color=(1, 0.84, 0.41, 1)  # Jaune pastel
        )

        self.settings_button = Button(
            text="Settings",
            size_hint=(1, 0.2),
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            on_press=self.open_settings
        )

        self.layout.add_widget(self.label_hour)
        self.layout.add_widget(self.settings_button)
        self.add_widget(self.layout)

        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, dt):
        self.label_hour.text = curent_hour()

    def open_settings(self, instance):
        self.manager.current = "settings"


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.btn_stop = Button(text="Stop Sound", on_press=self.stop_alarm)
        self.btn_set = Button(text="Set Alarm", on_press=self.set_alarm)
        self.btn_close = Button(text="Back", on_press=self.go_back)

        for btn in (self.btn_stop, self.btn_set, self.btn_close):
            btn.size_hint = (1, 0.2)
            btn.background_color = (0.3, 0.3, 0.3, 1)
            btn.color = (1, 1, 1, 1)
            layout.add_widget(btn)

        self.add_widget(layout)

    def stop_alarm(self, instance):
        stop_sound()

    def set_alarm(self, instance):
        # Simule une alarme pour 08:00 AM
        check_alarm("08:00 AM")

    def go_back(self, instance):
        self.manager.current = "clock"


class RadioReveilApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ClockScreen(name="clock"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm


if __name__ == '__main__':
    RadioReveilApp().run()