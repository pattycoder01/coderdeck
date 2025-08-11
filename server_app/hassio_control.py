# hassio_control.py

import requests

class HassioControl:
    def __init__(self, token, base_url="http://homeassistant.local:8123"): # init function
        self.token = token
        self.api_url = f"{base_url}/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_state(self, entity_id): # gets entity state
        url = f"{self.api_url}/states/{entity_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"error getting state of {entity_id}: {response.status_code}")
            return None

    def call_service(self, domain, service, data):
        url = f"{self.api_url}/services/{domain}/{service}"
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code in (200, 201):
            print(f"{service} run with entity {data.get('entity_id')}")
            return True
        else:
            print(f"error calling service {service}: {response.status_code}")
            return False

# example code
'''
# turn on light
hass.call_service("light", "turn_on", {"entity_id": "light.yourlight"})

# get sensor state
state = hass.get_state("sensor.yoursensor")
print(state)
'''