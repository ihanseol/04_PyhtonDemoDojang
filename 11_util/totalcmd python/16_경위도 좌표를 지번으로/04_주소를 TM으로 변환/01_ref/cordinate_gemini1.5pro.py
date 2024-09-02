import math


class Coordinates:
    """
    This class provides methods for converting between different coordinate systems:
      - Latitude/Longitude
      - Transverse Mercator (TM)
      - Grid Coordinates (nx, ny)

    It uses formulas provided by the National Geographic Information Institute of Korea and the Korea Meteorological Administration.
    """

    def __init__(self):
        """Initializes the Coordinates class with constants for the different projections."""
        # Constants for World Geodetic System to Plane Rectangular Coordinate System conversion
        self.pi = math.pi
        self.semi_major_axis_a = 6377397.155  # Semi-major axis (a)
        self.flattening_f = 0.00334277318217481  # Flattening (f)
        self.semi_minor_axis_b = self.semi_major_axis_a * (
                1 - self.flattening_f
        )  # Semi-minor axis (b)
        self.origin_scale_factor_ko = 1.0  # Origin scale factor (ko)
        self.origin_addition_value_x = 500000.0  # Origin addition value X (N)
        self.origin_addition_value_y = 200000.0  # Origin addition value Y (E)
        self.origin_latitude = 38.0  # Origin latitude
        self.origin_longitude = 127.0  # Origin longitude
        self.first_eccentricity = (
                                          pow(self.semi_major_axis_a, 2) - pow(self.semi_minor_axis_b, 2)
                                  ) / pow(
            self.semi_major_axis_a, 2
        )  # First eccentricity (e^2)
        self.second_eccentricity = (
                                           pow(self.semi_major_axis_a, 2) - pow(self.semi_minor_axis_b, 2)
                                   ) / pow(
            self.semi_minor_axis_b, 2
        )  # Second eccentricity (e'^2)
        self.origin_latitude_radian = self.origin_latitude / 180 * self.pi
        self.origin_longitude_radian = self.origin_longitude / 180 * self.pi
        self.origin_meridian_mo = self.semi_major_axis_a * (
                (
                        1
                        - self.first_eccentricity / 4
                        - 3 * pow(self.first_eccentricity, 2) / 64
                        - 5 * pow(self.first_eccentricity, 3) / 256
                )
                * self.origin_latitude_radian
                - (
                        3 * self.first_eccentricity / 8
                        + 3 * pow(self.first_eccentricity, 2) / 32
                        + 45 * pow(self.first_eccentricity, 3) / 1024
                )
                * math.sin(2 * self.origin_latitude_radian)
                + (
                        15 * pow(self.first_eccentricity, 2) / 256
                        + 45 * pow(self.first_eccentricity, 3) / 1024
                )
                * math.sin(4 * self.origin_latitude_radian)
                - (35 * pow(self.first_eccentricity, 3) / 2072)
                * math.sin(6 * self.origin_latitude_radian)
        )
        self.origin_meridian_e1 = (1 - math.sqrt(1 - self.first_eccentricity)) / (
                1 + math.sqrt(1 - self.first_eccentricity)
        )
        self.correction_10405_seconds = 0.0  # 10.405 seconds correction

        # Constants for Village Forecast Point Coordinates and Latitude/Longitude Conversion
        self.degrad = self.pi / 180.0
        self.raddeg = 180.0 / self.pi
        self.grid = 5.0  # Earth radius to use [km]
        self.re = 6371.00877 / self.grid
        self.slat1 = 30.0 * self.degrad
        self.slat2 = 60.0 * self.degrad
        self.olon = 126.0 * self.degrad
        self.olat = 38.0 * self.degrad
        self.xo = 42.0  # X-coordinate of the reference point [grid distance]
        self.yo = 135.0  # Y-coordinate of the reference point [grid distance]
        self.sn = math.log(
            math.cos(self.slat1) / math.cos(self.slat2)
        ) / math.log(
            math.tan(self.pi * 0.25 + self.slat2 * 0.5)
            / math.tan(self.pi * 0.25 + self.slat1 * 0.5)
        )
        self.sf = pow(math.tan(self.pi * 0.25 + self.slat1 * 0.5), self.sn) * math.cos(
            self.slat1
        ) / self.sn
        self.ro = self.re * self.sf / pow(
            math.tan(self.pi * 0.25 + self.olat * 0.5), self.sn
        )

    def convert_to_plane_rect(self, latitude: float, longitude: float) -> tuple:
        """
        Converts latitude/longitude coordinates to TM (Transverse Mercator) coordinates.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.

        Returns:
            A tuple containing the TM X (N) and TM Y (E) coordinates.
        """
        phi = latitude / 180 * self.pi  # Φ, PHI
        lamda = (
                        longitude - self.correction_10405_seconds
                ) / 180 * self.pi  # λ, LAMDA
        t = pow(math.tan(phi), 2)  # T
        c = (
                    self.first_eccentricity / (1 - self.first_eccentricity)
            ) * pow(
            math.cos(phi), 2
        )  # C
        a = (lamda - (self.origin_longitude / 180 * self.pi)) * math.cos(
            phi
        )  # A
        n = self.semi_major_axis_a / math.sqrt(
            1 - self.first_eccentricity * pow(math.sin(phi), 2)
        )  # N
        m = self.semi_major_axis_a * (
                (
                        1
                        - self.first_eccentricity / 4
                        - 3 * pow(self.first_eccentricity, 2) / 64
                        - 5 * pow(self.first_eccentricity, 3) / 256
                )
                * phi
                - (
                        3 * self.first_eccentricity / 8
                        + 3 * pow(self.first_eccentricity, 2) / 32
                        + 45 * pow(self.first_eccentricity, 3) / 1024
                )
                * math.sin(2 * phi)
                + (
                        15 * pow(self.first_eccentricity, 2) / 256
                        + 45 * pow(self.first_eccentricity, 3) / 1024
                )
                * math.sin(4 * phi)
                - 35 * pow(self.first_eccentricity, 3) / 3072 * math.sin(6 * phi)
        )  # M
        x = self.origin_addition_value_y + self.origin_scale_factor_ko * n * (
                a
                + pow(a, 3) / 6 * (1 - t + c)
                + pow(a, 5)
                / 120
                * (5 - 18 * t + pow(t, 2) + 72 * c - 58 * self.second_eccentricity)
        )  # X, TM X(N)
        y = self.origin_addition_value_x + self.origin_scale_factor_ko * (
                m
                - self.origin_meridian_mo
                + n
                * math.tan(phi)
                * (
                        pow(a, 2) / 2
                        + pow(a, 4)
                        / 24
                        * (5 - t + 9 * c + 4 * pow(c, 2))
                        + pow(a, 6)
                        / 720
                        * (
                                61
                                - 58 * t
                                + pow(t, 2)
                                + 600 * c
                                - 330 * self.second_eccentricity
                        )
                )
        )  # Y, TM Y(E)
        return (x, y)

    def convert_to_latitude_longitude(self, tm_x: float, tm_y: float) -> tuple:
        """
        Converts TM (Transverse Mercator) coordinates to latitude/longitude coordinates.

        Args:
            tm_x: TM X (N) coordinate.
            tm_y: TM Y (E) coordinate.

        Returns:
            A tuple containing the latitude and longitude in degrees.
        """
        m = self.origin_meridian_mo + (
                (tm_y - self.origin_addition_value_x) / self.origin_scale_factor_ko
        )  # M
        mu1 = m / (
                self.semi_major_axis_a
                * (
                        1
                        - self.first_eccentricity / 4
                        - 3 * pow(self.first_eccentricity, 2) / 64
                        - 5 * pow(self.first_eccentricity, 3) / 256
                )
        )  # μ1, MU1
        phi1 = (
                mu1
                + (3 * self.origin_meridian_e1 / 2 - 27 * pow(self.origin_meridian_e1, 3) / 32)
                * math.sin(2 * mu1)
                + (
                        21 * pow(self.origin_meridian_e1, 2) / 16
                        - 55 * pow(self.origin_meridian_e1, 4) / 32
                )
                * math.sin(4 * mu1)
                + (151 * pow(self.origin_meridian_e1, 3) / 96) * math.sin(6 * mu1)
                + (1097 * pow(self.origin_meridian_e1, 4) / 512) * math.sin(8 * mu1)
        )  # Φ1, PHI1
        r1 = (self.semi_major_axis_a * (1 - self.first_eccentricity)) / (
            pow((1 - self.first_eccentricity * pow(math.sin(phi1), 2)), (3 / 2))
        )  # R1, radius of curvature of the meridian at latitude Φ1
        c1 = self.second_eccentricity * pow(math.cos(phi1), 2)  # C1
        t1 = pow(math.tan(phi1), 2)  # T1
        n1 = self.semi_major_axis_a / math.sqrt(
            1 - self.first_eccentricity * pow(math.sin(phi1), 2)
        )  # N1, radius of curvature of the prime vertical at latitude Φ1
        d = (
                (tm_x - self.origin_addition_value_y)
                / (n1 * self.origin_scale_factor_ko)
        )  # D
        phi = (
                      phi1
                      - (n1 * math.tan(phi1) / r1)
                      * (
                              pow(d, 2) / 2
                              - pow(d, 4)
                              / 24
                              * (
                                      5
                                      + 3 * t1
                                      + 10 * c1
                                      - 4 * pow(c1, 2)
                                      - 9 * self.second_eccentricity
                              )
                              + pow(d, 6)
                              / 720
                              * (
                                      61
                                      + 90 * t1
                                      + 298 * c1
                                      + 45 * pow(t1, 2)
                                      - 252 * self.second_eccentricity
                                      - 3 * pow(c1, 2)
                              )
                      )
              ) * 180 / self.pi  # Φ, PHI, Latitude
        lamda = (
                self.origin_longitude
                + (
                        (1 / math.cos(phi1))
                        * (
                                d
                                - (pow(d, 3) / 6) * (1 + 2 * t1 + c1)
                                + (pow(d, 5) / 120)
                                * (5 - 2 * c1 + 28 * t1 - 3 * pow(c1, 2) + 8 * self.second_eccentricity + 24 * pow(t1,
                                                                                                                   2))
                        )
                )
                * 180
                / self.pi
                + self.correction_10405_seconds
        )  # λ, LAMDA, Longitude
        return (phi, lamda)

    def convert_to_grid(self, latitude: float, longitude: float) -> tuple:
        """
        Converts latitude/longitude coordinates to grid (nx, ny) coordinates.

        Args:
            latitude: Latitude in degrees.
            longitude: Longitude in degrees.

        Returns:
            A tuple containing the grid X (nx) and grid Y (ny) coordinates.
        """
        ra = self.re * self.sf / pow(
            math.tan(self.pi * 0.25 + latitude * self.degrad * 0.5), self.sn
        )
        theta = longitude * self.degrad - self.olon
        if theta > self.pi:
            theta -= 2.0 * self.pi
        if theta < -self.pi:
            theta += 2.0 * self.pi
        theta *= self.sn
        x = ra * math.sin(theta) + self.xo
        y = self.ro - ra * math.cos(theta) + self.yo
        return (int(x + 1.5), int(y + 1.5))

    def convert_to_latitude_longitude_from_grid(self, nx: int, ny: int) -> tuple:
        """
        Converts grid (nx, ny) coordinates to latitude/longitude coordinates.

        Args:
            nx: Grid X (nx) coordinate.
            ny: Grid Y (ny) coordinate.

        Returns:
            A tuple containing the latitude and longitude in degrees.
        """
        x = float(nx) - 1.0
        y = float(ny) - 1.0
        xn = x - self.xo
        yn = self.ro - y + self.yo
        ra = math.sqrt(xn * xn + yn * yn)
        if self.sn < 0.0:
            ra = -ra
        alat = 2.0 * math.atan(pow(self.re * self.sf / ra, 1.0 / self.sn)) - self.pi * 0.5
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
