from pprint import pp


def passes(tle, location, opts):
    print("<+++++++++++++++++>")
    pp(tle)
    print(location)
    print(opts)
    print("<=================>")
    return ["list", "of", "passes"]


def passes_all(tles, location, opts):
    pass_list = []
    for sat in tles:
        pass_list.extend(passes(sat, location, opts))
    pass_list.sort(key=lambda x: x["startUTC"])
    return pass_list
