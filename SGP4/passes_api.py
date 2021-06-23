from pprint import pp
import requests
from config import config
from SDR import tuner

key = "MQABGU-NC5PVB-K7LCCV-3XXN"


def endpoint(id, lat, lon, alt, days, elev):
    return f"radiopasses/{id}/{lat}/{lon}/{alt}/{days}/{elev}/"


def construct_url(id, lat, lon, alt, days, elev):
    base = "https://api.n2yo.com/rest/v1/satellite/"
    return base + endpoint(id, lat, lon, alt, days, elev) + "&apiKey=" + key


def passes(id, location, opts):
    url = construct_url(id.satnum, location["lat"], location["lon"], location["alt"], opts["days"], opts["elev"])
    response = requests.get(url)
    data = response.json()
    for pss in data["passes"]:
        pss["satnum"] = data["info"]["satid"]
        pss["satname"] = data["info"]["satname"]
        pss["freq"] = tuner.get_frequency(data["info"]["satid"])
    return data["passes"]


def passes_all(tles, location, opts):
    pass_list = []
    for sat in tles:
        pass_list.extend(passes(sat, location, opts))
    pass_list.sort(key=lambda x: x["startUTC"])
    return pass_list


