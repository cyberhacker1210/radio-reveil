# config.py

# Variables globales de configuration
say_stop = False   # Variable pour savoir si l'alarme est arrêtée ou non
fenetre = None     # Cette variable pourrait représenter une fenêtre spécifique ou une autre partie de l'interface

def reset_config():
    """Réinitialise les paramètres de configuration"""
    global say_stop, fenetre
    say_stop = False
    fenetre = None

