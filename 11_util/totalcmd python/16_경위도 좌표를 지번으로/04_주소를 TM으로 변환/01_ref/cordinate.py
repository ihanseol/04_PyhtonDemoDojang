import math

class Coordinates:
    def __init__(self):
        # Constants and initial calculations
        self.pi = math.pi
        self.semi_minor_axis_a = 6377397.155  # 장반경a
        self.flattening_f = 0.00334277318217481  # 편평률f
        self.semi_minor_axis_b = self.semi_minor_axis_a * (1 - self.flattening_f)  # 단반경b
        self.origin_scale_factor_ko = 1.0  # 원점축척계수ko
        self.origin_addition_value_x = 500000.0  # 원점가산값X(N)
        self.origin_addition_value_y = 200000.0  # 원점가산값Y(E)
        self.origin_latitude = 38.0  # 원점위도
        self.origin_longitude = 127.0  # 원점경도
        self.first_eccentricity = (self.semi_minor_axis_a ** 2 - self.semi_minor_axis_b ** 2) / self.semi_minor_axis_a ** 2  # 제1이심률e^2
        self.second_eccentricity = (self.semi_minor_axis_a ** 2 - self.semi_minor_axis_b ** 2) / self.semi_minor_axis_b ** 2  # 제2이심률e'^2
        self.origin_latitude_radian = self.origin_latitude / 180 * self.pi  # 원점위도 라디안
        self.origin_longitude_radian = self.origin_longitude / 180 * self.pi  # 원점경도 라디안
        self.origin_meridian_mo = self.semi_minor_axis_a * (
            (1 - self.first_eccentricity / 4 - 3 * self.first_eccentricity ** 2 / 64 - 5 * self.first_eccentricity ** 3 / 256) * self.origin_latitude_radian - 
            (3 * self.first_eccentricity / 8 + 3 * self.first_eccentricity ** 2 / 32 + 45 * self.first_eccentricity ** 3 / 1024) * math.sin(2 * self.origin_latitude_radian) + 
            (15 * self.first_eccentricity ** 2 / 256 + 45 * self.first_eccentricity ** 3 / 1024) * math.sin(4 * self.origin_latitude_radian) - 
            (35 * self.first_eccentricity ** 3 / 2072) * math.sin(6 * self.origin_latitude_radian)
        )
        self.origin_meridian_e1 = (1 - math.sqrt(1 - self.first_eccentricity)) / (1 + math.sqrt(1 - self.first_eccentricity))
        self.correction_10405_seconds = 0.0  # 10.405초 보정
        self.degrad = self.pi / 180.0
        self.raddeg = 180.0 / self.pi
        self.grid = 5.0  # 사용할 지구반경 [km]
        self.re = 6371.00877 / self.grid  # 사용할 지구반경 [km]
        self.slat1 = 30.0 * self.degrad  # 표준위도 [degree]
        self.slat2 = 60.0 * self.degrad  # 표준위도 [degree]
        self.olon = 126.0 * self.degrad  # 기준점의 경도 [degree]
        self.olat = 38.0 * self.degrad  # 기준점의 위도 [degree]
        self.xo = 42.0  # 기준점의 X좌표 [격자거리]
        self.yo = 135.0  # 기준점의 Y좌표 [격자거리]
        self.sn = math.log(math.cos(self.slat1) / math.cos(self.slat2)) / math.log(math.tan(self.pi * 0.25 + self.slat2 * 0.5) / math.tan(self.pi * 0.25 + self.slat1 * 0.5))
        self.sf = (math.tan(self.pi * 0.25 + self.slat1 * 0.5) ** self.sn) * math.cos(self.slat1) / self.sn
        self.ro = self.re * self.sf / (math.tan(self.pi * 0.25 + self.olat * 0.5) ** self.sn)
    
    def convert_to_plane_rect(self, latitude, longitude):
        phi = latitude / 180 * self.pi
        lamda = (longitude - self.correction_10405_seconds) / 180 * self.pi
        t = math.tan(phi) ** 2
        c = (self.first_eccentricity / (1 - self.first_eccentricity)) * math.cos(phi) ** 2
        a = (lamda - (self.origin_longitude / 180 * self.pi)) * math.cos(phi)
        n = self.semi_minor_axis_a / math.sqrt(1 - self.first_eccentricity * math.sin(phi) ** 2)
        m = self.semi_minor_axis_a * (
            (1 - self.first_eccentricity / 4 - 3 * self.first_eccentricity ** 2 / 64 - 5 * self.first_eccentricity ** 3 / 256) * phi - 
            (3 * self.first_eccentricity / 8 + 3 * self.first_eccentricity ** 2 / 32 + 45 * self.first_eccentricity ** 3 / 1024) * math.sin(2 * phi) + 
            (15 * self.first_eccentricity ** 2 / 256 + 45 * self.first_eccentricity ** 3 / 1024) * math.sin(4 * phi) - 
            35 * self.first_eccentricity ** 3 / 3072 * math.sin(6 * phi)
        )
        x = self.origin_addition_value_y + self.origin_scale_factor_ko * n * (a + (a ** 3) / 6 * (1 - t + c) + (a ** 5) / 120 * (5 - 18 * t + t ** 2 + 72 * c - 58 * self.second_eccentricity))
        y = self.origin_addition_value_x + self.origin_scale_factor_ko * (m - self.origin_meridian_mo + n * math.tan(phi) * ((a ** 2) / 2 + (a ** 4) / 24 * (5 - t + 9 * c + 4 * c ** 2) + (a ** 6) / 720 * (61 - 58 * t + t ** 2 + 600 * c - 330 * self.second_eccentricity)))
        return (x, y)
    
    def convert_to_latitude_longitude(self, tm_x, tm_y):
        m = self.origin_meridian_mo + ((tm_y - self.origin_addition_value_x) / self.origin_scale_factor_ko)
        mu1 = m / (self.semi_minor_axis_a * (1 - self.first_eccentricity / 4 - 3 * self.first_eccentricity ** 2 / 64 - 5 * self.first_eccentricity ** 3 / 256))
        phi1 = mu1 + (3 * self.origin_meridian_e1 / 2 - 27 * self.origin_meridian_e1 ** 3 / 32) * math.sin(2 * mu1) + (21 * self.origin_meridian_e1 ** 2 / 16 - 55 * self.origin_meridian_e1 ** 4 / 32) * math.sin(4 * mu1) + (151 * self.origin_meridian_e1 ** 3 / 96) * math.sin(6 * mu1) + (1097 * self.origin_meridian_e1 ** 4 / 512) * math.sin(8 * mu1)
        r1 = (self.semi_minor_axis_a * (1 - self.first_eccentricity)) / ((1 - self.first_eccentricity * math.sin(phi1) ** 2) ** (3 / 2))
        c1 = self.second_eccentricity * math.cos(phi1) ** 2
        t1 = math.tan(phi1) ** 2
        n1 = self.semi_minor_axis_a / math.sqrt(1 - self.first_eccentricity * math.sin(phi1) ** 2)
        d = (tm_x - self.origin_addition_value_y) / (n1 * self.origin_scale_factor_ko)
        phi = (phi1 - (n1 * math.tan(phi1) / r1) * (d ** 2 / 2 - d ** 4 / 24 * (5 + 3 * t1 + 10 * c1 - 4 * c1 ** 2 - 9 * self.second_eccentricity) + d ** 6 / 720 * (61 + 90 * t1 + 298 * c1 + 45 * t1 ** 2 - 252 * self.second_eccentricity - 3 * c1 ** 2))) * 180 / self.pi
        lamda = self.origin_longitude + (d - d ** 3 / 6 * (1 + 2 * t1 + c1) + d ** 5 / 120 * (5 - 2 * c1 + 28 * t1 - 3 * c1 ** 2 + 8 * self.second_eccentricity + 24 * t1 ** 2)) / math.cos(phi1) * 180 / self.pi
        return (phi, lamda)

    def convert_to_TM(self, v1, v2):
        PI = 3.14159265358979
        slat1 = 30.0 * PI / 180.0
        slat2 = 60.0 * PI / 180.0
        olon = 126.0 * PI / 180.0
        olat = 38.0 * PI / 180.0
        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = (sf ** sn * math.cos(slat1)) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = self.re * sf / (ro ** sn)
        rs = v1 * self.degrad
        ra = math.tan(PI * 0.25 + rs * 0.5)
        ra = self.re * self.sf / (ra ** sn)
        theta = v2 * self.degrad - olon
        if theta > PI:
            theta -= 2.0 * PI
        if theta < -PI:
            theta += 2.0 * PI
        theta *= sn
        x = ra * math.sin(theta) + self.xo
        y = ro - ra * math.cos(theta) + self.yo
        return (x, y)
