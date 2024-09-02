import math

class Coordinates:
    def __init__(self):
        self.pi = math.pi
        self.semi_minor_axis_a = 6377397.155  # 
        self.flattening_f = 0.00334277318217481  # 
        self.semi_minor_axis_b = self.semi_minor_axis_a * (1 - self.flattening_f)  # 
        self.origin_scale_factor_ko = 1.0  # 
        self.origin_addition_value_x = 500000.0  # (N)
        self.origin_addition_value_y = 200000.0  # (E)
        self.origin_latitude = 38.0  # 
        self.origin_longitude = 127.0  # 
        self.first_eccentricty = (self.semi_minor_axis_a ** 2 - self.semi_minor_axis_b ** 2) / self.semi_minor_axis_a ** 2  # e^2
        self.second_eccentricty = (self.semi_minor_axis_a ** 2 - self.semi_minor_axis_b ** 2) / self.semi_minor_axis_b ** 2  # e'^2
        self.origin_latitude_radian = self.origin_latitude / 180 * self.pi  # 
        self.origin_longitude_radian = self.origin_longitude / 180 * self.pi  # 
        self.origin_meridian_mo = self.semi_minor_axis_a * ((1 - self.first_eccentricty / 4 - 3 * self.first_eccentricty ** 2 / 64 - 5 * self.first_eccentricty ** 3 / 256) * self.origin_latitude_radian - (3 * self.first_eccentricty / 8 + 3 * self.first_eccentricty ** 2 / 32 + 45 * self.first_eccentricty ** 3 / 1024) * math.sin(2 * self.origin_latitude_radian) + (15 * self.first_eccentricty ** 2 / 256 + 45 * self.first_eccentricty ** 3 / 1024) * math.sin(4 * self.origin_latitude_radian) - (35 * self.first_eccentricty ** 3 / 2072) * math.sin(6 * self.origin_latitude_radian))  # 
        self.origin_meridian_e1 = (1 - math.sqrt(1 - self.first_eccentricty)) / (1 + math.sqrt(1 - self.first_eccentricty))  # 
        self.correction_10405_seconds = 0.0  # 10.405 
        self.degrad = self.pi / 180.0
        self.raddeg = 180.0 / self.pi
        self.grid = 5.0  # [km]
        self.re = 6371.00877 / self.grid  # [km]
        self.slat1 = 30.0 * self.degrad  # [degree]
        self.slat2 = 60.0 * self.degrad  # [degree]
        self.olon = 126.0 * self.degrad  # [degree]
        self.olat = 38.0 * self.degrad  # [degree]
        self.xo = 42.0  # [ ]
        self.yo = 135.0  # [ ]
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(math.tan(self.pi * 0.25 + self.slat2 * 0.5) / math.tan(self.pi * 0.25 + self.slat1 * 0.5))
        self.sf = math.pow(math.tan(self.pi * 0.25 + self.slat1 * 0.5), self.sn) * math.cos(self.slat1) / self.sn
        self.ro = self.re * self.sf / math.pow(math.tan(self.pi * 0.25 + self.olat * 0.5), self.sn)

    def convert_to_plane_rect(self, latitude, longitude):
        phi = latitude / 180 * self.pi
        lamda = (longitude - self.correction_10405_seconds) / 180 * self.pi
        t = math.pow(math.tan(phi), 2)
        c = (self.first_eccentricty / (1 - self.first_eccentricty)) * math.pow(math.cos(phi), 2)
        a = (lamda - (self.origin_longitude / 180 * self.pi)) * math.cos(phi)
        n = self.semi_minor_axis_a / math.sqrt(1 - self.first_eccentricty * math.pow(math.sin(phi), 2))
        m = self.semi_minor_axis_a * ((1 - self.first_eccentricty / 4 - 3 * self.first_eccentricty ** 2 / 64 - 5 * self.first_eccentricty ** 3 / 256) * phi - (3 * self.first_eccentricty / 8 + 3 * self.first_eccentricty ** 2 / 32 + 45 * self.first_eccentricty ** 3 / 1024) * math.sin(2 * phi) + (15 * self.first_eccentricty ** 2 / 256 + 45 * self.first_eccentricty ** 3 / 1024) * math.sin(4 * phi) - 35 * self.first_eccentricty ** 3 / 3072 * math.sin(6 * phi))
        x = self.origin_addition_value_y + self.origin_scale_factor_ko * n * (a + math.pow(a, 3) / 6 * (1 - t + c) + math.pow(a, 5) / 120 * (5 - 18 * t + math.pow(t, 2) + 72 * c - 58 * self.second_eccentricty))
        y = self.origin_addition_value_x + self.origin_scale_factor_ko * (m - self.origin_meridian_mo + n * math.tan(phi) * (math.pow(a, 2) / 2 + math.pow(a, 4) / 24 * (5 - t + 9 * c + 4 * math.pow(c, 2)) + math.pow(a, 6) / 720 * (61 - 58 * t + math.pow(t, 2) + 600 * c - 330 * self.second_eccentricty)))
        return x, y

    def convert_to_latitude_longitude(self, tm_x, tm_y):
        m = self.origin_meridian_mo + ((tm_y - self.origin_addition_value_x) / self.origin_scale_factor_ko)
        mu1 = m / (self.semi_minor_axis_a * (1 - self.first_eccentricty / 4 - 3 * self.first_eccentricty ** 2 / 64 - 5 * self.first_eccentricty ** 3 / 256))
        phi1 = mu1 + (3 * self.origin_meridian_e1 / 2 - 27 * math.pow(self.origin_meridian_e1, 3) / 32) * math.sin(2 * mu1) + (21 * math.pow(self.origin_meridian_e1, 2) / 16 - 55 * math.pow(self.origin_meridian_e1, 4) / 32) * math.sin(4 * mu1) + (151 * math.pow(self.origin_meridian_e1, 3) / 96) * math.sin(6 * mu1) + (1097 * math.pow(self.origin_meridian_e1, 4) / 512) * math.sin(8 * mu1)
        r1 = (self.semi_minor_axis_a * (1 - self.first_eccentricty)) / math.pow((1 - self.first_eccentricty * math.pow(math.sin(phi1), 2)), (3 / 2))
        c1 = self.second_eccentricty * math.pow(math.cos(phi1), 2)
        t1 = math.pow(math.tan(phi1), 2)
        n1 = self.semi_minor_axis_a / math.sqrt(1 - self.first_eccentricty * math.pow(math.sin(phi1), 2))
        d = (tm_x - self.origin_addition_value_y) / (n1 * self.origin_scale_factor_ko)
        phi = (phi1 - (n1 * math.tan(phi1) / r1) * (math.pow(d, 2) / 2 - math.pow(d, 4) / 24 * (5 + 3 * t1 + 10 * c1 - 4 * math.pow(c1, 2) - 9 * self.second_eccentricty) + math.pow(d, 6) / 720 * (61 + 90 * t1 + 298 * c1 + 45 * math.pow(t1, 2) - 252 * self.second_eccentricty - 3 * math.pow(c1, 2)))) * 180 / self.pi
        lamda = self.origin_longitude + ((1 / math.cos(phi1)) * (d - (math.pow(d, 3) / 6) * (1 + 2 * t1 + c1) + (math.pow(d, 5) / 120) * (5 - 2 * c1 + 28 * t1 - 3 * math.pow(c1, 2) + 8 * self.second_eccentricty + 24 * math.pow(t1, 2)))) * 180 / self.pi + self.correction_10405_seconds
        return phi, lamda

    def convert_to_grid(self, latitude, longitude):
        ra = self.re * self.sf / math.pow(math.tan(self.pi * 0.25 + latitude * self.degrad * 0.5), self.sn)
        theta = longitude * self.degrad - self.olon
        if theta > self.pi:
            theta -= 2.0 * self.pi
        if theta < -self.pi:
            theta += 2.0 * self.pi
        theta *= self.sn
        x = ra * math.sin(theta) + self.xo
        y = self.ro - ra * math.cos(theta) + self.yo
        return int(x + 1.5), int(y + 1.5)

    def convert_to_latitude_longitude_grid(self, nx, ny):
        x = float(nx) - 1.0
        y = float(ny) - 1.0
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0:
            ra = -ra
        alat = 2.0 * math.atan(math.pow(self.re * self.sf / ra, 1.0 / self.sn)) - self.pi * 0.5
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
        return lat, lon

coordinates = Coordinates()
print(coordinates.convert_to_plane_rect(37.5665, 126.9779))
print(coordinates.convert_to_latitude_longitude(315350.0, 401500.0))
print(coordinates.convert_to_grid(37.5665, 126.9779))
print(coordinates.convert_to_latitude_longitude_grid(62, 125))