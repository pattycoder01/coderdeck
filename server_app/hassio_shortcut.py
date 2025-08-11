# hassio_shortcut.py

class HassioShortcut:
    def __init__(self, hassio):
        self.hassio = hassio

    def light_on(self, entity_id):
        self.hassio.call_service('light', 'turn_on', {'entity_id': entity_id})

    def light_off(self, entity_id):
        self.hassio.call_service('light', 'turn_off', {'entity_id': entity_id})

    def light_toggle(self, entity_id):
        self.hassio.call_service('light', 'toggle', {'entity_id': entity_id})

    def hue_scene(self, entity_id):
        self.hassio.call_service('hue', 'activate_scene', {'entity_id': entity_id})