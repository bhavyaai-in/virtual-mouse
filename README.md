# Gesture Mouse

Turn your smartphone into a wireless trackpad and keyboard for your computer.

## Features

- **Touchpad** — Single-finger drag moves the cursor; double-tap for left click, triple-tap for right click
- **Scroll** — Swipe along the left or right edge of the screen to scroll vertically
- **Drag & drop** — Long-press for click-and-hold, then drag
- **Keyboard** — Type text directly from your phone and send it to the computer
- **Special keys** — Dedicated buttons for Enter, Backspace, Tab, Escape, arrow keys, Space, and double-click
- **macOS app/tab switcher** — Hold a bottom button and swipe horizontally to drive the Cmd+Tab or Cmd+~ switcher
- **Gyro mode** — Tilt your phone to move the cursor; sharp jerks trigger clicks
- **Voice input** — Speech-to-text via the Web Speech API (requires a supported browser)
- **Adjustable sensitivity** — Slider from 1× to 5× cursor speed
- **Dark UI** — Minimal, gesture-friendly interface optimized for mobile

## Architecture

| Component | Technology |
|---|---|
| Server | Python 3 (asyncio + websockets) |
| Mouse/keyboard control | [pynput](https://github.com/moses-palmer/pynput) |
| Frontend | Single-page HTML/JS served by the same server |
| Communication | WebSocket with JSON messages |

The Python server (`server.py`) runs on your computer, starts an HTTP + WebSocket server on port 8765, and translates incoming gesture events into mouse and keyboard actions via `pynput`. The frontend (`Touchpad.html`) is the mobile web UI that captures touch, gyro, and voice input.

## Requirements

- **Computer:** Python 3.9+ (tested on macOS)
- **Phone:** A modern browser (Safari, Chrome, Firefox)
- **Network:** Both devices on the same local network (for direct access), or a tunnel for remote access

## Installation

```bash
git clone <repo-url>
cd virtual_mouse

python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Start the server

```bash
source venv/bin/activate
python server.py
```

You should see:

```
Server running on http://0.0.0.0:8765
Open http://localhost:8765/ in your browser
```

### 2. Connect from your phone

Find your computer's local IP address:

```bash
# macOS / Linux
ipconfig getifaddr en0

# or
hostname -I
```

Open that IP in your phone's browser: `http://<your-local-ip>:8765`

The status dot in the header turns green when connected.

## Gesture Reference

| Gesture | Action |
|---|---|
| Drag one finger (center area) | Move cursor |
| Double tap | Left click |
| Triple tap | Right click |
| Drag along left/right edge | Scroll vertically |
| Long press after tap, then drag | Click-and-drag |
| Hold **Tab Switch** button + swipe | Cmd+Tab app switcher |
| Hold **App Switch** button + swipe | Cmd+~ window switcher |
| Tilt phone (Gyro mode on) | Move cursor |
| Sharp tilt (Gyro mode) | Click |

## Remote Access (Cloudflare Tunnel)

To access the touchpad from anywhere, not just your local network, set up a Cloudflare Tunnel pointing to `localhost:8765`.

## macOS Permissions

The first time you run the server, macOS will prompt for **Accessibility** permissions — this is required by `pynput` to control the mouse and keyboard. Go to **System Settings > Privacy & Security > Accessibility** and allow your terminal/IDE.
