from SGP4.parser import readTle
import requests
from config import config
from pprint import pp

tle_sources = config.load("../config/config.yml")["tle"]

for source in tle_sources:
    response = requests.get(source["source"])
    tle_list = list(filter(lambda x: x.satnum in source["sats"],readTle(response.text)))
    pp(tle_list)


