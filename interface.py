import tkinter as tk
from tktimepicker import AnalogPicker, AnalogThemes
from alarm import curent_hour


# Fonction pour récupérer la saisie et l'afficher
def recuperer_saisie():
    alarm_hour = time_picker.time()
    label_resultat.config(text=f"Vous avez saisi : {alarm_hour}")
    print(alarm_hour)
    return alarm_hour


def main_window():
    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.geometry("400x200")
    fenetre.title("radio reveil")
    label_hour = tk.Label(fenetre, text=curent_hour())
    label_hour.pack(pady=10)
    bouton_alarm = tk.Button(fenetre, text ="set alarm", command=alarm_picker)
    bouton_alarm.pack(pady=5)
    # Lancement de l'application
    fenetre.mainloop()



def alarm_picker():
    fenetre2 = tk.Tk()
    global time_picker 
    time_picker = AnalogPicker(fenetre2)
    time_picker.pack(expand=True, fill="both")
    theme = AnalogThemes(time_picker)
    theme.setDracula()
    # Ajout d'un label pour afficher le résultat
    global label_resultat 
    label_resultat = tk.Label(fenetre2, text="")
    label_resultat.pack(pady=10)
    # Ajout d'un bouton pour valider la saisie
    bouton = tk.Button(fenetre2, text="Valider", command=recuperer_saisie)
    bouton.pack(pady=5)



main_window()


