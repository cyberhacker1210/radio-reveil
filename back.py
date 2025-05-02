from datetime import datetime
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

sound = None
say_stop = False

def current_hour():
    now = datetime.now()
    return now.strftime("%I:%M:%p")  # exemple: "07:45:PM"

def day():
    return datetime.now().strftime("%d")

def play_alarm_sound():
    global sound, say_stop
    sound = SoundLoader.load("./reveil_sound.mp3")
    if sound:
        sound.loop = True
        sound.play()
        print("Alarme en cours !")

def stop_alarm_sound():
    global sound, say_stop
    if sound:
        sound.stop()
        sound.unload()
        sound = None
    say_stop = True
    print("Alarme arrêtée")

def check_alarm(target_hour):
    now = current_hour()
    print(f"Vérification: {now} vs {target_hour}")
    if now == target_hour and not say_stop:
        play_alarm_sound()
    else:
        Clock.schedule_once(lambda dt: check_alarm(target_hour), 30)  # recheck dans 30 sec
