# radio-reveil
it work on every platform who's suporting python
how to launch it :

# step 1
    clone the repo ;)
    i hope you d'ont be block at this step
    don't forget to import all the lib

# step 2
    launch the code 

# tips for rpi 

# LXDE Autostart
```bash
nano ~/.config/lxsession/LXDE-pi/autostart  
@/home/leo/radio-reveil/.venv/bin/python /home/leo/radio-reveil/main.py  
```

# systemd user service

```bash
mkdir -p ~/.config/systemd/user  
nano ~/.config/systemd/user/radio-reveil.service  
```

## Contenu du fichier `radio-reveil.service`

```bash

[Unit]  
Description=Radio-Reveil Kivy GUI  
After=graphical.target  

[Service]  
Type=simple  
ExecStart=/home/leo/radio-reveil/.venv/bin/python /home/leo/radio-reveil/main.py  
Restart=always  
Environment=DISPLAY=:0  
WorkingDirectory=/home/leo/radio-reveil  

[Install]  
WantedBy=default.target  

```
## Activation du service

```bash

systemctl --user daemon-reload  
systemctl --user enable radio-reveil.service  
systemctl --user start radio-reveil.service  
```


