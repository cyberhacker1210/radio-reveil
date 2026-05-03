# radio-reveil — Alarm Clock with Touchscreen UI

A Raspberry Pi alarm clock with a fullscreen touchscreen interface built with Kivy/KivyMD. The clock display bounces around the screen with animated color changes (screensaver style), and triggers an audio alarm at a set time via pygame.

## Hardware

- Raspberry Pi (any model with audio output)
- Touchscreen display (fullscreen, auto-detected)
- Speakers connected via 3.5mm jack or USB

## Tech Stack

| Technology | Usage |
|---|---|
| Python 3 | Main language |
| Kivy | Touchscreen UI framework |
| KivyMD | Material Design components (MDTimePicker) |
| pygame | Audio playback for the alarm |
| datetime | Time tracking and alarm comparison |

## How it works

```
Raspberry Pi boots
        ↓
Kivy app launches in fullscreen
        ↓
MainScreen: clock bounces around screen with color animation
        ↓
User taps the clock → goes to SettingsScreen
        ↓
User picks alarm time via MDTimePicker
        ↓
Every second: current time checked against alarm time
        ↓
Match found → pygame plays reveil_sound.mp3 on loop
        ↓
User taps "Arrêter l'alarme" → sound stops
```

## Screens

**MainScreen** — fullscreen clock that bounces around the display like a screensaver. The label moves at 60 FPS, bounces off screen edges, and smoothly cycles through pastel colors. Tap the label to open settings.

**SettingsScreen** — three buttons: go back to clock, stop the alarm, or set a new alarm time.

**SetAlarmScreen** — hour and minute sliders to pick the alarm time, with a confirm button.

## Project Structure

```
radio-reveil/
├── main.py              # App entry point, all screen logic
├── back.py              # Audio backend (pygame: play / stop alarm)
├── reveil_sound.mp3     # Alarm sound file (must be present)
└── README.md
```

## Getting Started

**Prerequisites:** Python 3.8+, pip, touchscreen display, speakers

```bash
git clone https://github.com/cyberhacker1210/radio-reveil
cd radio-reveil
pip install kivy kivymd pygame
```

Place your alarm sound file at the root of the project:

```
radio-reveil/
└── reveil_sound.mp3
```

```bash
python main.py
```

The app launches in fullscreen automatically (`Config.set('graphics', 'fullscreen', 'auto')`).

### Auto-start on Raspberry Pi boot

```bash
crontab -e
# Add:
@reboot cd /home/pi/radio-reveil && python3 main.py
```

Or use a systemd service for better control over display environment variables (recommended for a dedicated screen).

## Notes

- The alarm sound loops infinitely (`pygame.mixer.music.play(-1)`) until manually stopped.
- Alarm check runs every second via Kivy's `Clock.schedule_interval`.
- The app uses KivyMD's dark theme with a BlueGray primary palette.

## Author

**cyberhacker1210** — [GitHub](https://github.com/cyberhacker1210)
