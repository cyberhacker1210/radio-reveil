from datetime import datetime
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

alarm_time = None
sound = None
say_stop = False

def current_hour():
    now = datetime.now()
    return now.strftime("%H:%M")

def play_alarm_sound():
    global sound
    print("load le son")
    sound = SoundLoader.load("reveil_sound.mp3")
    print("j arrive a load le son")
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

def check_alarm(current_time):
    global alarm_time, say_stop
    if alarm_time == current_time and not say_stop:
        play_alarm_sound()

def set_alarm_time(hour, minute):
    global alarm_time, say_stop
    alarm_time = f"{int(hour):02}:{int(minute):02}"
    say_stop = False
    print(f"Alarme réglée pour: {alarm_time}")
