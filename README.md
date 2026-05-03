# radio-reveil — Internet Radio Alarm Clock

A Python alarm clock that automatically plays an internet radio stream at a set time. Runs on any machine or Raspberry Pi.

## Tech Stack

| Technology | Usage |
|---|---|
| Python 3 | Main language |
| pygame / vlc | Audio streaming |
| schedule | Task scheduling |
| datetime | Time management |
| requests | Stream URL validation |

## How it works

```
User sets alarm time + radio stream URL
              ↓
Python scheduler runs in background
              ↓
System clock reaches alarm time
              ↓
Audio plays through speakers
              ↓
Auto-stop after X minutes (optional)
```

## Features

- Custom alarm time (HH:MM format)
- Play any internet radio stream URL
- Auto-stop timer
- Lightweight — runs on Raspberry Pi
- Simple CLI interface

## Project Structure

```
radio-reveil/
├── main.py           # Entry point & scheduler
├── player.py         # Audio stream player
├── config.py         # Alarm settings
├── requirements.txt
└── README.md
```

## Getting Started

**Prerequisites:** Python 3.8+, pip, speakers

```bash
git clone https://github.com/cyberhacker1210/radio-reveil
cd radio-reveil
pip install -r requirements.txt
```

Edit `config.py`:

```python
ALARM_TIME = "07:30"
RADIO_URL = "http://your-radio-stream-url.mp3"
STOP_AFTER = 30  # minutes
```

```bash
python main.py
```

### Example stream URLs

```
France Inter:  http://direct.franceinter.fr/live/franceinter-midfi.mp3
NRJ:           http://cdn.nrjaudio.fm/adwz1/fr/30001/mp3_128.mp3
```

### Auto-start on Raspberry Pi

```bash
crontab -e
# Add:
@reboot python3 /home/pi/radio-reveil/main.py
```

## Author

**cyberhacker1210** — [GitHub](https://github.com/cyberhacker1210)
