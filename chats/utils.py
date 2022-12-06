import json
import requests
from django.conf import settings


def publish_message(new_message, channel="chat"):
    print(new_message)
    command = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": str(new_message)
        }
    }

    api_key = settings.API_KEY
    data = json.dumps(command)
    headers = {'Content-type': 'application/json', 'Authorization': 'apikey ' + api_key}
    print(requests.post("http://localhost:8000/api", data=data, headers=headers))
