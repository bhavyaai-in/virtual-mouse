import asyncio
import json
import websockets
import logging
import email.utils
from pathlib import Path
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from websockets.datastructures import Headers
from websockets.http11 import Response

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

mouse = MouseController()
keyboard = KeyboardController()

HTML_FILE = Path(__file__).parent / "Touchpad.html"

_cmd_held = False
_scroll_acc = 0.0

SPECIAL_KEYS = {
    "enter": Key.enter,
    "backspace": Key.backspace,
    "tab": Key.tab,
    "escape": Key.esc,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "space": Key.space,
}


def hold_cmd():
    global _cmd_held
    if not _cmd_held:
        keyboard.press(Key.cmd)
        _cmd_held = True


def release_cmd():
    global _cmd_held
    if _cmd_held:
        keyboard.release(Key.cmd)
        _cmd_held = False


def handle_event(data):
    global _cmd_held
    event = data.get("event")
    pass_list=["Client connected!","connection open",None,"None"]
    if event not in pass_list:
        print("event : ",event)
    if event == "move":
        dx, dy = data.get("dx", 0), data.get("dy", 0)
        x, y = mouse.position
        mouse.position = (x + dx, y + dy)

    elif event == "motion":
        x = data.get("x", 0) * 3
        y = data.get("y", 0) * 3
        mx, my = mouse.position
        mouse.position = (mx + x, my + y)

    elif event == "click":
        button = data.get("button", "left")
        btn = Button.left if button == "left" else Button.right
        mouse.click(btn)

    elif event == "double_click":
        mouse.click(Button.left, 2)

    elif event == "scroll":
        dy = data.get("dy", 0)
        global _scroll_acc
        if dy != 0:
            _scroll_acc -= dy

    elif event == "click_hold":
        button = data.get("button", "left")
        state = data.get("state")
        btn = Button.left if button == "left" else Button.right
        if state == "start":
            mouse.press(btn)
        elif state == "end":
            mouse.release(btn)

    elif event == "drag_move":
        dx, dy = data.get("dx", 0), data.get("dy", 0)
        x, y = mouse.position
        mouse.position = (x + dx, y + dy)

    elif event == "special_key":
        key = data.get("key", "")
        if key in SPECIAL_KEYS:
            keyboard.tap(SPECIAL_KEYS[key])

    elif event == "cmd_hold_start":
        hold_cmd()

    elif event == "cmd_hold_tab":
        keyboard.tap(Key.tab)

    elif event == "cmd_hold_shift_tab":
        keyboard.press(Key.shift)
        keyboard.tap(Key.tab)
        keyboard.release(Key.shift)

    elif event == "cmd_hold_tilde":
        keyboard.press(KeyCode(vk=50))
        keyboard.release(KeyCode(vk=50))

    elif event == "cmd_hold_shift_tilde":
        keyboard.press(Key.shift)
        keyboard.press(KeyCode(vk=50))
        keyboard.release(KeyCode(vk=50))
        keyboard.release(Key.shift)

    elif event == "cmd_hold_end":
        release_cmd()

    elif event == "keypress":
        key = data.get("key", "")
        if key:
            keyboard.type(key)


async def process_request(connection, request):
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return None

    if request.path == "/" or request.path.endswith(".html"):
        try:
            content = HTML_FILE.read_text()
            body = content.encode()
            headers = Headers([
                ("Date", email.utils.formatdate(usegmt=True)),
                ("Connection", "close"),
                ("Content-Length", str(len(body))),
                ("Content-Type", "text/html; charset=utf-8"),
            ])
            return Response(200, "OK", headers, body)
        except FileNotFoundError:
            return connection.respond(404, "Not found")

    return connection.respond(404, "Not found")

# how to do it




async def handle_connection(websocket):
    # logger.info("Client connected!")
    try:
        await websocket.send(json.dumps({"type": "connected", "role": "phone"}))
        await websocket.send(json.dumps({"type": "mac_status", "connected": True}))

        async for message in websocket:
            data = json.loads(message)
            if data.get("event") == "ping" or data.get("type") == "ping":
                await websocket.send(json.dumps({"type": "pong"}))
                continue
            handle_event(data)

    except websockets.exceptions.ConnectionClosed:
        logger.info("Client disconnected.")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        release_cmd()


async def scroll_flusher():
    global _scroll_acc
    while True:
        await asyncio.sleep(1 / 30)
        if _scroll_acc != 0:
            steps = int(_scroll_acc)
            if steps != 0:
                _scroll_acc -= steps
                mouse.scroll(0, steps)
            else:
                _scroll_acc = 0


async def main():
    asyncio.create_task(scroll_flusher())
    async with websockets.serve(
        handle_connection,
        "0.0.0.0",
        8765,
        process_request=process_request,
    ):
        logger.info("Server running on http://0.0.0.0:8765")
        logger.info("Open http://localhost:8765/ in your browser")
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped.")
