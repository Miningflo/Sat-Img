# calculate next pass
# get frequency of next pass
# tune radio to frequency
# pipe output to wx2img
# send image to discord channel

import datetime
from pprint import pp
from SGP4.parser import readTle
import requests
from config import config
from SGP4.passes_api import passes_all


def unix2date(unix):
    unix = int(unix)
    return datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M')


def task(name, freq):
    # It is now time
    # Run the task of imaging at frequency
    main()


def main():
    tle_sources = config.load()["tle"]

    for source in tle_sources:
        response = requests.get(source["source"])
        tle_list = list(filter(lambda x: x.satnum in source["sats"], readTle(response.text)))

        observer = config.load()["observer"]
        pass_list = passes_all(tle_list, observer["location"], observer["opts"])[:3]

        pass_list = list(map(lambda x: {
            "start": unix2date(x["startUTC"]),
            "max": unix2date(x["maxUTC"]),
            "end": unix2date(x["endUTC"]),
            "num": x["satnum"],
            "name": x["satname"],
            "freq": x["freq"],
        }, pass_list))
        # pp(pass_list)

        nxt = pass_list[0]
        print(f"At {nxt['start']} {nxt['name']} will pass over until {nxt['end']}, frequency: {nxt['freq']} MHz")
        print(f"Schedule a task to tune into {nxt['freq']} MHz at {nxt['start']}")
        print(f"At {nxt['end']}, wrap up image, send it to discord and get the next pass and schedule it")


if __name__ == '__main__':
    main()
