# calculate next pass
# get frequency of next pass
# tune radio to frequency
# pipe output to wx2img
# send image to discord channel

import time
from pprint import pp

import pause as pause

from config import config
from SGP4.passes_api import passes_all
from utils import *


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

    all_tle = get_tle(tle_sources["sats"], tle_sources["sources"])
    pp(all_tle)

    # observer = config.load()["observer"]
    # pass_list = passes_all(all_tle.values(), observer["location"], observer["opts"])[:2]
    #
    # pass_list = list(map(lambda x: {
    #     "start": timestamp(x["startUTC"]),
    #     "max": timestamp(x["maxUTC"]),
    #     "end": timestamp(x["endUTC"]),
    #     "num": x["satnum"],
    #     "name": x["satname"],
    #     "freq": x["freq"],
    # }, pass_list))
    # pp(pass_list)
    # print("<--------------------------------->")
    #
    # nxt = pass_list[0]
    # print(f"At {readable(nxt['start'])} {nxt['name']} will pass over until {readable(nxt['end'])}, frequency: {nxt['freq']} MHz")
    # print(f"Schedule a task to tune into {nxt['freq']} MHz at {readable(nxt['start'])}")
    # print(f"At {readable(nxt['end'])}, wrap up image, send it to discord and get the next pass and schedule it")
    # pause.until(nxt["start"])
    # task(nxt["name"], nxt["freq"], nxt["end"])


if __name__ == '__main__':
    main()
