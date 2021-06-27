def full_test():
    from config import config
    import requests
    from SGP4.parser import readTle
    from SGP4.passes_api import passes_all
    from Discord.discord_hook import send_message
    from wx2img.utils import read_file
    from wx2img.imager import data_to_img, histogram, sample_steps
    from utils import readable, timestamp

    tle_sources = config.load()["tle"]

    all_tle = []
    for source in tle_sources:
        response = requests.get(source["source"])
        all_tle.extend(list(filter(lambda x: x.satnum in source["sats"], readTle(response.text))))

    observer = config.load()["observer"]
    pass_list = passes_all(all_tle, observer["location"], observer["opts"])[:2]

    input_file = "./wx2img/test.wav"
    samplerate, data = read_file(input_file)

    hook = config.load()["discord-webhook"]
    message = {
        "hook": hook,
        "satname": pass_list[0]["satname"],
        "time": readable(timestamp(pass_list[0]["maxUTC"])),
        "image_ext": "png",
        "image_data": data_to_img(histogram(sample_steps(data, samplerate))),
        "next": pass_list[1]["satname"],
        "next_time": readable(timestamp(pass_list[1]["maxUTC"]))
    }

    send_message(message)


full_test()
