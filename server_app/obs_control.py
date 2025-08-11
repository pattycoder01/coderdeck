# obs_control.py

from obsws_python import ReqClient

class OBSControl:
    def __init__(self, host='localhost', port=4455): # connects to local obs on port 4455; btw you can't have a password set for the obs websocket server
        try:
            self.client = ReqClient(host=host, port=port)
        except ConnectionRefusedError:
            self.client = None
            print("obs offline")
        except Exception:
            self.client = None
            print("obs not connected")

    def switch_scene(self, scene_name):
        if self.client:
            try:
                self.client.set_current_program_scene(scene_name)
            except Exception:
                print("failed to switch scene")
        else:
            print("obs not connected")

    def start_recording(self):
        if self.client:
            try:
                self.client.start_record()
            except Exception:
                print("failed to start recording")
        else:
            print("obs not connected")

    def stop_recording(self):
        if self.client:
            try:
                self.client.stop_record()
            except Exception:
                print("failed to stop recording")
        else:
            print("obs not connected")

    def toggle_mute(self, source_name):
        if self.client:
            try:
                self.client.toggle_input_mute(source_name)
            except Exception:
                print("failed to toggle mute")
        else:
            print("obs not connected")

    def set_transition(self, transition_name):
        if self.client:
            try:
                self.client.set_current_scene_transition(transition_name)
            except Exception:
                print("failed to set transition")
        else:
            print("obs not connected")
