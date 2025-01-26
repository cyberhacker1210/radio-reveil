from datetime import datetime
import config as conf
import pygame

def curent_hour():
    curent_date = datetime.now()
    curent_hour = curent_date.strftime("%I:%M:%p")
    type(curent_hour)

    return(curent_hour)

def day():
    curent_date = datetime.now()
    curent_day = curent_date.strftime("%d")
    return(curent_day)

def sound():
    pygame.mixer.init()
    sound = pygame.mixer.Sound("./reveil_sound.mp3")
    pygame.mixer.music.load(sound)
    duration = sound.get_length() * 1000
    conf.fenetre.after(duration, lambda: sound)

def stop_sound():
    pygame.mixer.music.stop()




def check_alarm(hour_of_alarm):
    print("toto")
    if hour_of_alarm == curent_hour():
        sound()
        print("C'est l'heure !") 
       
    else:
        conf.fenetre.after(30000, lambda: check_alarm(hour_of_alarm))
        print("toto1")


curent_hour()