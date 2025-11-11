import math
from typing import Dict, Any, Tuple

# --- Constants ---
HOR_SUN = 4
HOR_MOON = 5
SUN = 0
MOON = 8


# --- Type Simulation (Using classes or dicts) ---

class tRSTime:
    """VBA Type tRSTime"""

    def __init__(self):
        self.JD = 0.0  # 날짜 (Julian Day)
        self.ObjAlt = 0.0  # 목표 고도 (Target Altitude)
        self.Longitude = 0.0  # 경도
        self.Latitude = 0.0  # 위도
        self.TZone = 0.0  # 시간권 (Time Zone, hours offset)
        self.RiseTime = 0.0  # 뜨는 시각 (JD)
        self.SetTime = 0.0  # 지는 시각 (JD)
        self.bRise = False  # 뜨는 시간 있는지
        self.bSet = False  # 지는 시간 있는지


class ObjPos:
    """VBA Type ObjPos: Object Position at 00h, 12h, 24h UT"""

    def __init__(self):
        self.RA1 = 0.0  # Right Ascension at 00h UT
        self.RA2 = 0.0  # Right Ascension at 12h UT
        self.RA3 = 0.0  # Right Ascension at 24h UT
        self.DE1 = 0.0  # Declination at 00h UT
        self.DE2 = 0.0  # Declination at 12h UT
        self.DE3 = 0.0  # Declination at 24h UT


# --- Assumed External Dependencies (Placeholders) ---

def get_jd0(date_jd: float) -> float:
    """Placeholder for GetJD0 (JD at nearest noon/0.5)"""
    # Assuming the implementation from previous context
    if date_jd - math.floor(date_jd) >= 0.5:
        return math.floor(date_jd) + 0.5
    else:
        return math.floor(date_jd) - 0.5


def make_time_string3(julday: float) -> str:
    """Placeholder for MakeTimeString3 (Formats time as HH:MM)"""
    # Requires InvJD to convert JD back to Y/M/D/H/M/S
    return "HH:MM"


def rev(angle: float) -> float:
    """Placeholder for Rev (Normalizes angle to 0-360 degrees)"""
    return angle % 360.0


def planet_pos_b(pl: int, jd: float, tz: float, topo: bool) -> Tuple[float, float, float]:
    """
    Placeholder for PlanetPosB (Calculates RA, DE, and Magnitude).

    Args:
        pl: Object ID (SUN=0, MOON=8)
        jd: Julian Day
        tz: Time Zone
        topo: Topocentric calculation flag

    Returns: (RA, DE, Magnitude)
    """
    # *** This must be replaced with accurate astronomical calculation ***
    return 0.0, 0.0, 0.0


def inter3_sph(ra1, de1, ra2, de2, ra3, de3, t_factor, ra_out, de_out):
    """
    Placeholder for Inter3Sph (3-point interpolation for spherical coordinates).

    VBA passes RA/DE by reference; Python returns the interpolated values.

    Args: RA/DE at 3 points, t_factor (interpolation point -1.0 to 1.0)
    Returns: (Interpolated RA, Interpolated DE)
    """
    # *** This must be replaced with a proper interpolation function (e.g., Lagrange) ***
    return ra2, de2


def equ_to_alt_az(ra: float, de: float, lha: float, lat: float) -> Tuple[float, float]:
    """
    Placeholder for EquToAltAz (Converts Equatorial to Horizon coordinates).

    Args: RA, DE, Local Hour Angle (LHA), Latitude
    Returns: (Azimuth, Altitude)
    """
    # *** This must be replaced with a proper coordinate transformation ***
    return 0.0, 0.0


def int2(alt1: float, alt2: float, t1: float, t2: float, target_alt: float) -> float:
    """
    Placeholder for Int2 (Linear interpolation to find time (T) when target_alt is reached).

    Args: Altitude at T1, Altitude at T2, Time T1, Time T2, Target Altitude
    Returns: Interpolated Time (JD)
    """
    # Simple linear interpolation: T = T1 + (T2 - T1) * (Target - Alt1) / (Alt2 - Alt1)
    if alt2 == alt1:
        return t1  # Avoid division by zero, return starting time
    return t1 + (t2 - t1) * (target_alt - alt1) / (alt2 - alt1)


# --- Sub/Function Implementations ---

def get_rise_set_by_pos(data_set: tRSTime, pos_data: ObjPos, prec: int):
    """
    VBA Sub GetRiseSetByPos를 1:1 변환.
    3차 보간된 위치 데이터를 사용하여 출몰 시각을 분할 검색으로 찾습니다.
    (VBA passes DataSet by reference; Python modifies the passed object)
    """

    # 1. 초기 설정 및 Local Sidereal Time (LST) 계산

    # JD at 00:00 UT on the target date (ut0)
    ut_now = get_jd0(data_set.JD) - data_set.TZone / 24.0
    ut0 = get_jd0(ut_now)

    # Julian Century from J2000.0 (JD 2451545.0)
    t1 = (ut0 - 2451545.0) / 36525.0

    # Greenwich Sidereal Time (GST) at 00h UT (temp: degrees)
    temp = rev(100.46061837 + 36000.770053608 * t1 + 0.000387933 * t1 ** 2 - t1 ** 3 / 38710000.0)
    # GST at current time (ut_now) + Longitude = Local Sidereal Time (LST) (temp: degrees)
    temp = rev(temp + data_set.Longitude + (ut_now - ut0) * 360.985647366)

    LO = data_set.Longitude
    La = data_set.Latitude
    oAlt = data_set.ObjAlt
    jd0 = get_jd0(data_set.JD)

    DE1, DE2, DE3 = pos_data.DE1, pos_data.DE2, pos_data.DE3
    RA1, RA2, RA3 = pos_data.RA1, pos_data.RA2, pos_data.RA3

    # 2. 고도(Altitude) 및 방위각(Azimuth) 계산

    N = 1440.0 / float(prec)  # Number of intervals (1440 mins in a day) / PREC
    N2 = N / 2.0
    dt = 1.0 / N  # Time step in days

    # Arrays for Altitude, Azimuth, and Time
    ALT = [0.0] * (int(N) + 1)
    AZ = [0.0] * (int(N) + 1)
    T = [0.0] * (int(N) + 1)

    for i in range(int(N) + 1):
        T[i] = jd0 + i * dt

        # 3-point interpolation to find RA/DE at time T(i)
        # i: 0 to N. (i - N2) / N2 maps to -1.0 to 1.0 for interpolation
        # RA, DE are modified by reference in VBA, returned in Python
        RA, de = inter3_sph(RA1, DE1, RA2, DE2, RA3, DE3, (i - N2) / N2, 0.0, 0.0)

        # Current LST in degrees, converted to Hour Angle ( / 15 )
        # 360.985647366 is the daily change in sidereal time
        LHA_deg = (temp + i * dt * 360.985647366)
        LHA_hours = LHA_deg / 15.0

        # Convert Equatorial (RA, DE) to Horizon (AZ, ALT)
        AZ[i], ALT[i] = equ_to_alt_az(RA, de, LHA_hours, La)

    # 3. 출몰 시각 찾기 (Interpolation Search)

    br, bs = False, False
    R, S = 0.0, 0.0

    for i in range(int(N)):
        # Rise: Altitude is below target and rising (crosses oAlt from below)
        if ALT[i] <= oAlt and oAlt <= ALT[i + 1]:
            br = True
            # Linear interpolation to find the exact Rise Time (R)
            R = int2(ALT[i], ALT[i + 1], T[i], T[i + 1], oAlt)

        # Set: Altitude is above target and setting (crosses oAlt from above)
        if ALT[i] >= oAlt and oAlt >= ALT[i + 1]:
            bs = True
            # Linear interpolation to find the exact Set Time (S)
            S = int2(ALT[i], ALT[i + 1], T[i], T[i + 1], oAlt)

    # 4. 결과 저장
    data_set.RiseTime = R
    data_set.SetTime = S
    data_set.bRise = br
    data_set.bSet = bs


def rs_time(longi: float, lati: float, jul: float, tz: float, t: int, pl: int, prec: int) -> str:
    """
    VBA Function RSTime을 1:1 변환.
    관측지, 날짜, 천체를 입력받아 출몰 시각 문자열을 반환합니다.
    """

    P = ObjPos()
    D = tRSTime()
    oH = 0.0
    M = [0.0] * 3  # Placeholder for Magnitude/Phase

    # 1. 목표 고도 (ObjAlt) 설정
    if t == HOR_SUN:
        oH = -0.8333  # Sun's geometric altitude at true rise/set
    elif t == HOR_MOON:
        oH = 0.125  # Moon's altitude at true rise/set (smaller correction)
    else:
        # Handle other types if necessary
        return "--:--/--:--"

    # 2. 관측 데이터 설정
    D.Longitude = longi
    D.Latitude = lati
    D.ObjAlt = oH
    D.JD = jul
    D.TZone = tz

    # 3. 날짜 및 천체 위치 (00h, 12h, 24h UT) 얻기
    jd0 = get_jd0(D.JD)

    # Get positions at 00h UT, 12h UT, 24h UT for 3-point interpolation
    P.RA1, P.DE1, M[0] = planet_pos_b(pl, jd0, D.TZone, True)
    P.RA2, P.DE2, M[1] = planet_pos_b(pl, jd0 + 0.5, D.TZone, True)
    P.RA3, P.DE3, M[2] = planet_pos_b(pl, jd0 + 1.0, D.TZone, True)

    # 4. 출몰 시각 계산
    get_rise_set_by_pos(D, P, prec)

    # 5. 출력 문자열 생성
    RSTR = ""

    # Rise Time
    if D.bRise:
        RSTR += make_time_string3(D.RiseTime)
    else:
        RSTR += "--:--"

    RSTR += "/"

    # Set Time
    if D.bSet:
        RSTR += make_time_string3(D.SetTime)
    else:
        RSTR += "--:--"

    # 6. 달의 위상 정보 추가 (MOON only)
    if pl == MOON:
        # Get Moon's magnitude/phase at TZ (e.g., KST 12:00)
        # Note: The VBA code reuses P.RA1, P.DE1 for this point,
        # but only uses the returned magnitude M[1].
        # The JD used is jd0 + TZ / 24.0 (UT time equivalent of local noon)
        _, _, phase_val = planet_pos_b(pl, jd0 + D.TZone / 24.0, D.TZone, True)

        # Round(M(1) * 100) -> Round(phase_val * 100)
        phase_percent = int(round(phase_val * 100))
        RSTR += f"({phase_percent}%)"

    return RSTR
