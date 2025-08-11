# app.py

# import external libraries
import asyncio
import yaml
import json
from aiohttp import web
import websockets

# import helper files
from hassio_control import HassioControl
from hassio_shortcut import HassioShortcut
from soundboard_svc import SoundBoard
from obs_control import OBSControl
from discord_control import DiscordControl
from media_control import MediaControl
from function_keys import FunctionKey
from net_utils import get_local_ip
from ui_utils import show_qr_async

# load config file
with open("config/config.yaml", "r") as f:
    config_file = yaml.safe_load(f)

# setup config
BINDS_FILE_PATH = config_file["binds"]["file_path"]
DISCORD_ENABLED = config_file["discord"]["enabled"]
OBS_ENABLED = config_file["obs"]["enabled"]
HASSIO_ENABLED = config_file["home_assistant"]["enabled"]
SOUNDBOARD_ENABLED = config_file["home_assistant"]["enabled"]

# initialize control interfaces and optional config
if HASSIO_ENABLED:
    HASSIO_URL = config_file["home_assistant"]["server_ip"]
    HASSIO_TOKEN = config_file["home_assistant"]["access_token"]
    hassio = HassioControl(HASSIO_TOKEN, HASSIO_URL) # home assistant api wrapper
    hassiosc = HassioShortcut(hassio) # helper for common home assistant actions
if SOUNDBOARD_ENABLED:
    sound = SoundBoard() # local soundboard service
if OBS_ENABLED:
    OBS_IP = config_file["obs"]["server_ip"]
    OBS_PORT = config_file["obs"]["server_port"]
    obs = OBSControl(OBS_IP, OBS_PORT) # control obs studio
if DISCORD_ENABLED:
    discord = DiscordControl() # discord mute/deafen integration using hotkeys
media = MediaControl() # media control (e.g. play/pause)
fkey = FunctionKey() # function key mapping (keys f1 to f24)

# load buttons from binds config file
def load_buttons():
    with open(BINDS_FILE_PATH, "r") as f:
        return yaml.safe_load(f)["buttons"]

# execute actions when button pressed
async def execute_action(action):
    match action:
        case "none": # default case if button is not defined
            print("none")
        case "volume_up":
            media.volume_up()
        case "volume_mute":
            media.mute()
        case "volume_down":
            media.volume_down()
        case "next":
            media.next_track()
        case "previous":
            media.previous_track()
        case "playpause":
            media.play_pause()
        case _: # execute arbitrary python code (danger)
            exec(action)

# websocket server
async def ws_handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
        except json.JSONDecodeError: # what the fuck
            continue

        buttons = load_buttons()

        if data.get("action") == "get_buttons": # initial case to send button layout to new client
            print("client connected")
            await websocket.send(json.dumps({ "action": "buttons", "buttons": buttons }))

        elif data.get("action") == "click": # receives if a specific button is pressed
            button_id = data.get("click")
            print(f"pressed {button_id}")
            if button_id in buttons:
                await execute_action(buttons[button_id].get("action"))

        elif data.get("action") == "keepalive": # keepalive handler and also automatically updates button layout
            await websocket.send(json.dumps({ "action": "buttons", "buttons": buttons }))

# start websocket server
async def start_ws():
    async with websockets.serve(ws_handler, "0.0.0.0", 8765): # on all interfaces
        await asyncio.Future()

# http server for index.html/images
async def start_http():
    app = web.Application()
    app.router.add_static("/", "./static", show_index=True)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 5000) # on all interfaces
    await site.start()

# main function
async def main():
    ip = get_local_ip()
    port = 5000
    show_qr_async(ip, port) # shows window with connection qr code and link
    print(f"Server on: {ip}:{port}/index.html") # prints server address in console
    await asyncio.gather(start_http(), start_ws()) # starts websocket/http server

asyncio.run(main())