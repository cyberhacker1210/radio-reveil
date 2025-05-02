from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import StringProperty
import back
import config

class MainScreen(Screen):
    current_time = StringProperty()
    


    def update_time(self, dt):
        self.current_time = back.current_hour()

    def on_enter(self):
        Clock.schedule_interval(self.update_time, 1)

class SettingsScreen(Screen):
    def stop_sound(self):
        back.stop_alarm_sound()
    pass

class AlarmConfigScreen(Screen):
    def set_alarm(self):
        hour = f"{self.ids.hour_spinner.text}:{self.ids.minute_spinner.text}:{self.ids.ampm_spinner.text}"
        self.manager.current = "main"
        back.check_alarm(hour)

from kivy.lang import Builder
Builder.load_file("interface.kv")

class ReveilApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        sm.add_widget(AlarmConfigScreen(name="alarm_config"))
        config.fenetre = sm
        return sm

if __name__ == '__main__':
    ReveilApp().run()
