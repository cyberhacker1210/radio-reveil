# -*- coding: utf-8 -*-

import tkinter as tk
import customtkinter as ctk
from tktimepicker import AnalogPicker, AnalogThemes
from alarm import curent_hour, check_alarm, stop_sound
from tkinter import PhotoImage
import config as conf


# Fonction pour récupérer la saisie et l'afficher
ctk.set_appearance_mode("dark")  # "light" ou "dark"
ctk.set_default_color_theme("blue")  # "green", "dark-blue"
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

def main_window():
    conf.fenetre = tk.Tk()
    conf.fenetre.geometry(f"900x700")
    conf.fenetre.title("radio reveil")
    conf.fenetre.configure(bg="#222831")

    conf.label_hour = tk.Label(conf.fenetre, text=curent_hour(), font=("Arial", 40, "bold"), bg="#222831", fg="#FFD369")
    conf.label_hour.pack(fill="both", expand=True)
    conf.label_hour.bind("<Button-1>", lambda event: settings())
    update_label()
    conf.fenetre.bind("<Configure>", resize_label)
    conf.fenetre.mainloop()

def settings():
    conf.fenetre3 = ctk.CTkToplevel(conf.fenetre)
    conf.fenetre3.title("Settings")
    conf.fenetre3.configure(bg="#222831")

    # Définir le style du bouton global
    button_style = {
        "font": ("Arial", 12),
        "corner_radius": 20,
        "fg_color": "#444",  # Couleur de fond (gris foncé)
        "hover_color": "#555",  # Couleur au survol (plus claire)
    }

    # Appliquer ce style à tous les boutons
    conf.bouton_sound = ctk.CTkButton(
        conf.fenetre3, text=" Stop sound",
        command=stop_sound, **button_style
    )
    conf.bouton_sound.pack(side="left", padx=10, pady=5, fill="both", expand=True)

    conf.bouton_alarm = ctk.CTkButton(
        conf.fenetre3, text=" Set Alarm",
        command=alarm_picker, **button_style
    )
    conf.bouton_alarm.pack(side="left", padx=10, pady=5, fill="both", expand=True)

    conf.bouton_close = ctk.CTkButton(
        conf.fenetre3, text="close settings",
        command=lambda: close_fenetre(conf.fenetre3), **button_style
    )
    conf.bouton_close.pack(side="left", padx=10, pady=5, fill="both", expand=True)

    conf.fenetre3.mainloop()



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


