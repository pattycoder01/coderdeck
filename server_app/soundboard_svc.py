# soundboard_svc.py

import os
from pygame import mixer

class SoundBoard:
    SOUND_DIR = "sounds"
    SUPPORTED_FORMATS = (".mp3", ".wav", ".ogg")

    def __init__(self):
        os.makedirs(self.SOUND_DIR, exist_ok=True)
        mixer.init()

    def play(self, filename): # plays audio file, you can plug the audio output into your mic using mixline
        full_path = os.path.join(self.SOUND_DIR, filename)
        if not filename.lower().endswith(self.SUPPORTED_FORMATS):
            raise ValueError("only .mp3, .wav or .ogg audio files allowed")
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"{filename} not found")
        mixer.music.load(full_path)
        mixer.music.play()

    def stop(self):
        mixer.music.stop()