# discord_control.py

import keyboard

class DiscordControl: # just sends key presses on virtual keys f13 and f14, needs to be set in discord too
    @staticmethod
    def mute():
        keyboard.send('f13')

    @staticmethod
    def deafen():
        keyboard.send('f14')