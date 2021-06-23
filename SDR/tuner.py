import json

from config import config


def get_frequency(id):
    freq = config.load()["frequency"]
    file = open(freq, 'r')
    data = json.loads(file.read())
    file.close()

    return data[str(id)] if str(id) in data.keys() else None


print(get_frequency(33591))
print(get_frequency(1))
