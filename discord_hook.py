import base64
import json
import config
import requests

file = open("testimg.txt", 'r')
content = file.read()
file.close()


def create_payload(payload):
    return json.dumps({
        "username": payload["username"],
        "embeds": [
            {
                "title": "Pass at " + payload["time"],
                "image": {
                    "url": "attachment://" + payload["image"]
                },
            }
        ]
    })


hook = config.load()["discord-webhook"]
payload = {
    "username": "NOAA 18",
    "time": "17:20",
    "image": "img.jpg"
}

files = [
    ('file1', (payload["image"], base64.decodebytes(open('testimg.txt', 'rb').read()))),
]
data = [
    ('payload_json', create_payload(payload))
]

response = requests.post(hook, files=files, data=data)

print(response.text)
