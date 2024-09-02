import math

class CoordinateConverter:
    def __init__(self):
        self.semiMinorAxisA = 6378137.0
        self.flatteningF = 1 / 298.257223563
        self.semiMinorAxisB = self.semiMinorAxisA * (1 - self.flatteningF)
        self.firstEccentricty = (self.semiMinorAxisA**2 - self.semiMinorAxisB**2) / self.semiMinorAxisA**2
        self.secondEccentricty = (self.semiMinorAxisA**2 - self.semiMinorAxisB**2) / self.semiMinorAxisB**2
        self.originLatitude = 38.0
        self.originLongitude = 127.5
        self.originLatitudeRadian = self.originLatitude / 180 * math.pi
        self.originLongitudeRadian = self.originLongitude / 180 * math.pi
        self.originMeridianMo = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * self.firstEccentricty**2 / 64 - 5 * self.firstEccentricty**3 / 256) * self.originLatitudeRadian - (3 * self.firstEccentricty / 8 + 3 * self.firstEccentricty**2 / 32 + 45 * self.firstEccentricty**3 / 1024) * math.sin(2 * self.originLatitudeRadian) + (15 * self.firstEccentricty**2 / 256 + 45 * self.firstEccentricty**3 / 1024) * math.sin(4 * self.originLatitudeRadian) - (35 * self.firstEccentricty**3 / 2072) * math.sin(6 * self.originLatitudeRadian))
        self.originMeridianE1 = (1 - math.sqrt(1 - self.firstEccentricty)) / (1 + math.sqrt(1 - self.firstEccentricty))
        self.grid = 1.0
        self.re = 6371.00877 / self.grid
        self.slat1 = 30.0 * math.pi / 180
        self.slat2 = 60.0 * math.pi / 180
        self.olon = 126.0 * math.pi / 180
        self.olat = 38.0 * math.pi / 180
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(math.tan(math.pi * 0.25 + self.slat2 * 0.5) / math.tan(math.pi * 0.25 + self.slat1 * 0.5))
        self.sf = math.pow(math.tan(math.pi * 0.25 + self.slat1 * 0.5), self.sn) * math.cos(self.slat1) / self.sn
        self.ro = self.re * self.sf / math.pow(math.tan(math.pi * 0.25 + self.olat * 0.5), self.sn)
        self.correction10405Seconds = 0.000000000664
        self.originAdditionValueY = 200000
        self.originAdditionValueX = 500000
        self.originScaleFactorKo = 0.9996
        self.xo = 400000
        self.yo = 600000
        self.raddeg = 180 / math.pi

    def convert_to_plane_rect(self, latitude, longitude):
        phi = latitude / 180 * math.pi
        lamda = (longitude - self.correction10405Seconds) / 180 * math.pi
        t = math.pow(math.tan(phi), 2)
        c = (self.firstEccentricty / (1 - self.firstEccentricty)) * math.pow(math.cos(phi), 2)
        a = (lamda - (self.originLongitude / 180 * math.pi)) * math.cos(phi)
        n = self.semiMinorAxisA / math.sqrt(1 - self.firstEccentricty * math.pow(math.sin(phi), 2))
        m = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * self.firstEccentricty**2 / 64 - 5 * self.firstEccentricty**3 / 256) * phi - (3 * self.firstEccentricty / 8 + 3 * self.firstEccentricty**2 / 32 + 45 * self.firstEccentricty**3 / 1024) * math.sin(2 * phi) + (15 * self.firstEccentricty**2 / 256 + 45 * self.firstEccentricty**3 / 1024) * math.sin(4 * phi) - 35 * self.firstEccentricty**3 / 3072 * math.sin(6 * phi))
        x = self.originAdditionValueY + self.originScaleFactorKo * n * (a + math.pow(a, 3) / 6 * (1 - t + c) + math.pow(a, 5) / 120 * (5 - 18 * t + math.pow(t, 2) + 72 * c - 58 * self.secondEccentricty))
        y = self.originAdditionValueX + self.originScaleFactorKo * (m - self.originMeridianMo + n * math.tan(phi) * (math.pow(a, 2) / 2 + math.pow(a, 4) / 24 * (5 - t + 9 * c + 4 * math.pow(c, 2)) + math.pow(a, 6) / 720 * (61 - 58 * t + math.pow(t, 2) + 600 * c - 330 * self.secondEccentricty)))
        return x, y

    def convert_to_latitude_longitude(self, tmX, tmY):
        m = self.originMeridianMo + ((tmY - self.originAdditionValueX) / self.originScaleFactorKo)
        mu1 = m / (self.semiMinorAxisA * (1 - self.firstEccentricty / 4 - 3 * self.firstEccentricty**2 / 64 - 5 * self.firstEccentricty**3 / 256))
        phi1 = mu1 + (3 * self.originMeridianE1 / 2 - 27 * self.originMeridianE1**3 / 32) * math.sin(2 * mu1) + (21 * self.originMeridianE1**2 / 16 - 55 * self.originMeridianE1**4 / 32) * math.sin(4 * mu1) + (151 * self.originMeridianE1**3 / 96) * math.sin(6 * mu1) + (1097 * self.originMeridianE1**4 / 512) * math.sin(8 * mu1)
        r1 = (self.semiMinorAxisA * (1 - self.firstEccentricty)) / (math.pow((1 - self.firstEccentricty * math.pow(math.sin(phi1), 2)), (3 / 2)))
        c1 = self.secondEccentricty * math.pow(math.cos(phi1), 2)
        t1 = math.pow(math.tan(phi1), 2)
        n1 = self.semiMinorAxisA / math.sqrt(1 - self.firstEccentricty * math.pow(math.sin(phi1), 2))
        d = (tmX - self.originAdditionValueY) / (n1 * self.originScaleFactorKo)
        phi = (phi1 - (n1 * math.tan(phi1) / r1) * (math.pow(d, 2) / 2 - math.pow(d, 4) / 24 * ( 5 + 3 * t1 + 10 * c1 - 4 * math.pow(c1, 2) - 9 * self.secondEccentricty) + math.pow(d, 6) / 720 * (61 + 90 * t1 + 298 * c1 + 45 * math.pow(t1, 2) - 252 * self.secondEccentricty - 3 * math.pow(c1, 2)))) * 180 / math.pi
        lamda = self.originLongitude + ((1 / math.cos(phi1)) * (d - (math.pow(d, 3) / 6) * (1 + 2 * t1 + c1) + (math.pow(d, 5) / 120) * (5 - 2 * c1 + 28 * t1 - 3 * math.pow(c1, 2) + 8 * self.secondEccentricty + 24 * math.pow(t1, 2)))) * 180 / math.pi + self.correction10405Seconds
        return phi, lamda

    def convert_to_grid(self, latitude, longitude):
        ra = self.re * self.sf / math.pow(math.tan(math.pi * 0.25 + latitude * math.pi / 180 * 0.5), self.sn)
        theta = longitude * math.pi / 180 - self.olon
        if theta > math.pi:
            theta -= 2.0 * math.pi
        if theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= self.sn
        x = ra * math.sin(theta) + self.xo
        y = self.ro - ra * math.cos(theta) + self.yo
        return int(x + 1.5), int(y + 1.5)

    def convert_to_latitude_longitude_from_grid(self, nx, ny):
        x = float(nx) - 1.0
        y = float(ny) - 1.0
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0:
            ra = -ra
        alat = 2.0 * math.atan(math.pow(self.re * self.sf / ra, 1.0 / self.sn)) - math.pi * 0.5
        theta = 0.0
        if abs(xn) <= 0.0:
            theta = 0.0
        else:
            if abs(yn) <= 0.0:
                theta = math.pi * 0.5
                if xn < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(xn, yn)
        alon = theta / self.sn + self.olon
        lat = alat * self.raddeg
        lon = alon * self.raddeg
        return lat, lon
