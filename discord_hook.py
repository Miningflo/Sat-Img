import config
import requests

file = open("testimg.txt", 'r')
content = file.read()
file.close()
print(content)


hook = config.load()["discord-webhook"]
headers = {"Content-Type": "multipart/form-data"}
payload = {
    "content": "test",
    "file": content
}

x = requests.post(hook, headers=headers, data=payload)

print(x.text)
