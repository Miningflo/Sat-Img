import datetime


def timestamp(unix):
    unix = int(unix)
    return datetime.datetime.fromtimestamp(unix)


def readable(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M')