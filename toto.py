from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from datetime import datetime
import os


# ---- Alarm Logic ---- #
class AlarmManager:
    def __init__(self):
        self.alarm_time = None
        self.alarm_active = False
        self.alarm_triggered = False
        self.sound = SoundLoader.load('assets/alarm.wav')

    def set_alarm(self, hour, minute):
        self.alarm_time = f"{hour}:{minute}"
        self.alarm_active = True
        self.alarm_triggered = False

    def stop_alarm(self):
        self.alarm_active = False
        self.alarm_triggered = False
        if self.sound and self.sound.state == 'play':
            self.sound.stop()

    def check_alarm(self):
        now = datetime.now().strftime('%H:%M')
        if self.alarm_active and not self.alarm_triggered and self.alarm_time == now:
            self.alarm_triggered = True
            if self.sound:
                self.sound.play()
            return True
        return False


# ---- Time Picker Popup ---- #
class TimePickerPopup(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Choisir l'heure"
        self.size_hint = (0.6, 0.5)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.spinner_hour = Spinner(text='07', values=[f"{i:02}" for i in range(0, 24)])
        self.spinner_min = Spinner(text='00', values=[f"{i:02}" for i in range(0, 60)])

        validate_btn = Button(text="✅ Valider", size_hint_y=None, height=50)
        validate_btn.bind(on_release=lambda _: self._validate(callback))

        layout.add_widget(Label(text="Heure"))
        layout.add_widget(self.spinner_hour)
        layout.add_widget(Label(text="Minutes"))
        layout.add_widget(self.spinner_min)
        layout.add_widget(validate_btn)
        self.content = layout

    def _validate(self, callback):
        hour = self.spinner_hour.text
        minute = self.spinner_min.text
        callback(hour, minute)
        self.dismiss()


# ---- Settings Popup ---- #
class SettingsPopup(Popup):
    def __init__(self, set_alarm_callback, stop_alarm_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Réglages"
        self.size_hint = (0.8, 0.5)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        set_btn = Button(text="🛌 Régler l'alarme", size_hint_y=None, height=60)
        set_btn.bind(on_release=lambda _: self.open_time_picker(set_alarm_callback))

        stop_btn = Button(text="🔇 Stopper l'alarme", size_hint_y=None, height=60)
        stop_btn.bind(on_release=lambda _: stop_alarm_callback())

        close_btn = Button(text="❌ Fermer", size_hint_y=None, height=60)
        close_btn.bind(on_release=self.dismiss)

        layout.add_widget(set_btn)
        layout.add_widget(stop_btn)
        layout.add_widget(close_btn)

        self.content = layout

    def open_time_picker(self, callback):
        TimePickerPopup(callback).open()


# ---- Main Screen ---- #
class ClockScreen(Screen):
    def __init__(self, alarm_manager, theme_color, **kwargs):
        super().__init__(**kwargs)
        self.alarm = alarm_manager
        self.theme_color = theme_color

        self.layout = BoxLayout(orientation='vertical', padding=20)
        self.label_hour = Label(
            text='--:--:--',
            font_size='100sp',
            bold=True,
            color=self.theme_color
        )
        self.label_status = Label(text='', font_size='20sp', color=self.theme_color)

        # On clique sur l'heure pour ouvrir les réglages
        self.label_hour.bind(on_touch_down=self.on_time_touch)

        self.layout.add_widget(self.label_hour)
        self.layout.add_widget(self.label_status)
        self.add_widget(self.layout)

        Clock.schedule_interval(self.update_clock, 1)

    def on_time_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            SettingsPopup(self.set_alarm, self.stop_alarm).open()

    def update_clock(self, *args):
        now = datetime.now()
        self.label_hour.text = now.strftime('%H:%M:%S')

        if self.alarm.check_alarm():
            self.label_status.text = f"⏰ Alarme : {self.alarm.alarm_time}"
        elif self.alarm.alarm_active:
            self.label_status.text = f"Alarme réglée : {self.alarm.alarm_time}"
        else:
            self.label_status.text = ""

    def set_alarm(self, hour, minute):
        self.alarm.set_alarm(hour, minute)

    def stop_alarm(self):
        self.alarm.stop_alarm()


# ---- App with Swipe Themes ---- #
class RadioReveilApp(App):
    def build(self):
        self.alarm = AlarmManager()
        Window.fullscreen = 'auto'

        self.manager = ScreenManager(transition=SlideTransition())
        self.themes = [
            ((1, 0.8, 0.2, 1), "Clair"),
            ((0.8, 1, 1, 1), "Bleu ciel"),
            ((1, 1, 1, 1), "Blanc"),
            ((0.4, 1, 0.5, 1), "Vert"),
        ]

        for i, (color, _) in enumerate(self.themes):
            self.manager.add_widget(ClockScreen(self.alarm, theme_color=color, name=f"theme_{i}"))

        Window.bind(on_touch_down=self._on_touch)
        return self.manager

    def _on_touch(self, window, touch):
        if touch.dx < -40:
            self.manager.current = self.manager.next()
        elif touch.dx > 40:
            self.manager.current = self.manager.previous()

if __name__ == '__main__':
    RadioReveilApp().run()