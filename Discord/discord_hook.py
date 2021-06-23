import base64
import json
from config import config
import requests


def send_message(message_data):
    files = [
        ('file1', ("generic_name." + message_data["image_ext"], message_data["image_data"])),
    ]
    data = [
        ('payload_json', create_payload(message_data))
    ]
    requests.post(message_data["hook"], files=files, data=data)


def create_payload(message_data):
    return json.dumps({
        "username": message_data["satname"],
        "embeds": [
            {
                "title": "Pass at " + message_data["time"],
                "image": {
                    "url": "attachment://generic_name." + message_data["image_ext"]
                },
            }
        ]
    })


hook = config.load()["discord-webhook"]
image = base64.decodebytes(open('testimg.txt', 'rb').read())
message = {
    "hook": hook,
    "satname": "NOAA 18",
    "time": "17:20",
    "image_ext": "jpg",
    "image_data": image
}

send_message(message)
