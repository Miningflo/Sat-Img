# calculate next pass
# get frequency of next pass
# tune radio to frequency
# pipe output to wx2img
# send image to discord channel

import time
from pprint import pp

import pause as pause

from config import config
from utils import *
from SDR import sdr
from wx2img.imager import *
from SGP4.passes_api import passes_all
from Discord.discord_hook import send_message


def task(passes, freq, duration):
    # It is now time
    # Run the task of imaging at frequency
    print(f"Imaging {passes[0]['satname']} on {freq} MHz")
    samples, sample_rate = sdr.listen(freq, duration)
    hook = config.load()["discord-webhook"]
    message = {
        "hook": hook,
        "satname": passes[0]["satname"],
        "time": readable(passes[0]["maxUTC"]),
        "image_ext": "png",
        "image_data": data_to_img(cutoff(sample_steps(samples, sample_rate))),
        "next": passes[1]["satname"],
        "next_time": readable(passes[1]["maxUTC"])
    }

    send_message(message)
    main()


def main():
    tle_sources = config.load()["tle"]

    all_tle = get_tle(tle_sources["sats"], tle_sources["sources"])
    pp(all_tle)

    observer = config.load()["observer"]
    pass_list = passes_all(all_tle.values(), observer["location"], observer["opts"])[:2]

    pass_list = list(map(lambda x: {
        "start": x["startUTC"],
        "max": x["maxUTC"],
        "end": x["endUTC"],
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
    pause.until(int(nxt["start"]))
    task(pass_list, nxt["freq"], int(nxt["end"]) - int(nxt["start"]))


if __name__ == '__main__':
    main()
