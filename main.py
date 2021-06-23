# calculate next pass
# get frequency of next pass
# tune radio to frequency
# pipe output to wx2img
# send image to discord channel

import datetime
import time
from pprint import pp

import pause as pause

from SGP4.parser import readTle
import requests
from config import config
from SGP4.passes_api import passes_all


def timestamp(unix):
    unix = int(unix)
    return datetime.datetime.fromtimestamp(unix)


def readable(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M')


def task(name, freq, end):
    # It is now time
    # Run the task of imaging at frequency
    print(f"Imaging {name} on {freq} MHz")
    while int(time.time()) < end:
        # Do the imaging
        pass
    main()


def main():
    tle_sources = config.load()["tle"]

    for source in tle_sources:
        response = requests.get(source["source"])
        tle_list = list(filter(lambda x: x.satnum in source["sats"], readTle(response.text)))

        observer = config.load()["observer"]
        pass_list = passes_all(tle_list, observer["location"], observer["opts"])[:3]

        pass_list = list(map(lambda x: {
            "start": timestamp(x["startUTC"]),
            "max": timestamp(x["maxUTC"]),
            "end": timestamp(x["endUTC"]),
            "num": x["satnum"],
            "name": x["satname"],
            "freq": x["freq"],
        }, pass_list))
        pp(pass_list)
        print("<--------------------------------->")

        nxt = pass_list[0]
        print(f"At {readable(nxt['start'])} {nxt['name']} will pass over until {readable(nxt['end'])}, frequency: {nxt['freq']} MHz")
        print(f"Schedule a task to tune into {nxt['freq']} MHz at {readable(nxt['start'])}")
        print(f"At {readable(nxt['end'])}, wrap up image, send it to discord and get the next pass and schedule it")
        pause.until(nxt["start"])
        task(nxt["name"], nxt["freq"], nxt["end"])


if __name__ == '__main__':
    main()
