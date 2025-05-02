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
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from random import uniform


# Définition de l'écran principal
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Définir l'heure initiale et afficher sur le label
        self.time_label = Label(
            text="00:00:00",
            font_size=100,
            size_hint=(None, None),  # Taille fixe pour faciliter le calcul des collisions
            size=(200, 100),  # Taille du label
            pos=(self.width / 2, self.height / 2),  # Position initiale
            color=(1, 1, 1, 1)  # Couleur initiale (blanc)
        )
        self.add_widget(self.time_label)

        # Variables pour la direction du mouvement
        self.dx = 5  # Vitesse horizontale
        self.dy = 5  # Vitesse verticale

        # Mettre à jour l'heure toutes les secondes
        Clock.schedule_interval(self.update_time, 1)

        # Lancer l'animation de rebond
        Clock.schedule_interval(self.animate_bounce, 1 / 60)  # 60 FPS

        # Lancer l'animation de changement de couleur
        self.animate_color()

    def on_touch_down(self, touch):
        """Gère les clics sur le label"""
        if self.time_label.collide_point(touch.x, touch.y):
            print("Label cliqué !")
            # Changer l'écran actif vers 'settings'
            self.manager.current = 'settings'
        return super().on_touch_down(touch)

    def animate_bounce(self, dt):
        """Déplace le label et gère les rebonds sur les bords de l'écran"""
        # Mettre à jour la position
        new_x = self.time_label.x + self.dx
        new_y = self.time_label.y + self.dy

        # Vérifier les collisions avec les bords de l'écran
        if new_x <= 0 or new_x + self.time_label.width >= self.width:
            self.dx *= -1  # Inverser la direction horizontale
        if new_y <= 0 or new_y + self.time_label.height >= self.height:
            self.dy *= -1  # Inverser la direction verticale

        # Appliquer la nouvelle position
        self.time_label.x += self.dx
        self.time_label.y += self.dy

    def animate_color(self):
        """Change la couleur du texte de manière fluide"""
        # Générer une nouvelle couleur pastel
        new_r = uniform(0.7, 1.0)
        new_g = uniform(0.7, 1.0)
        new_b = uniform(0.7, 1.0)

        # Créer une animation pour changer la couleur
        anim = Animation(duration=2)  # Durée de 2 secondes
        anim.bind(on_progress=lambda *args: self.update_label_color(new_r, new_g, new_b))
        anim.bind(on_complete=lambda *args: self.animate_color())  # Relancer l'animation
        anim.start(self)

    def update_label_color(self, r, g, b):
        """Met à jour la couleur du texte"""
        self.time_label.color = (r, g, b, 1)

    def update_time(self, dt):
        """Met à jour l'heure à chaque seconde"""
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.text = current_time


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
