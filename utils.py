import datetime
from SGP4.parser import readTle
import requests


def timestamp(unix):
    unix = int(unix)
    return datetime.datetime.fromtimestamp(unix)


def readable(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M')


def get_tle(sats, sources):
    all_tle = {}
    for source in sources:
        response = requests.get(source)
        parsed = readTle(response.text)
        for tle in parsed:
            if tle.satnum in sats:
                if tle.satnum in all_tle:
                    if all_tle[tle.satnum].revs < tle.revs:
                        all_tle[tle.satnum] = tle
                else:
                    all_tle[tle.satnum] = tle

    return all_tle
