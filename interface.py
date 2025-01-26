import tkinter as tk
from tktimepicker import AnalogPicker, AnalogThemes
from alarm import curent_hour, check_alarm, stop_sound
import config as conf


# Fonction pour récupérer la saisie et l'afficher
def recuperer_saisie():
    alarm_hour = str(conf.time_picker.time())
    conf.label_resultat.config(text=f"Vous avez saisi : {alarm_hour}")
    print(alarm_hour)

    alarm_hour = alarm_hour.strip("()").replace("'", "")
    hours, minutes, period = map(str.strip, alarm_hour.split(','))

    hours = hours.zfill(2)
    minutes = minutes.zfill(2)

    alarm_hour = f"{hours}:{minutes}:{period}"
    print(alarm_hour)
    
    check_alarm(alarm_hour)
    close_fenetre(conf.fenetre2)
    update_label()


def close_fenetre(windows):
    try:
        windows.destroy()
        print("Fenêtre détruite")
    except Exception as e:
        print(f"Erreur lors de la destruction : {e}")

def update_label():
    conf.label_hour.config(text= curent_hour())
    conf.fenetre.after(1000, update_label)

def resize_label(event):
    # Récupérer la taille actuelle de la fenêtre
    width = conf.fenetre.winfo_width()
    height = conf.fenetre.winfo_height()

    # Adapter la taille de la police en fonction de la largeur
    font_size = int(min(width, height) * 0.3)  # 5% de la taille minimale
    conf.label_hour.config(font=("Helvetica", font_size))
    button_font_size = int(min(width, height) * 0.1)
    conf.bouton_alarm.config(font=("Helvetica", button_font_size))


def main_window():
    # Création de la fenêtre principale
    conf.fenetre = tk.Tk()
    conf.fenetre.geometry("400x200")
    conf.fenetre.title("radio reveil")
    conf.label_hour = tk.Label(conf.fenetre, text=curent_hour())
    conf.label_hour.pack(fill="both", expand=True)
    conf.bouton_alarm = tk.Button(conf.fenetre, text ="set alarm", command=alarm_picker)
    conf.bouton_alarm.pack(pady=5)
    update_label()
    conf.fenetre.bind("<Configure>", resize_label)
    conf.fenetre.mainloop()

    # Lancement de l'application


def sound_windows():
    conf.sound_windows = tk.Toplevel(conf.fenetre)
    bouton = tk.Button(conf.sound_windows, text="areter le son", command=stop_sound)
    bouton.pack(pady=5)

def alarm_picker():
    conf.fenetre2 = tk.Toplevel(conf.fenetre)
    time_picker = AnalogPicker(conf.fenetre2)
    conf.time_picker = time_picker
    time_picker.pack(expand=True, fill="both")
    theme = AnalogThemes(time_picker)
    theme.setDracula()
    # Ajout d'un label pour afficher le résultat
    label_resultat = tk.Label(conf.fenetre2, text="")
    conf.label_resultat = label_resultat
    label_resultat.pack(pady=10)
    # Ajout d'un bouton pour valider la saisie
    bouton = tk.Button(conf.fenetre2, text="Valider", command=recuperer_saisie)
    bouton.pack(pady=5)



main_window()


