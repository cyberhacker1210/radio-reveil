from datetime import datetime
from kivy.clock import Clock
import pygame


alarm_time = None
sound = None
say_stop = False

def current_hour():
    now = datetime.now()
    return now.strftime("%H:%M")

def play_alarm_sound():
    print("play alarm sound (pygame)")
    pygame.mixer.init()
    pygame.mixer.music.load("reveil_sound.mp3")
    pygame.mixer.music.play(-1)  # -1 pour boucle infinie
    print("Alarme en cours !")

def stop_alarm_sound():
    print("Alarme arrêtée (pygame)")
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def check_alarm(current_time):
    global alarm_time, say_stop
    if alarm_time == current_time and not say_stop:
        play_alarm_sound()

def set_alarm_time(hour, minute):
    global alarm_time, say_stop
    alarm_time = f"{int(hour):02}:{int(minute):02}"
    say_stop = False
    print(f"Alarme réglée pour: {alarm_time}")
