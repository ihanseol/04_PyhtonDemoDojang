import math

class Coordinates:
    def __init__(self):
        self.pi = math.pi
        self.semiMinorAxisA = 6377397.155
        self.flatteningF = 0.00334277318217481
        self.semiMinorAxisB = self.semiMinorAxisA * (1 - self.flatteningF)
        self.firstEccentricty = (pow(self.semiMinorAxisA, 2) - pow(self.semiMinorAxisB, 2)) / pow(self.semiMinorAxisA, 2)
        self.secondEccentricty = (pow(self.semiMinorAxisA, 2) - pow(self.semiMinorAxisB, 2)) / pow(self.semiMinorAxisB, 2)
        self.originLatitudeRadian = self.originLatitude / 180 * self.pi
        self.originLongitudeRadian = self.originLongitude / 180 * self.pi
        self.originMeridianMo = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty, 2) / 64 - 5 * pow(self.firstEccentricty, 3) / 256) * self.originLatitudeRadian - (3 * self.firstEccentricty / 8 + 3 * pow(self.firstEccentricty, 2) / 32 + 45 * pow(self.firstEccentricty, 3) / 1024) * math.sin(2 * self.originLatitudeRadian) + (15 * pow(self.firstEccentricty, 2) / 256 + 45 * pow(self.firstEccentricty, 3) / 1024) * math.sin(4 * self.originLatitudeRadian) - (35 * pow(self.firstEccentricty, 3) / 3072) * math.sin(6 * self.originLatitudeRadian))
        self.originMeridianE1 = (1 - math.sqrt(1 - self.firstEccentricty)) / (1 + math.sqrt(1 - self.firstEccentricty))
        self.re = 6371.00877 / self.grid
        self.slat1 = 30.0 * self.degrad
        self.slat2 = 60.0 * self.degrad
        self.olon = 126.0 * self.degrad
        self.olat = 38.0 * self.degrad
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(math.tan(self.pi * 0.25 + self.slat2 * 0.5) / math.tan(self.pi * 0.25 + self.slat1 * 0.5))
        self.sf = pow(math.tan(self.pi * 0.25 + self.slat1 * 0.5), self.sn) * math.cos(self.slat1) / self.sn
        self.ro = self.re * self.sf / pow(math.tan(self.pi * 0.25 + self.olat * 0.5), self.sn)

    def convertToPlaneRect(self, latitude, longitude):
        phi = latitude / 180 * self.pi
        lamda = (longitude - self.correction10405Seconds) / 180 * self.pi
        t = pow(math.tan(phi), 2)
        c = (self.firstEccentricty / (1 - self.firstEccentricty)) * pow(math.cos(phi), 2)
        a = lamda - (self.originLongitude / 180 * self.pi)
        n = self.semiMinorAxisA / math.sqrt(1 - self.firstEccentricty * pow(math.sin(phi), 2))
        m = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty, 2) / 64 - 5 * pow(self.firstEccentricty, 3) / 256) * phi - (3 * self.firstEccentricty / 8 + 3 * pow(self.firstEccentricty, 2) / 32 + 45 * pow(self.firstEccentricty, 3) / 1024) * math.sin(2 * phi) + (15 * pow(self.firstEccentricty, 2) / 256 + 45 * pow(self.firstEccentricty, 3) / 1024) * math.sin(4 * phi) - (35 * pow(self.firstEccentricty, 3) / 3072) * math.sin(6 * phi))
        x = self.originAdditionValueY + self.originScaleFactorKo * n * (a + pow(a, 3) / 6 * (1 - t + c) + pow(a, 5) / 120 * (5 - 18 * t + pow(t, 2) + 72 * c - 58 * self.secondEccentricty))
        y = self.originAdditionValueX + self.originScaleFactorKo * (m - self.originMeridianMo + n * math.tan(phi) * (pow(a, 2) / 2 + pow(a, 4) / 24 * (5 + 3 * t + 10 * c - 4 * pow(c, 2) - 9 * self.secondEccentricty) + pow(a, 6) / 720 * (61 + 90 * t + 298 * c + 45 * pow(t, 2) - 252 * self.secondEccentricty - 3 * pow(c, 2))))
        return (x, y)

    def convertToLatitudeLongitude(self, tmX, tmY):
        m = self.originMeridianMo + ((tmY - self.originAdditionValueX) / self.originScaleFactorKo)
        mu1 = m / (self.semiMinorAxisA * (1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty, 2) / 64 - 5 * pow(self.firstEccentricty, 3) / 256))
        phi1 = mu1 + (3 * self.originMeridianE1 / 2 - 27 * pow(self.originMeridianE1, 3) / 32) * math.sin(2 * mu1) + (21 * pow(self.originMeridianE1, 2) / 16 - 55 * pow(self.originMeridianE1, 4) / 32) * math.sin(4 * mu1) + (151 * pow(self.originMeridianE1, 3) / 96) * math.sin(6 * mu1) + (1097 * pow(self.originMeridianE1, 4) / 512) * math.sin(8 * mu1)
        ra = self.re * self.sf / math.tan(self.pi * 0.25 + phi1 * 0.5)
        theta = 0.0
        if abs(tmX - self.originAdditionValueY) <= 0.0:
            theta = 0.0
        else:
            if abs(tmY - self.originAdditionValueX) <= 0.0:
                theta = self.pi * 0.5
                if tmX - self.originAdditionValueY < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(tmX - self.originAdditionValueY, tmY - self.originAdditionValueX)
        alat = 2 * math.atan(pow(self.re * self.sf / ra, 1 / self.sn)) - self.pi * 0.5
        alon = theta / self.sn + self.olon
        lat = alat * self.raddeg
        lon = alon * self.raddeg
        return (lat, lon)

    def convertToGrid(self, latitude, longitude):
        ra = self.re * self.sf / math.tan(self.pi * 0.25 + latitude * self.degrad * 0.5)
        theta = longitude * self.degrad - self.olon
        if theta > self.pi:
            theta -= 2 * self.pi
        if theta < -self.pi:
            theta += 2 * self.pi
        theta *= self.sn
        x = ra * math.sin(theta) + self.xo
        y = self.ro - ra * math.cos(theta) + self.yo
        return (int(x + 1.5), int(y + 1.5))

    def convertToLatitudeLongitudeGrid(self, nx, ny):
        x = nx - 1.0
        y = ny - 1.0
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0:
            ra = -ra
        alat = 2 * math.atan(pow(self.re * self.sf / ra, 1 / self.sn)) - self.pi * 0.5
        theta = 0.0
        if abs(xn) <= 0.0:
            theta = 0.0
        else:
            if abs(yn) <= 0.0:
                theta = self.pi * 0.5
                if xn < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(xn, yn)
        alon = theta / self.sn + self.olon
        lat = alat * self.raddeg
        lon = alon * self.raddeg
        return (lat, lon)

# Usage
coordinates = Coordinates()
latitude, longitude = coordinates.convertToPlaneRect(37.5665, 126.9779)
print(f"Latitude: {latitude}, Longitude: {longitude}")