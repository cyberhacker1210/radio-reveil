from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto') 

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.clock import Clock
from back import play_alarm_sound, stop_alarm_sound
from datetime import datetime
from kivy.graphics import Color, Rectangle


# Définition de l'écran principal
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Définir l'heure initiale et afficher sur le label
        self.time_label = Label(
            text="00:00",
            font_size='100sp',
            size_hint=(1, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.time_label)
        self.time_label.bind(on_touch_down=self.on_time_label_touch)
        Clock.schedule_interval(self.update_time, 1)  # Mettre à jour l'heure toutes les secondes

    def on_time_label_touch(self, instance, touch):
        """Vérifie si le touché est sur le label et ouvre les paramètres si c'est le cas"""
        if instance.collide_point(touch.x, touch.y):
            self.open_settings()

    def update_time(self, dt):
        """Met à jour l'heure à chaque seconde"""
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.text = current_time

    def open_settings(self):
        """Ouvre la fenêtre des paramètres"""
        self.manager.current = 'settings'


# Définition de l'écran des paramètres
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)
        self.add_widget(layout)

        # Bouton pour revenir à l'écran principal
        back_button = Button(text="Retour à l'écran principal", on_press=self.go_back, size_hint=(1, 0.2))
        layout.add_widget(back_button)

        # Bouton pour arrêter l'alarme
        stop_alarm_button = Button(text="Arrêter l'alarme", on_press=self.stop_alarm, size_hint=(1, 0.2))
        layout.add_widget(stop_alarm_button)

        # Bouton pour régler l'alarme
        set_alarm_button = Button(text="Régler l'alarme", on_press=self.set_alarm, size_hint=(1, 0.2))
        layout.add_widget(set_alarm_button)

    def on_touch_down(self, touch):
        # Inverser l'axe Y
        touch.y = self.height - touch.y
        return super().on_touch_down(touch)
    
    def go_back(self, instance):
        self.manager.current = 'main'

    def stop_alarm(self, instance):
        stop_alarm_sound()
        # Ajouter la logique pour arrêter l'alarme

    def set_alarm(self, instance):
        # Ouvrir la fenêtre de réglage de l'alarme
        self.open_alarm_picker()

    def open_alarm_picker(self):
        """Ouvre le Time Picker sous forme d'horloge"""
        content = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Créer des labels locaux pour l'heure et les minutes
        hour_label = Label(text="Heure: 08", size_hint=(1, 0.2))
        minute_label = Label(text="Minute: 00", size_hint=(1, 0.2))

        # Ajouter un slider pour l'heure
        self.hour_slider = Slider(min=0, max=23, value=8, step=1)
        self.hour_slider.bind(value=lambda instance, value: hour_label.setter('text')(hour_label, f"Heure: {int(value):02}"))
        content.add_widget(hour_label)
        content.add_widget(self.hour_slider)

        # Ajouter un slider pour les minutes
        self.minute_slider = Slider(min=0, max=59, value=0, step=1)
        self.minute_slider.bind(value=lambda instance, value: minute_label.setter('text')(minute_label, f"Minute: {int(value):02}"))
        content.add_widget(minute_label)
        content.add_widget(self.minute_slider)

        # Ajouter un bouton pour confirmer le réglage de l'alarme
        confirm_button = Button(text="Confirmer", on_press=self.set_alarm_time)
        content.add_widget(confirm_button)

        # Créer la popup
        self.popup = Popup(title="Réglage de l'alarme", content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def update_hour_label(self, instance, value):
        """Met à jour l'heure affichée"""
        self.hour_label.text = f"Heure: {int(value):02}"

    def update_minute_label(self, instance, value):
        """Met à jour les minutes affichées"""
        self.minute_label.text = f"Minute: {int(value):02}"
    
    def check_alarm_time(self, dt):
        """Vérifie si l'heure actuelle correspond à l'heure de l'alarme"""
        
        current_time = datetime.now().strftime('%H:%M')
        alarm_time = f"{int(self.hour_slider.value):02}:{int(self.minute_slider.value):02}"
        if current_time == alarm_time:
            play_alarm_sound()
            # Ajouter la logique pour déclencher l'alarme
            return False

    def set_alarm_time(self, instance):
        """Confirme l'heure de l'alarme et ferme le Time Picker"""
        hour = int(self.hour_slider.value)
        minute = int(self.minute_slider.value)
        print(f"Alarme réglée à {hour:02}:{minute:02}")
        self.popup.dismiss()
        Clock.schedule_interval(self.check_alarm_time, 1)


# Définition de l'application
class ReveilApp(App):
    def build(self):
        # Création d'un gestionnaire d'écran
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm


# Lancer l'application
if __name__ == '__main__':
    ReveilApp().run()
