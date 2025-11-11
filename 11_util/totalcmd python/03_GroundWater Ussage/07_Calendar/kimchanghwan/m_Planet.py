import math
from dataclasses import dataclass

# --- Constants and Helpers ---
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi
C = 173.144632684657  # speed of light (AU/Day)


# Mocks for missing VB/DLL functions (Placeholder implementations)
def InvJDYear(julday: float) -> float:
    """MOCK: Estimates the year from a Julian Date. Needed for JDtoTDT."""
    # Simplified estimation for demonstration
    return 2000.0 + (julday - 2451545.0) / 365.25


def GetLBR(jd: float, ipla: int, is_heliocentric: bool) -> tuple[float, float, float]:
    """
    MOCK: Placeholder for the core ephemeris function (VSOP87/EPL2000).
    Returns heliocentric Longitude (l, degrees), Latitude (B, degrees), and Distance (R, AU).
    """
    if ipla == 3:  # Earth
        l = (jd - 2451545.0) * 0.9856 + 100.0
        B = 0.0
        R = 1.00001
    elif ipla == 11:  # Moon (Geocentric)
        l = (jd - 2451545.0) * 13.176 + 200.0
        B = 5.0 * math.sin(jd * DEG_TO_RAD)
        R = 0.00257
    else:  # Other planets
        l = (jd - 2451545.0) * 0.5 + 50.0 * ipla
        B = 0.1 * ipla
        R = 1.0 + 0.1 * ipla

    return l % 360, B, R


def Rev(angle: float) -> float:
    """Normalize an angle to the range [0, 360) degrees."""
    return angle % 360.0


def Arctan2d(y: float, x: float) -> float:
    """atan2 returning degrees."""
    return math.degrees(math.atan2(y, x))


def Arccosd(x: float) -> float:
    """acos returning degrees, with domain error handling."""
    if x > 1.0: x = 1.0
    if x < -1.0: x = -1.0
    return math.degrees(math.acos(x))


def Int2(X1: float, x2: float, Y1: float, Y2: float, P: float) -> float:
    """2-point linear interpolation (corresponds to VB's Int2)."""
    DX = x2 - X1
    dy = Y2 - Y1
    R = (P - X1) / DX
    return Y1 + R * dy


# --- Data Structure ---
@dataclass
class TPlanetData:
    """Data structure for DE404 (mocked by GetLBR)."""
    JD: float
    l: float
    B: float
    R: float
    ipla: int


# --- Global/Module-level variable equivalent ---
# In VB, oblecl is a module-level Dim. In Python, we pass it or define it at the module level
# if it's truly global, but since ecl() calculates it, we'll keep it locally scoped in PlanetPosB.

# --- Core Functions ---

def ecl(julday: float) -> float:
    """Calculate the obliquity of the ecliptic (황도 경사각) in degrees."""
    T = (julday - 2451545.0) / 3652500
    ecl2 = -249.67 + (-39.05 + (7.12 + (27.87 + (5.79 + 2.45 * T) * T) * T) * T) * T
    ecl_deg = 23.439291111 + (-4680.93 + (-1.55 + (1999.25 + (-51.38 + ecl2 * T) * T) * T) * T) * T / 3600
    return ecl_deg


def JDtoTDT(julday: float) -> float:
    """
    Calculate Terrestrial Dynamical Time (TDT) from Julian Date (JD/UT).
    This function implements a complex historical Delta T model.
    """
    y = int(InvJDYear(julday))
    T = 0.0
    dt = 0.0

    if y < 949:
        T = (y - 2000) / 100
        dt = (2715.6 + 573.36 * T + 46.5 * T * T) / 3600
    elif 949 <= y <= 1619:
        T = (y - 1850) / 100
        dt = (22.5 * T * T) / 3600
    elif y == 1620 or y == 1621:
        dt = 124 / 3600
    elif y == 1622 or y == 1623:
        dt = 115 / 3600
    elif y == 1624 or y == 1625:
        dt = 106 / 3600
    elif y == 1626 or y == 1627:
        dt = 98 / 3600
    elif y == 1628 or y == 1629:
        dt = 91 / 3600
    elif y == 1630 or y == 1631:
        dt = 85 / 3600
    elif y == 1632 or y == 1633:
        dt = 79 / 3600
    elif y == 1634 or y == 1635:
        dt = 74 / 3600
    elif y == 1636 or y == 1637:
        dt = 70 / 3600
    elif y == 1638 or y == 1639:
        dt = 65 / 3600
    elif 1640 <= y <= 1645:
        dt = 60 / 3600
    elif 1646 <= y <= 1653:
        dt = 50 / 3600
    elif 1654 <= y <= 1661:
        dt = 40 / 3600
    elif 1662 <= y <= 1671:
        dt = 30 / 3600
    elif 1672 <= y <= 1681:
        dt = 20 / 3600
    elif 1682 <= y <= 1691:
        dt = 10 / 3600
    elif 1692 <= y <= 1707:
        dt = 9 / 3600
    elif 1708 <= y <= 1717:
        dt = 10 / 3600
    elif 1718 <= y <= 1733:
        dt = 11 / 3600
    elif 1734 <= y <= 1743:
        dt = 12 / 3600
    elif 1744 <= y <= 1751:
        dt = 13 / 3600
    elif 1752 <= y <= 1757:
        dt = 14 / 3600
    elif 1758 <= y <= 1765:
        dt = 15 / 3600
    elif 1766 <= y <= 1775:
        dt = 16 / 3600
    elif 1776 <= y <= 1791:
        dt = 17 / 3600
    elif 1792 <= y <= 1795:
        dt = 16 / 3600
    elif 1796 <= y <= 1797:
        dt = 15 / 3600
    elif 1798 <= y <= 1799:
        dt = 14 / 3600
    elif 1800 <= y <= 1899:
        T = (y - 1900) / 100
        # The following lines implement a polynomial evaluation for dt based on T
        dt = 727058.63 + T * 123563.95
        dt = 2513807.78 + T * (1818961.41 + T * dt)
        dt = 1061660.75 + T * (2087298.89 + T * dt)
        dt = 56282.84 + T * (324011.78 + T * dt)
        dt = -2.5 + T * (228.95 + T * (5218.61 + T * dt))
        dt = dt / 3600
    elif 1900 <= y <= 1987:
        T = (y - 1900) / 100
        dt = -0.861938 + T * (0.677066 + T * -0.212591)
        dt = 0.025184 + T * (-0.181133 + T * (0.55304 + T * dt))
        dt = -0.00002 + T * (0.000297 + T * dt)
        dt = dt * 24
    elif 1988 <= y <= 1996:
        T = (y - 2000) / 100
        dt = (67 + 123.5 * T + 32.5 * T * T) / 3600
    elif y == 1997:
        dt = 62 / 3600
    elif 1998 <= y <= 1999:
        dt = 63 / 3600
    elif 2000 <= y <= 2001:
        dt = 64 / 3600
    elif 2002 <= y <= 2020:
        T = (y - 2000) / 100
        dt = (63 + 123.5 * T + 32.5 * T * T) / 3600
    elif y > 2020:
        T = (y - 1875.1) / 100
        dt = 45.39 * T * T / 3600
    else:
        dt = 0

    return dt / 24 + julday


def Plan404(Pla: TPlanetData) -> int:
    """
    Wrapper for GetLBR, adjusting index and converting to radians.
    ipla index: 1-Mercury, 2-Venus, 3-Earth... 9-Neptune, 10-Pluto, 11-Moon.
    """
    i = Pla.ipla

    # VB CByte(Pla.ipla) is tricky here. Assuming ipla is meant to be 1-based index (1-11)
    # The VB logic i=i-1, If i=10 Then i=9 means:
    # 1 -> 0 (Mercury)
    # ...
    # 9 -> 8 (Neptune)
    # 10 -> 9 (Pluto) -> **set to 9** (This is the VB code's handling of Pluto's index 10)
    # 11 -> 10 (Moon)

    # Correcting the index based on VB logic
    i_use = i - 1
    if i_use == 10:  # If original ipla was 11 (Moon), i_use is 10.
        i_use = 9  # The VB code's comment says 'If i=10 Then i=9'. This looks like a bug/convention for DE404 planet indexes where Pluto=9?
        # Replicating the VB code's behavior: 10 (Pluto) becomes 9. But 11 (Moon) also becomes 10.
        # Let's trust the logic written:
        # i = i - 1
        # If i = 10 Then i = 9
        # If original ipla=11 (Moon), i=10. This line makes Moon index 9.
        # If original ipla=10 (Pluto), i=9. This line does nothing.
        # This implies both Pluto and Moon use index 9 for GetLBR. This is highly non-standard.

    # Re-interpreting the VB logic to be safe:
    # 1-Mercury, 2-Venus, 3-Earth, 4-Mars, 5-Jupiter, 6-Saturn, 7-Uranus, 8-Neptune, 9-Pluto, 10-Sun, 11-Moon.
    # The VB code seems to use 1-based indices that map differently for DE404.

    # Let's strictly follow the VB code's math:
    i_internal = Pla.ipla
    i_internal = i_internal - 1
    if i_internal == 10:
        i_internal = 9
    Pla.ipla = i_internal

    l_deg, B_deg, R = GetLBR(Pla.JD, Pla.ipla, True)

    Pla.l = l_deg * DEG_TO_RAD
    Pla.B = B_deg * DEG_TO_RAD
    Pla.R = R

    # VB comment: If i <> 8 Then Plan404 = 1 Else Plan404 = 0 '명왕성은 계산 안함
    # i=8 refers to the *internal* index 8, which is 9-1=8 (Pluto).
    # Since we set ipla=9 (Pluto) to ipla=8 in the earlier logic:
    if i_internal == 8:  # If original ipla was 9 (Pluto), or 10 (Sun) if mapping is different. Assuming 9=Pluto.
        return 0  # Do not calculate Pluto
    else:
        return 1


def PlanetPosB(pIndex: int, julday: float, TZ: float, TimeAbbr: bool) -> tuple[float, float, float]:
    """
    Calculates geocentric Equatorial coordinates (RA, Dec) and Phase (PH) for a planet.
    Mimics the VB GoTo CorTimeAbbr: structure using a while loop.

    pIndex: Planet index (0=Sun, 8=Moon, others must be mapped).
    julday: Current Julian Day (UT).
    TZ: Time Zone correction (hours).
    TimeAbbr: Boolean flag for Light-Time Correction.

    Returns: (pRA [rad], pDE [rad], PH [0.0 - 1.0])
    """

    # Initialization
    i = pIndex
    tpla = TPlanetData(JD=0.0, l=0.0, B=0.0, R=0.0, ipla=0)
    CorTimeA = False

    # Light-time correction constant (AU/Day)
    c = C

    # Initial time calculation
    current_julday = julday  # Use a mutable copy for the loop

    # --- CorTimeAbbr Loop Equivalent ---
    while True:
        # Calculate TDT, Obliquity, and D based on current_julday
        TDT = JDtoTDT(current_julday - TZ / 24.0)
        oblecl = ecl(current_julday - TZ / 24.0) * DEG_TO_RAD
        # D is unused in the remaining VB snippet

        # 1. Get Earth's Heliocentric Coordinates (index 3)
        tpla.JD = TDT
        tpla.ipla = 3
        Plan404(tpla)
        SunLon = tpla.l
        SunLat = tpla.B
        SunDist = tpla.R

        # Earth's Heliocentric Rectangular Coordinates
        xe = SunDist * math.cos(SunLon) * math.cos(SunLat)
        ye = SunDist * math.sin(SunLon) * math.cos(SunLat)
        ze = SunDist * math.sin(SunLat)

        # 2. Get Moon's Geocentric Coordinates (index 11)
        tpla.ipla = 11
        Plan404(tpla)
        MoonLon = tpla.l
        MoonLat = tpla.B
        MoonDist = tpla.R

        # Moon's Geocentric Rectangular Coordinates
        DX = MoonDist * math.cos(MoonLon) * math.cos(MoonLat)
        dy = MoonDist * math.sin(MoonLon) * math.cos(MoonLat)
        dz = MoonDist * math.sin(MoonLat)

        # Moon's Heliocentric Rectangular Coordinates
        xm = xe + DX
        ym = ye + dy
        zm = ze + dz

        # Recalculate Earth's Heliocentric Spherical (Unused, but kept for 1:1)
        # The VB code has an error here, SunLat should be Arctan2d(ze, ...), but uses zg
        # We will keep the VB code as is for 1:1 translation, assuming zg is meant to be ze
        # SunLon_deg = Rev(Arctan2d(ye, xe))
        # SunLat_deg = Arctan2d(ze, math.sqrt(xe * xe + ye * ye))

        # --- CorTimeAbbr Label Start ---

        hDist = 0.0  # Heliocentric distance of the target planet
        eln = 0.0  # Heliocentric Longitude of the target planet (rad)
        elt = 0.0  # Heliocentric Latitude of the target planet (rad)

        if i == 0:  # Sun
            # The sun is at the center of the coordinate system, but its geocentric position is -Earth's heliocentric position
            hDist = 0.0
            eln, elt = 0.0, 0.0  # Sun's heliocentric coordinates are 0

            # Sun's Geocentric Rectangular (xh, yh, zh) from Earth's negative heliocentric (xe, ye, ze)
            xh = 0.0
            yh = 0.0
            zh = 0.0

            xg = xh - xe
            yg = yh - ye
            zg = zh - ze
            gDist = math.sqrt(xg * xg + yg * yg + zg * zg)

        elif i == 8:  # Moon
            # Moon's Geocentric Rectangular (xm - xe, ym - ye, zm - ze) is already calculated above as DX, dy, dz
            xg = xm - xe
            yg = ym - ye
            zg = zm - ze
            hDist = math.sqrt(xm * xm + ym * ym + zm * zm)  # Moon's Heliocentric distance
            gDist = math.sqrt(xg * xg + yg * yg + zg * zg)  # Moon's Geocentric distance

        else:  # Other Planets (Non-Sun, Non-Moon)
            # 1. Get Planet's Heliocentric Coordinates
            tpla.ipla = i
            Plan404(tpla)
            eln = tpla.l
            elt = tpla.B
            hDist = tpla.R

            # 2. Planet's Heliocentric Rectangular Coordinates
            xh = hDist * math.cos(eln) * math.cos(elt)
            yh = hDist * math.sin(eln) * math.cos(elt)
            zh = hDist * math.sin(elt)

            # 3. Planet's Geocentric Rectangular Coordinates
            xg = xh - xe
            yg = yh - ye
            zg = zh - ze
            gDist = math.sqrt(xg * xg + yg * yg + zg * zg)

        # Light-Time Correction Check (Only for non-Sun/Moon if TimeAbbr is True)
        if TimeAbbr and not CorTimeA and i not in (0, 8):
            Tc = gDist / c
            current_julday -= Tc
            CorTimeA = True
            continue  # Go back to the start of the while loop (CorTimeAbbr label)

        # If the code reaches here, correction is complete or not needed
        break

    # --- Final Geocentric Conversion (Applicable after correction loop exits) ---

    # Geocentric Ecliptic Spherical (glon, glat) in degrees
    glon_deg = Rev(Arctan2d(yg, xg))
    gLAT_deg = Arctan2d(zg, math.sqrt(xg * xg + yg * yg))

    # Geocentric Equatorial Rectangular (xe, ye, ze) - re-use variables
    xe_eq = xg
    ye_eq = yg * math.cos(oblecl) - zg * math.sin(oblecl)
    ze_eq = yg * math.sin(oblecl) + zg * math.cos(oblecl)

    # Geocentric Equatorial Spherical (RA, Dec) in radians
    pRA = Rev(Arctan2d(ye_eq, xe_eq)) * DEG_TO_RAD
    pDE = Arctan2d(ze_eq, math.sqrt(xe_eq * xe_eq + ye_eq * ye_eq)) * DEG_TO_RAD

    # --- Physical Characteristics (Phase) ---

    # Elongation (elon) in degrees
    # Arccosd((SunDist ^ 2 + gDist ^ 2 - hDist ^ 2) / (2 * SunDist * gDist))
    try:
        cos_elon = (SunDist ** 2 + gDist ** 2 - hDist ** 2) / (2 * SunDist * gDist)
    except ZeroDivisionError:
        cos_elon = 0  # Should not happen unless Earth/Planet distance is zero

    elon_deg = Arccosd(cos_elon)
    FV_deg = 0.0
    PH = 0.0

    if i == 0:  # Sun
        PH = 1.0

    elif i == 8:  # Moon
        # The VB code re-calculates elongation for the Moon here
        SunLon_deg = Rev(Arctan2d(ye, xe))
        glon_deg_rev = Rev(Arctan2d(yg, xg))

        # elon = Rev(Arccosd(Cosd((180 + SunLon) - glon) * Cosd(gLAT))) - Requires Cosd
        # Assuming Cosd(x) is math.cos(x * DEG_TO_RAD)

        # Convert SunLon_deg and glon_deg_rev to radians for the next calculation
        SunLon_rad = SunLon_deg * DEG_TO_RAD
        glon_rad = glon_deg_rev * DEG_TO_RAD
        gLAT_rad = gLAT_deg * DEG_TO_RAD

        # Using the VB logic as written (converted to Python degrees/radians):
        arg = math.cos((180.0 + SunLon_deg - glon_deg_rev) * DEG_TO_RAD) * math.cos(gLAT_rad)
        elon_deg = Rev(Arccosd(arg))

        FV_deg = 180.0 - elon_deg
        PH = (1.0 + math.cos(FV_deg * DEG_TO_RAD)) / 2.0
        PH = float(PH)  # Ensures it matches VB's CSng (single-precision float)

    elif i > 0:  # Other planets
        # FV: Phase angle (degrees)
        try:
            cos_FV = (gDist ** 2 + hDist ** 2 - SunDist ** 2) / (2 * hDist * gDist)
        except ZeroDivisionError:
            cos_FV = 0

        FV_deg = Arccosd(cos_FV)
        PH = (1.0 + math.cos(FV_deg * DEG_TO_RAD)) / 2.0
        PH = float(PH)

    return pRA, pDE, PH


# --- Example Usage (Demonstration of Mocks) ---
if __name__ == '__main__':
    # Test Data: 2000-01-01 12:00:00 UT (JD 2451545.0)
    TEST_JD = 2451545.0

    print(f"--- Test Case: JD {TEST_JD} ---")

    # 1. Test ecl (Obliquity)
    obliq_deg = ecl(TEST_JD)
    print(f"Obliquity (ecl): {obliq_deg:.6f} degrees")

    # 2. Test JDtoTDT (Delta T)
    tdt_jd = JDtoTDT(TEST_JD)
    delta_t_sec = (tdt_jd - TEST_JD) * 24.0 * 3600.0
    print(f"TDT JD: {tdt_jd:.6f}")
    print(f"Delta T (seconds): {delta_t_sec:.3f} seconds")

    # 3. Test PlanetPosB (Planet Position) - Using the mock ephemeris
    # Target: Sun (pIndex=0), No time correction
    ra, dec, phase = PlanetPosB(pIndex=0, julday=TEST_JD, TZ=0.0, TimeAbbr=False)
    print("\n--- SUN Position (Mock Ephemeris) ---")
    print(f"RA: {ra / DEG_TO_RAD:.4f} deg, Dec: {dec / DEG_TO_RAD:.4f} deg, Phase: {phase:.4f}")

    # Target: Moon (pIndex=8), With time correction
    ra_moon, dec_moon, phase_moon = PlanetPosB(pIndex=8, julday=TEST_JD, TZ=0.0, TimeAbbr=True)
    print("\n--- MOON Position (Mock Ephemeris, Time Correction ON) ---")
    print(f"RA: {ra_moon / DEG_TO_RAD:.4f} deg, Dec: {dec_moon / DEG_TO_RAD:.4f} deg, Phase: {phase_moon:.4f}")

    # Target: Mars (pIndex=4), With time correction (will trigger the GoTo loop)
    ra_mars, dec_mars, phase_mars = PlanetPosB(pIndex=4, julday=TEST_JD, TZ=0.0, TimeAbbr=True)
    print("\n--- MARS Position (Mock Ephemeris, Time Correction ON) ---")
    print(f"RA: {ra_mars / DEG_TO_RAD:.4f} deg, Dec: {dec_mars / DEG_TO_RAD:.4f} deg, Phase: {phase_mars:.4f}")
