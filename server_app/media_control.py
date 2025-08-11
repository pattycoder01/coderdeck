# media_control.py

import win32api
import win32con

class MediaControl: # sends virtual key presses for play/pause, etc.
    @staticmethod
    def play_pause():
        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)

    @staticmethod
    def next_track():
        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)

    @staticmethod
    def previous_track():
        win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)

    @staticmethod
    def volume_up():
        win32api.keybd_event(win32con.VK_VOLUME_UP, 0, 0, 0)

    @staticmethod
    def volume_down():
        win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, 0, 0)

    @staticmethod
    def mute():
        win32api.keybd_event(win32con.VK_VOLUME_MUTE, 0, 0, 0)
