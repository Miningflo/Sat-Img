import math
import datetime

PI = math.pi


def deg2rad(deg):
    return deg / 180 * PI


def rad2deg(rad):
    return rad * 180 / PI


def sinDeg(deg):
    return math.sin(deg2rad(deg))


def cosDeg(deg):
    return math.cos(deg2rad(deg))


def asinDeg(x):
    return rad2deg(math.asin(x))


# /**
#  * Convert day, year to javascript date
#  * @param int year    last 2 digits of year
#  * @param float days  passed days this year
#  * @returns javascript date object
#  */
def epochDate(year, days):
    yr = year + 2000 if year < 57 else year + 1900
    date = datetime.datetime(yr, 1, 1)
    date += datetime.timedelta(seconds=days * 86400000)  # support for fractional days
    return date


# /**
#  * Calculate coordinates of vertical position of the sun
#  * Source: https://en.wikipedia.org/wiki/Position_of_the_Sun#Calculations
#  * @param Date date
#  * @returns lat: number, lon: number
#  */
def getSolarPosition(date):
    # calculate declination of the sun
    first = datetime.datetime(date.getFullYear(), 0, 1)  # jan 1st
    n = ((date - first) / 1000 / 60 / 60 / 24)  # days since jan 1st (not rounded)
    # inclination of orbital plane = -23.44
    # eccentricity of earths orbit = 0.0167
    declination = asinDeg(
        sinDeg(-23.44) *
        cosDeg(
            360 / 365.24 * (n + 10) +
            360 / PI * 0.0167 *
            sinDeg(
                360 / 365.24 * (n - 2)
            )
        )
    )
    t = date.getUTCHours() + date.getUTCMinutes() / 60 + date.getUTCSeconds() / 3600 + date.getUTCMilliseconds() / 3600000
    lon = declination
    lat = 180 - 15 * t
    # ENHANCEMENT: Use other coordinate system with distance from earth included
    return lat, lon
