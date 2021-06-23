import re

from SGP4.tle import Tle


def readTle(fulltle):
    fulltle = re.sub(r"\s*[\r\n]$", "", fulltle, flags=re.M)
    tlelines = fulltle.split("\n")

    res = []
    tle = {}
    for line in tlelines:
        if len(line) > 24:
            if line[0] == "1":
                tle["line1"] = line
            else:
                tle["line2"] = line
                res.append(Tle(*tle.values()))
                tle = {}
        else:
            tle["name"] = line
    return res
