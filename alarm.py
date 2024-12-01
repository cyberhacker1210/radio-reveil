from datetime import datetime

def curent_hour():
    curent_date = datetime.now()
    curent_hour = curent_date.strftime("%H:%M")
    return(curent_hour)

def day():
    curent_date = datetime.now()
    curent_day = curent_date.strftime("%d")
    return(curent_day)

def alarm(alarm_hour):
    if alarm_hour == curent_hour():
        print("c'est l'heure")

