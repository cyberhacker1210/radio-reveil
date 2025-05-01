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
    conf.fenetre.geometry("900x700")
    conf.fenetre.title("Radio Réveil")
    conf.fenetre.configure(bg="#222831")

    # Création du canvas pour le défilement horizontal
    canvas = tk.Canvas(conf.fenetre, bg="#222831", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Frame contenant toutes les pages
    container = tk.Frame(canvas, bg="#222831")
    canvas.create_window((0, 0), window=container, anchor="nw")

    # Crée les pages de chaque thème en appelant les fonctions depuis themes.py
    create_theme1(container)
    create_theme2(container)
    create_theme3(container)
    create_theme4(container)

    # Ajustement dynamique du scroll
    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    container.bind("<Configure>", update_scrollregion)

    # === Défilement instantané ===
    def on_swipe_left(event):
        canvas.xview_scroll(1, "units")

    def on_swipe_right(event):
        canvas.xview_scroll(-1, "units")

    # Liens avec le swipe
    canvas.bind("<ButtonPress-1>", on_swipe_left)
    canvas.bind("<ButtonRelease-1>", on_swipe_right)

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

    fond_dracula = "#282a36"  # Couleur de fond utilisée par le thème Dracula
    texte_clair = "#f8f8f2"

    screen_width = conf.fenetre.winfo_screenwidth()
    screen_height = conf.fenetre.winfo_screenheight()

    # Canvas de fond, couleur identique au time picker
    canvas = tk.Canvas(conf.fenetre2, width=screen_width, height=screen_height,
                       bg=fond_dracula, highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Frame interne avec fond identique
    frame = ctk.CTkFrame(canvas, fg_color=fond_dracula)
    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Ajout du AnalogPicker
    time_picker = AnalogPicker(frame)
    conf.time_picker = time_picker
    time_picker.pack(pady=0)  # Pas de marge pour coller au bord visuel

    # Appliquer thème Dracula au time picker
    theme = AnalogThemes(time_picker)
    theme.setDracula()

    # Label résultat (couleur texte cohérente)
    label_resultat = ctk.CTkLabel(
        frame,
        text="",
        text_color=texte_clair,
        font=ctk.CTkFont("Helvetica", 16)
    )
    conf.label_resultat = label_resultat
    label_resultat.pack(pady=10)

    # Bouton arrondi stylisé
    bouton = ctk.CTkButton(
        frame,
        text="Valider",
        command=recuperer_saisie,
        fg_color="#6272a4",         # Couleur cohérente avec Dracula
        hover_color="#44475a",
        text_color=texte_clair,
        corner_radius=15,
        font=ctk.CTkFont("Helvetica", 14, weight="bold"),
        width=150,
        height=40
    )
    bouton.pack(pady=10)

    # Scroll si nécessaire
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

def create_theme1(container):
    page = tk.Frame(container, width=900, height=700, bg="#222831")
    label = tk.Label(
        page,
        text=f"Style 1 - {curent_hour()}",
        font=("Arial", 40, "bold"),
        bg="#222831",
        fg="#FFD369"
    )
    label.pack(expand=True)

    # Ajouter le bouton pour accéder aux paramètres
    button_settings = ctk.CTkButton(
        page,
        text="Settings",
        command=settings,
        font=("Arial", 14),
        corner_radius=20,
        fg_color="#444",  # Gris foncé
        hover_color="#555",  # Plus clair au survol
    )
    button_settings.pack(side="bottom", pady=20)

    label.bind("<Button-1>", lambda e: settings())
    page.pack(side="left", fill="both", expand=False)

# Fonction pour créer le deuxième thème (Thème Sombre avec Effet Néon)
def create_theme2(container):
    page = tk.Frame(container, width=900, height=700, bg="#282a36")
    label = tk.Label(
        page,
        text=f"Style 2 - {curent_hour()}",
        font=("Helvetica", 50, "bold"),
        bg="#282a36",
        fg="#50fa7b"  # Couleur néon
    )
    label.pack(expand=True)

    # Ajouter le bouton pour accéder aux paramètres
    button_settings = ctk.CTkButton(
        page,
        text="Settings",
        command=settings,
        font=("Arial", 14),
        corner_radius=20,
        fg_color="#444",  # Gris foncé
        hover_color="#555",  # Plus clair au survol
    )
    button_settings.pack(side="bottom", pady=20)

    label.bind("<Button-1>", lambda e: settings())
    page.pack(side="left", fill="both", expand=False)

# Fonction pour créer le troisième thème (Thème Dynamique avec Gradient)
def create_theme3(container):
    page = tk.Frame(container, width=900, height=700)
    page.configure(bg="blue")  # Assure une couleur de fond cohérente

    canvas = tk.Canvas(page, width=900, height=700, bg="blue", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_rectangle(0, 0, 900, 700, fill="blue", outline="red")

    label = tk.Label(
        page,
        text=f"Style 3 - {curent_hour()}",
        font=("Arial", 40, "bold"),
        bg="blue",
        fg="white"
    )
    label.place(relx=0.5, rely=0.4, anchor="center")  # Position propre

    button_settings = ctk.CTkButton(
        page,
        text="Settings",
        command=settings,
        font=("Arial", 14),
        corner_radius=20,
        fg_color="#444",
        hover_color="#555"
    )
    button_settings.place(relx=0.5, rely=0.85, anchor="center")

    label.bind("<Button-1>", lambda e: settings())
    page.pack(side="left", fill="both", expand=False)

# Fonction pour créer le quatrième thème (Minimaliste avec Couleurs Pastel)
def create_theme4(container):
    page = tk.Frame(container, width=900, height=700, bg="#f8f8f2")
    label = tk.Label(
        page,
        text=f"Style 4 - {curent_hour()}",
        font=("Arial", 40, "bold"),
        bg="#f8f8f2",
        fg="#6272a4"  # Bleu pastel
    )
    label.pack(expand=True)

    # Ajouter le bouton pour accéder aux paramètres
    button_settings = ctk.CTkButton(
        page,
        text="Settings",
        command=settings,
        font=("Arial", 14),
        corner_radius=20,
        fg_color="#444",  # Gris foncé
        hover_color="#555",  # Plus clair au survol
    )
    button_settings.pack(side="bottom", pady=20)

    label.bind("<Button-1>", lambda e: settings())
    page.pack(side="left", fill="both", expand=False)







main_window()


