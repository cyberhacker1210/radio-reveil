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
    conf.label_resultat.configure(text=f"Vous avez saisi : {alarm_hour}")
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
    
    # Obtenir la taille réelle de l'écran
    screen_width = conf.fenetre.winfo_screenwidth()
    screen_height = conf.fenetre.winfo_screenheight()

    # Simuler plein écran sans déborder
    conf.fenetre.geometry(f"{screen_width}x{screen_height}+0+0")
    conf.fenetre.overrideredirect(True)  # Retire la barre de titre
    #conf.fenetre.attributes("-topmost", True)  # Toujours au-dessus

    conf.fenetre.title("radio reveil")
    conf.fenetre.configure(bg="#222831")

    conf.label_hour = tk.Label(
        conf.fenetre, text=curent_hour(), font=("Arial", 40, "bold"),
        bg="#222831", fg="#FFD369"
    )
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
    conf.fenetre2 = ctk.CTkToplevel(conf.fenetre)
    conf.fenetre2.title("Sélecteur d'heure")

    screen_width = conf.fenetre.winfo_screenwidth()
    screen_height = conf.fenetre.winfo_screenheight()

    fond_sombre = "#282a36"
    texte_clair = "#f8f8f2"

    # Canvas CustomTkinter (via tkinter)
    canvas = tk.Canvas(conf.fenetre2, width=screen_width, height=screen_height, bg=fond_sombre, highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Frame intérieure
    frame = ctk.CTkFrame(canvas, fg_color=fond_sombre)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # AnalogPicker (supposé toujours en Tkinter standard)
    time_picker = AnalogPicker(frame)
    conf.time_picker = time_picker
    time_picker.pack(pady=20)

    theme = AnalogThemes(time_picker)
    theme.setDracula()

    # Label résultat
    label_resultat = ctk.CTkLabel(
        frame,
        text="",
        text_color=texte_clair,
        font=ctk.CTkFont("Helvetica", 16)
    )
    conf.label_resultat = label_resultat
    label_resultat.pack(pady=10)

    # Bouton arrondi CustomTkinter
    bouton = ctk.CTkButton(
        frame,
        text="Valider",
        command=recuperer_saisie,
        fg_color="#6272a4",         # Violet Dracula
        hover_color="#44475a",
        text_color=texte_clair,
        corner_radius=15,
        font=ctk.CTkFont("Helvetica", 14, weight="bold"),
        width=150,
        height=40
    )
    bouton.pack(pady=10)

    # Scroll adaptatif
    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame.bind("<Configure>", update_scrollregion)

    def start_scroll(event):
        canvas.scan_mark(event.x, event.y)

    def scroll_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    canvas.bind("<ButtonPress-1>", start_scroll)
    canvas.bind("<B1-Motion>", scroll_move)

    conf.fenetre2.resizable(True, True)






main_window()


