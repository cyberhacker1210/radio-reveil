from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch

# Définir la taille de la fenêtre pour s'adapter à l'écran 3.5"
Config.set('graphics', 'width', '480')  # largeur de l'écran
Config.set('graphics', 'height', '320')  # hauteur de l'écran
Config.set('graphics', 'resizable', '0')  # Désactiver la redimension de la fenêtre

class MainApp(App):
    def build(self):
        # Utilisation d'un FloatLayout pour un agencement plus flexible
        layout = FloatLayout()

        # Création d'un bouton "Réveil"
        wake_up_button = Button(
            text="Réveil",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        wake_up_button.bind(on_press=self.show_alarm_popup)
        layout.add_widget(wake_up_button)

        # Création d'un bouton "Paramètres"
        settings_button = Button(
            text="Paramètres",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        settings_button.bind(on_press=self.show_settings_popup)
        layout.add_widget(settings_button)

        return layout

    def show_alarm_popup(self, instance):
        # Popup simple pour l'alarme
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Label(text="Réveil activé!"))

        close_button = Button(text="Fermer")
        close_button.bind(on_press=lambda x: self.close_popup())
        popup_content.add_widget(close_button)

        self.popup = Popup(
            title="Réveil",
            content=popup_content,
            size_hint=(None, None),
            size=(300, 200)
        )
        self.popup.open()

    def show_settings_popup(self, instance):
        # Popup pour afficher les paramètres
        popup_content = BoxLayout(orientation='vertical')

        # Ajouter un slider pour ajuster l'heure de l'alarme
        time_slider = Slider(min=0, max=24, value=8)
        time_slider.bind(value=self.on_slider_value_change)
        popup_content.add_widget(Label(text="Réglage Heure"))
        popup_content.add_widget(time_slider)

        # Ajouter un switch pour activer/désactiver l'alarme
        alarm_switch = Switch(active=True)
        popup_content.add_widget(Label(text="Activer Alarme"))
        popup_content.add_widget(alarm_switch)

        close_button = Button(text="Fermer")
        close_button.bind(on_press=lambda x: self.close_popup())
        popup_content.add_widget(close_button)

        self.popup = Popup(
            title="Paramètres",
            content=popup_content,
            size_hint=(None, None),
            size=(300, 300)
        )
        self.popup.open()

    def on_slider_value_change(self, instance, value):
        # Gérer le changement de valeur du slider
        print(f"Heure de l'alarme réglée à {value}h")

    def close_popup(self):
        self.popup.dismiss()

if __name__ == "__main__":
    MainApp().run()
