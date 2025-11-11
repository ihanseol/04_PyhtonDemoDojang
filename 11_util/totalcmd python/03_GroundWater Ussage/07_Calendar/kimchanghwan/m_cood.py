import math
from typing import Tuple


# ----------------------------------------------------
# 1. 외부/보조 함수 정의 (VB 코드에 없지만 필요함)
# ----------------------------------------------------

# Python의 math 모듈은 라디안(radian)을 사용하므로, 도(degree) 함수를 정의합니다.
def Cosd(angle_deg: float) -> float:
    """코사인 (인수: 도)"""
    return math.cos(math.radians(angle_deg))


def Sind(angle_deg: float) -> float:
    """사인 (인수: 도)"""
    return math.sin(math.radians(angle_deg))


def Arccosd(x: float) -> float:
    """아크 코사인 (반환: 도)"""
    # math.acos의 입력은 -1.0 ~ 1.0 범위여야 합니다.
    x = max(-1.0, min(1.0, x))
    return math.degrees(math.acos(x))


def Arcsind(x: float) -> float:
    """아크 사인 (반환: 도)"""
    # math.asin의 입력은 -1.0 ~ 1.0 범위여야 합니다.
    x = max(-1.0, min(1.0, x))
    return math.degrees(math.asin(x))


def Arctan2d(y: float, x: float) -> float:
    """아크탄젠트 2 (반환: 도)"""
    return math.degrees(math.atan2(y, x))


def Rev(angle: float) -> float:
    """각도를 0 ~ 360도 범위로 정규화 (VB 코드에서 사용됨)"""
    return angle % 360


# VB 코드에 정의되지 않은 RotZ, RotY의 뼈대 (3D 회전 함수 가정)
def RotZ(X: float, y: float, Z: float, angle_deg: float) -> Tuple[float, float, float]:
    """Z축 회전 (X, y, Z를 참조로 업데이트해야 하지만, Python에서는 반환)"""
    # 실제 VB 코드에서는 X, y, Z가 인수로 전달되어 내부에서 값이 변경됩니다.
    # Python에서는 변경된 값을 튜플로 반환하도록 가정합니다.
    # 이 함수가 EquToAltAz 내부에서 호출될 때, X, y, Z가 업데이트되어야 합니다.
    # 여기서는 VB 코드의 행렬 변환 로직을 정확히 알 수 없으므로, 뼈대만 만듭니다.

    # 예시:
    # angle_rad = math.radians(angle_deg)
    # X_new = X * math.cos(angle_rad) - y * math.sin(angle_rad)
    # y_new = X * math.sin(angle_rad) + y * math.cos(angle_rad)
    # Z_new = Z
    # return X_new, y_new, Z_new
    return X, y, Z  # 뼈대 반환


def RotY(X: float, y: float, Z: float, angle_deg: float) -> Tuple[float, float, float]:
    """Y축 회전 (X, y, Z를 참조로 업데이트해야 하지만, Python에서는 반환)"""
    return X, y, Z  # 뼈대 반환


# ----------------------------------------------------
# 2. VB 함수 -> Python 함수 변환
# ----------------------------------------------------

def AngDistLon(RA1: float, RA2: float) -> float:
    """
    경도 사이의 각거리 계산 (VB: AngDistLon)

    :param RA1: 첫 번째 경도 (도)
    :param RA2: 두 번째 경도 (도)
    :return: 두 경도 사이의 각거리 (도)
    """
    if RA1 == RA2:
        return 0.0
    else:
        # VB: AngDistLon = Arccosd(Cosd(RA1 - RA2))
        return Arccosd(Cosd(RA1 - RA2))


def EquToAltAz(RA: float, DEC: float, LST: float, Latitude: float) -> Tuple[float, float]:
    """
    적도 좌표 (RA, DEC)를 지평 좌표 (Alt, Az)로 변환 (VB: EquToAltAz)

    :param RA: 적경 (도)
    :param DEC: 적위 (도)
    :param LST: 지방 항성시 (시)
    :param Latitude: 관측자 위도 (도)
    :return: (azimuth_deg, altitude_deg) 튜플
    """
    X: float
    y: float
    Z: float

    # 1. 적도 좌표를 직교 좌표 (X, y, Z)로 변환 (적경, 적위)
    X = Cosd(RA) * Cosd(DEC)
    y = Sind(RA) * Cosd(DEC)
    Z = Sind(DEC)

    # 2. 시각 (Hour Angle, HA) 회전 및 좌표 변환
    # LST * 15는 지방 항성시(시)를 도(degree)로 변환한 시각입니다.
    # VB: RotZ X, y, Z, LST * 15 + 180
    X, y, Z = RotZ(X, y, Z, LST * 15 + 180)

    # 3. 위도 회전
    # VB: RotY X, y, Z, Latitude
    X, y, Z = RotY(X, y, Z, Latitude)

    # 4. 지평 좌표 (Alt, Az) 계산

    # VB: az = Rev(-Arctan2d(y, Z))
    az: float = Rev(-Arctan2d(y, Z))

    # VB: ALT = Arcsind(-X)
    ALT: float = Arcsind(-X)

    return az, ALT


def Nutation(JDE: float) -> Tuple[float, float]:
    """
    황경 및 황축 경사의 장동(Nutation) 계산 (VB: Nutation)

    :param JDE: 에페머리스 줄리앙 일 (Julian Ephemeris Day)
    :return: (dPsi_arcsec, dEps_arcsec) 튜플 (단위: 초)
    """
    # 출력 변수 (VB의 Pass-by-Reference를 대체)
    dPsi: float
    dEps: float

    # VB 코드에서 사용된 변수
    # eps0: Double (사용되지 않음)
    OM: float
    T: float
    L1: float
    L2: float
    T2: float

    # 1. 시대 T (Julian Century from J2000.0) 계산
    T = (JDE - 2451545) / 36525
    T2 = T * T

    # 2. 필수 인자 계산 (도)

    # L1: 태양의 평균 황경
    # VB: L1 = Rev(280.466457 + 36000.7698278 * T + 0.00030322 * T2 + 0.00000002 * T2 * T)
    L1 = Rev(280.466457 + 36000.7698278 * T + 0.00030322 * T2 + 0.00000002 * T2 * T)

    # L2: 달의 평균 황경
    # VB: L2 = Rev(218.3164477 + 481267.88123421 * T - 0.0015786 * T2 + T2 * T / 538841 - T2 * T2 / 65194000)
    L2 = Rev(218.3164477 + 481267.88123421 * T - 0.0015786 * T2 + T2 * T / 538841 - (T2 * T2) / 65194000)

    # OM: 달의 승교점 경도 (Long. of ascending node of the Moon's mean orbit)
    # VB: OM = Rev(125.04452 - 1934.136261 * T + 0.0020708 * T2 + (T2 * T) / 450000)
    OM = Rev(125.04452 - 1934.136261 * T + 0.0020708 * T2 + (T2 * T) / 450000)

    # 3. 장동 계산 (단위: 초, IAU 1980 모델의 주요 항)

    # dPsi: 황경의 장동 (Longitudinal nutation)
    # VB: dPsi = -17.2 * Sind(OM) - 1.32 * Sind(2 * L1) - 0.23 * Sind(2 * L2) + 0.21 * Sind(2 * OM)
    dPsi = (-17.2 * Sind(OM) - 1.32 * Sind(2 * L1) - 0.23 * Sind(2 * L2) + 0.21 * Sind(2 * OM))

    # dEps: 황도 경사의 장동 (Obliquity nutation)
    # VB: dEps = 9.2 * Cosd(OM) + 0.57 * Cosd(2 * L1) + 0.1 * Cosd(2 * L2) - 0.09 * Cosd(2 * OM)
    dEps = (9.2 * Cosd(OM) + 0.57 * Cosd(2 * L1) + 0.1 * Cosd(2 * L2) - 0.09 * Cosd(2 * OM))

    return dPsi, dEps
