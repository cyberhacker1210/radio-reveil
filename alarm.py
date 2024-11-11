from datetime import datetime

def hour():
    curent_date = datetime.now()
    curent_hour = curent_date.strftime("%H:%M")

    
    print(curent_hour)

def day():
    curent_date = datetime.now()
    curent_day = curent_date.strftime("%d")
    print(curent_day)


day()