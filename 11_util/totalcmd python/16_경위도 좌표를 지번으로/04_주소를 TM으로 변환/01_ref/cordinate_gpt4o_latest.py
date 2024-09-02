import math


class CoordinateConverter:
    def __init__(self):
        self.pi = math.pi
        self.degrad = self.pi / 180.0
        self.raddeg = 180.0 / self.pi
        self.grid = 5.0
        self.semiMinorAxisA = 6378137.0
        self.flatteningF = 1 / 298.257223563
        self.originLatitude = 38.0
        self.originLongitude = 127.0
        self.correction10405Seconds = 0.0
        self.originScaleFactorKo = 1.0
        self.originAdditionValueX = 200000.0
        self.originAdditionValueY = 500000.0
        self.xo = 43
        self.yo = 136

        # Initialization calculations
        self.semiMinorAxisB = self.semiMinorAxisA * (1 - self.flatteningF)
        self.firstEccentricty = (pow(self.semiMinorAxisA, 2) - pow(self.semiMinorAxisB, 2)) / pow(self.semiMinorAxisA,
                                                                                                  2)
        self.secondEccentricty = (pow(self.semiMinorAxisA, 2) - pow(self.semiMinorAxisB, 2)) / pow(self.semiMinorAxisB,
                                                                                                   2)
        self.originLatitudeRadian = self.originLatitude * self.degrad
        self.originLongitudeRadian = self.originLongitude * self.degrad
        self.originMeridianMo = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty,
                                                                                                2) / 64 - 5 * pow(
            self.firstEccentricty, 3) / 256) * self.originLatitudeRadian -
                                                       (3 * self.firstEccentricty / 8 + 3 * pow(self.firstEccentricty,
                                                                                                2) / 32 + 45 * pow(
                                                           self.firstEccentricty, 3) / 1024) * math.sin(
                    2 * self.originLatitudeRadian) +
                                                       (15 * pow(self.firstEccentricty, 2) / 256 + 45 * pow(
                                                           self.firstEccentricty, 3) / 1024) * math.sin(
                    4 * self.originLatitudeRadian) -
                                                       (35 * pow(self.firstEccentricty, 3) / 3072) * math.sin(
                    6 * self.originLatitudeRadian))
        self.originMeridianE1 = (1 - math.sqrt(1 - self.firstEccentricty)) / (1 + math.sqrt(1 - self.firstEccentricty))
        self.re = 6371.00877 / self.grid
        self.slat1 = 30.0 * self.degrad
        self.slat2 = 60.0 * self.degrad
        self.olon = 126.0 * self.degrad
        self.olat = 38.0 * self.degrad
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(
            math.tan(self.pi * 0.25 + self.slat2 * 0.5) / math.tan(self.pi * 0.25 + self.slat1 * 0.5))
        self.sf = pow(math.tan(self.pi * 0.25 + self.slat1 * 0.5), self.sn) * math.cos(self.slat1) / self.sn
        self.ro = self.re * self.sf / pow(math.tan(self.pi * 0.25 + self.olat * 0.5), self.sn)

    def convertToPlaneRect(self, latitude: float, longitude: float) -> (float, float):
        phi = latitude * self.degrad
        lamda = (longitude - self.correction10405Seconds) * self.degrad
        t = pow(math.tan(phi), 2)
        c = (self.firstEccentricty / (1 - self.firstEccentricty)) * pow(math.cos(phi), 2)
        a = (lamda - self.originLongitudeRadian) * math.cos(phi)
        n = self.semiMinorAxisA / math.sqrt(1 - self.firstEccentricty * pow(math.sin(phi), 2))
        m = self.semiMinorAxisA * ((1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty, 2) / 64 - 5 * pow(
            self.firstEccentricty, 3) / 256) * phi -
                                   (3 * self.firstEccentricty / 8 + 3 * pow(self.firstEccentricty, 2) / 32 + 45 * pow(
                                       self.firstEccentricty, 3) / 1024) * math.sin(2 * phi) +
                                   (15 * pow(self.firstEccentricty, 2) / 256 + 45 * pow(self.firstEccentricty,
                                                                                        3) / 1024) * math.sin(4 * phi) -
                                   35 * pow(self.firstEccentricty, 3) / 3072 * math.sin(6 * phi))
        x = self.originAdditionValueY + self.originScaleFactorKo * n * (
                    a + pow(a, 3) / 6 * (1 - t + c) + pow(a, 5) / 120 * (
                        5 - 18 * t + pow(t, 2) + 72 * c - 58 * self.secondEccentricty))
        y = self.originAdditionValueX + self.originScaleFactorKo * (m - self.originMeridianMo + n * math.tan(phi) * (
                    pow(a, 2) / 2 + pow(a, 4) / 24 * (5 - t + 9 * c + 4 * pow(c, 2)) + pow(a, 6) / 720 * (
                        61 - 58 * t + pow(t, 2) + 600 * c - 330 * self.secondEccentricty)))
        return (x, y)

    def convertToLatitudeLongitude(self, tmX: float, tmY: float) -> (float, float):
        m = self.originMeridianMo + ((tmY - self.originAdditionValueX) / self.originScaleFactorKo)
        mu1 = m / (self.semiMinorAxisA * (
                    1 - self.firstEccentricty / 4 - 3 * pow(self.firstEccentricty, 2) / 64 - 5 * pow(
                self.firstEccentricty, 3) / 256))
        phi1 = mu1 + (3 * self.originMeridianE1 / 2 - 27 * pow(self.originMeridianE1, 3) / 32) * math.sin(2 * mu1) + (
                    21 * pow(self.originMeridianE1, 2) / 16 - 55 * pow(self.originMeridianE1, 4) / 32) * math.sin(
            4 * mu1) + (151 * pow(self.originMeridianE1, 3) / 96) * math.sin(6 * mu1) + (
                           1097 * pow(self.originMeridianE1, 4) / 512) * math.sin(8 * mu1)
        r1 = (self.semiMinorAxisA * (1 - self.firstEccentricty)) / (
            pow((1 - self.firstEccentricty * pow(math.sin(phi1), 2)), (3 / 2)))
        c1 = self.secondEccentricty * pow(math.cos(phi1), 2)
        t1 = pow(math.tan(phi1), 2)
        n1 = self.semiMinorAxisA / math.sqrt(1 - self.firstEccentricty * pow(math.sin(phi1), 2))
        d = (tmX - self.originAdditionValueY) / (n1 * self.originScaleFactorKo)
        phi = (phi1 - (n1 * math.tan(phi1) / r1) * (pow(d, 2) / 2 - pow(d, 4) / 24 * (
                    5 + 3 * t1 + 10 * c1 - 4 * pow(c1, 2) - 9 * self.secondEccentricty) + pow(d, 6) / 720 * (
                                                                61 + 90 * t1 + 298 * c1 + 45 * pow(t1,
                                                                                                   2) - 252 * self.secondEccentricty - 3 * pow(
                                                            c1, 2)))) * self.raddeg
        lamda = self.originLongitude + ((1 / math.cos(phi1)) * (
                    d - (pow(d, 3) / 6) * (1 + 2 * t1 + c1) + (pow(d, 5) / 120) * (
                        5 - 2 * c1 + 28 * t1 - 3 * pow(c1, 2) + 8 * self.secondEccentricty + 24 * pow(t1,
                                                                                                      2)))) * self.raddeg + self.correction10405Seconds
        return (phi, lamda)

    def convertToGrid(self, latitude: float, longitude: float) -> (int, int):
        ra = self.re * self.sf / pow(math.tan(self.pi * 0.25 + latitude * self.degrad * 0.5), self.sn)
        theta = longitude * self.degrad - self.olon
        if theta > self.pi:
            theta -= 2.0 * self.pi
        if theta < -self.pi:
            theta += 2.0 * self.pi
        theta *= self.sn
        x = ra * math.sin(theta) + self.xo
        y = self.ro - ra * math.cos(theta) + self.yo
        return (int(x + 1.5), int(y + 1.5))

    def convertToLatitudeLongitudeFromGrid(self, nx: int, ny: int) -> (float, float):
        x = float(nx) - 1.0
        y = float(ny) - 1.0
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0:
            ra = -ra
        alat = 2.0 * math.atan(pow(self.re * self.sf / ra, 1.0 / self.sn)) - self.pi * 0.5
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


# Example usage:
converter = CoordinateConverter()

# Convert latitude and longitude to plane rectangular coordinates
plane_rect_coords = converter.convertToPlaneRect(37.5665, 126.9780)
print("Plane Rectangular Coordinates:", plane_rect_coords)

# Convert TM coordinates to latitude and longitude
lat_lon_coords = converter.convertToLatitudeLongitude(plane_rect_coords[0], plane_rect_coords[1])
print("Latitude and Longitude:", lat_lon_coords)

# Convert latitude and longitude to grid coordinates
grid_coords = converter.convertToGrid(37.5665, 126.9780)
print("Grid Coordinates:", grid_coords)

# Convert grid coordinates to latitude and longitude
lat_lon_from_grid = converter.convertToLatitudeLongitudeFromGrid(grid_coords[0], grid_coords[1])
print("Latitude and Longitude from Grid:", lat_lon_from_grid)
