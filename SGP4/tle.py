import math

from SGP4 import utils
from SGP4.constants import C


def parseTlePower(string):
    # APPLY LEADING DECIMAL
    # from: [+|-| ]   X X X X X   [+|-] X
    # to:   [+|-]   . X X X X X e [+|-] X
    return float(string[0] + "." + string[1:5] + "e" + string[-2:])


def calcChecksum(line):
    # sum of all digits on a line ('-' counts as 1) modulo 10
    res = 0
    for char in line[:-1]:
        if not char.isdigit():
            if char == "-":
                res += 1
        else:
            res += int(char)
    return res % 10


def formatExp(n):
    return "{:4e}".format(n * 10).replace("e", "").replace(".", "").ljust(8, " ")


class Tle:
    def __init__(self, name, line1, line2):
        # name of satelite
        self.satname = name
        # number of satelite
        self.satnum = int(line1[2:7])
        # [C (classified) ,U (unclassified), S (secret🤐)]
        self.classification = line1[7]
        # year of launch (YY)
        self.idy = int(line1[9:11])
        # Launch number
        self.idn = int(line1[11:14])
        # Piece of launch
        self.idp = line1[14:17]
        # last 2 digits TLE epoch year (reference moment)
        self.epochyear = int(line1[18:20])
        # epoch day of year + fractional portion of day
        self.epochdays = float(line1[20:32])
        # date object of epoch
        self.epochdate = utils.epochDate(self.epochyear, self.epochdays)
        # first derivative of mean motion (revs/day²) => acceleration (aka ballistic coefficient)
        self.ndot = float(line1[33:43])
        # second derivative of mean motion (revs/day³) => change in acceleration
        self.nddot = parseTlePower(line1[44:52])
        # drag term / radiation pressure coefficient (1/rad)
        self.bstar = parseTlePower(line1[53:61])
        # Ephemeris type
        self.eph = int(line1[62])
        # TLE element number
        self.elem = int(line1[64:68])

        # calculate and check checksum for line 1
        checksum1 = int(line1[68])
        assert checksum1 == calcChecksum(
            line1), f"invalid TLE data on line 1 (name: {self.satname}, number: {self.satnum})"

        # check if satnums of TLE lines are the same
        assert int(line2[2:7]) == self.satnum, "TLE lines are not from the same satellite"

        # angle of inclination (degrees)
        self.inclo = float(line2[8:16])
        # right ascension of the ascending node (degrees)
        # angle between orbital plane and reference point
        self.nodeo = float(line2[17:25])
        # eccentricity of orbit
        # APPLY LEADING DECIMAL
        # distance between focal points / length of major axis
        self.ecco = float("." + line2[26:33])
        # argument of perigee (degrees)
        # angle between ascending node and perigee (closest point to earth)
        self.argpo = float(line2[34:42])
        # mean anomaly (degrees)
        # angle between true anomaly (current position on orbit) and perigee
        self.mo = float(line2[43:51])
        # mean motion (revolutions/day)
        # mean number of revolutions per day completed
        self.no = float(line2[52:61])
        # total number of revolutions at epoch
        self.revs = int(line2[63:68])

        # calculate and check checksum for line 2
        checksum2 = int(line2[68])
        assert checksum2 == calcChecksum(
            line2), f"invalid TLE data on line 2 (name: {self.satname}, number: {self.satnum})"

        # convert degrees to radians
        self.nodeo = utils.deg2rad(self.nodeo)
        self.argpo = utils.deg2rad(self.argpo)
        self.mo = utils.deg2rad(self.mo)
        self.inclo = utils.deg2rad(self.inclo)

        # convert revolutions/day to radians/minute
        self.no = self.no * 2 * math.pi / C.XMNPDA  # # rev per min in rad
        self.ndot = self.ndot * 2 * math.pi / math.pow(C.XMNPDA, 2)  # # rev / min² in rad
        self.nddot = self.nddot * 2 * math.pi / math.pow(C.XMNPDA, 3)  # # rev / min³ in rad

    def _formatLine1(self):
        idn = str(self.idn).ljust(3, "0")
        epochdays = str(round(self.epochdays, 8)).ljust(12, "0")
        ndot = str(round(self.ndot / 2 / math.pi * math.pow(C.XMNPDA, 2), 8)).replace("0", "").ljust(10, " ")
        nddot = formatExp(self.nddot / 2 / math.pi * math.pow(C.XMNPDA, 3))
        bstar = formatExp(self.bstar)
        elem = str(self.elem).ljust(4, " ")

        return f"1 {self.satnum}{self.classification} {self.idy}{idn}{self.idp} {self.epochyear}{epochdays} {ndot} {nddot} {bstar} {self.eph} {elem}"

    @property  # first decorate the getter method
    def checksum1(self):  # This getter method name is *the* name
        return calcChecksum(self._formatLine1() + "*")

    def _formatLine2(self):
        inclo = str(round(utils.rad2deg(self.inclo), 4)).ljust(8, " ")
        nodeo = str(round(utils.rad2deg(self.nodeo), 4)).ljust(8, " ")
        ecco = str(round(self.ecco, 7))[2:]
        argpo = str(round(utils.rad2deg(self.argpo), 4)).ljust(8, " ")
        mo = str(round(utils.rad2deg(self.mo), 4)).ljust(8, " ")
        no = str(round(self.no / 2 / math.pi * C.XMNPDA, 8)).ljust(11, " ")
        revs = str(self.revs).ljust(5, " ")

        return f"2 {self.satnum} {inclo} {nodeo} {ecco} {argpo} {mo} {no}{revs}"

    @property  # first decorate the getter method
    def checksum2(self):  # This getter method name is *the* name
        return calcChecksum(self._formatLine2() + "*")

    def __str__(self):
        return str(self.satname) + "\n" + str(self._formatLine1()) + str(self.checksum1) + "\n" + str(
            self._formatLine2()) + str(self.checksum2) + "\n"

    def __repr__(self):
        return str(self)
