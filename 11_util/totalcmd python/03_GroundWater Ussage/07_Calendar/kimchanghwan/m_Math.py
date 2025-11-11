import math

# --- 상수 ---
# Python의 math 모듈에서 math.pi를 사용합니다.
pi: float = math.pi
hpi: float = pi / 2.0  # pi / 2
RadtoDeg: float = 180.0 / pi
DegtoRad: float = pi / 180.0


# --- 삼각 함수 ---

def Arcsin(X: float) -> float:
    """
    라디안 단위로 역사인(Arcsin)을 계산합니다. (VBA Arcsin 변환)
    Python의 math.asin과 동일합니다.
    """
    # 원본: Arcsin = Atn(X / math.sqrt(1 - X * X))
    return math.asin(X)


def Arccos(X: float) -> float:
    """
    라디안 단위로 역코사인(Arccos)을 계산합니다. (VBA Arccos 변환)
    Python의 math.acos와 동일합니다.
    """
    # Python의 math.acos()는 입력 값 범위를 자동으로 처리합니다.
    return math.acos(X)


def Sind(X: float) -> float:
    """
    도(degree) 단위의 입력에 대해 사인(Sin)을 계산합니다.
    """
    return math.sin(X * DegtoRad)


def Cosd(X: float) -> float:
    """
    도(degree) 단위의 입력에 대해 코사인(Cos)을 계산합니다.
    """
    return math.cos(X * DegtoRad)


def Tand(X: float) -> float:
    """
    도(degree) 단위의 입력에 대해 탄젠트(Tan)를 계산합니다.
    """
    return math.tan(X * DegtoRad)


def Arcsind(X: float) -> float:
    """
    도(degree) 단위로 역사인(Arcsin)을 계산합니다.
    """
    # 원본: RadtoDeg * Atn(X / Sqr(1 - X * X))
    # Python: math.asin(X) * RadtoDeg
    # 입력 값이 1을 초과하거나 -1 미만인 경우 math.asin은 ValueError를 발생시키지만,
    # 원본 VBA 코드가 X >= 1인 경우 90을 반환하도록 처리했기 때문에
    # math.asin을 사용하는 것이 더 간결하며, 필요하다면 예외 처리가 추가될 수 있습니다.
    if X >= 1:
        return 90.0
    elif X <= -1:  # VBA 원본에는 없지만, 안전을 위해 추가
        return -90.0
    return Arcsin(X) * RadtoDeg


def Arccosd(X: float) -> float:
    """
    도(degree) 단위로 역코사인(Arccos)을 계산합니다.
    """
    # 원본: 90 - RadtoDeg * Atn(X / Sqr(1 - X * X))
    return Arccos(X) * RadtoDeg


def Arctand(X: float) -> float:
    """
    도(degree) 단위로 역탄젠트(Arctan)를 계산합니다.
    """
    # 원본: RadtoDeg * Atn(X)
    return math.atan(X) * RadtoDeg


def Rev(X: float) -> float:
    """
    각도를 0 ~ 360도 범위로 정규화합니다.
    """
    # Python의 % 연산자는 C나 VBA의 Mod와 달리 결과의 부호가 피제수(360)의 부호를 따릅니다.
    # 따라서, 음수 입력에 대해서도 0과 360 사이의 값을 보장하기 위해 추가적인 로직이 필요합니다.
    result = X % 360.0
    if result < 0:
        result += 360.0
    return result


def Arctan2(y: float, X: float) -> float:
    """
    4사분면을 고려하여 라디안 단위로 역탄젠트(Arctan2)를 계산합니다. (VBA Arctan2 변환)
    Python의 math.atan2(y, x)와 동일합니다.
    """
    # Python의 math.atan2는 VBA에서 복잡하게 구현된 4사분면 로직을 모두 처리합니다.
    # 인수의 순서는 math.atan2(y, x) 입니다.
    return math.atan2(y, X)


def Arctan2d(y: float, X: float) -> float:
    """
    4사분면을 고려하여 도(degree) 단위로 역탄젠트(Arctan2)를 계산합니다.
    """
    # 결과가 -180도 ~ 180도 범위로 나옴.
    return Arctan2(y, X) * RadtoDeg


def Log10(X: float) -> float:
    """
    10을 밑으로 하는 로그(Log10)를 계산합니다.
    """
    # Python의 math.log10(X)를 사용하거나, math.log(X, 10)을 사용합니다.
    # 원본 로직: Log(X) / Log(10)
    # VBA에서는 Log가 자연로그(밑 e)이므로, math.log를 사용합니다.
    if X < 0:
        # VBA 원본이 X < 0 이면 X = -X 로 처리했습니다.
        X = -X
    return math.log(X) / 2.30258509299405
    # return math.log10(X) # Python 내장 함수 사용 시


# --- 보간 함수 ---

def Inter3(Y1: float, Y2: float, Y3: float, N: float) -> float:
    """
    3개의 항을 이용한 보간법 (Lagrange 보간법)을 계산합니다.
    """
    a = Y2 - Y1
    B = Y3 - Y2
    c = Y1 + Y3 - 2 * Y2

    # Inter3 = Y2 + (N / 2) * (a + B + N * c)
    return Y2 + (N / 2.0) * (a + B + N * c)


# --- 좌표 변환 함수 ---

# RectToSph와 SphToRect 함수는 값을 in-place로 변경하기 위해 튜플로 반환하거나
# 클래스/리스트를 사용할 수 있지만, VBA Sub처럼 여러 값을 반환하는 형태로 구현합니다.

def SphToRect(a: float, B: float, r: float = 1000.0) -> tuple[float, float, float]:
    """
    구면좌표(경도 a, 위도 B, 모두 degree)에서 직교좌표(X, y, Z)로 변환합니다.
    """
    a_rad = a * DegtoRad
    B_rad = B * DegtoRad

    X = r * math.cos(a_rad) * math.cos(B_rad)
    y = r * math.sin(a_rad) * math.cos(B_rad)
    Z = r * math.sin(B_rad)
    return X, y, Z


def RectToSph(X: float, y: float, Z: float, r: float = 1000.0) -> tuple[float, float]:
    """
    직교좌표(X, y, Z)에서 구면좌표(경도 a, 위도 B, 모두 degree)로 변환합니다.
    """
    # VBA 원본은 Rev(Arctan2d(y, X))
    a = Rev(Arctan2d(y, X))

    # VBA 원본: B = Arcsind(Z / 1000#)
    B = Arcsind(Z / r)

    return a, B


def RTS_Real(X: float, y: float, Z: float) -> tuple[float, float]:
    """
    직교좌표(X, y, Z)에서 구면좌표(경도 a, 위도 B, 모두 degree)로 변환합니다. (길이 계산 포함)
    """
    r = math.sqrt(X * X + y * y + Z * Z)

    # VBA 원본: a = Rev(Arctan2d(y, X))
    a = Rev(Arctan2d(y, X))

    # VBA 원본: B = Arcsind(Z / Sqr(X * X + y * y + Z * Z))
    B = Arcsind(Z / r)

    return a, B


def Inter3Sph(A1: float, B1: float, A2: float, B2: float, A3: float, B3: float, N: float) -> tuple[float, float]:
    """
    3개의 구면 좌표를 직교 좌표로 변환 후 보간하고, 다시 구면 좌표로 변환합니다.
    """
    # 1. 구면 좌표 -> 직교 좌표 (r=1000.0 가정)
    X1, Y1, Z1 = SphToRect(A1, B1)
    X2, Y2, Z2 = SphToRect(A2, B2)
    X3, Y3, Z3 = SphToRect(A3, B3)

    # 2. 직교 좌표 보간
    rx = Inter3(X1, X2, X3, N)
    ry = Inter3(Y1, Y2, Y3, N)
    rz = Inter3(Z1, Z2, Z3, N)

    # 3. 직교 좌표 -> 구면 좌표 (RTS_Real 사용)
    resLon, resLat = RTS_Real(rx, ry, rz)

    return resLon, resLat


# --- 회전 함수 ---

# VBA Function은 인수를 ByRef로 받아 in-place로 변경했지만,
# Python에서는 인수를 튜플로 받아 변경된 튜플을 반환하도록 구현합니다.
# 또는 리스트/mutable 객체를 사용하여 in-place 변경을 시뮬레이션 할 수도 있습니다.
# 여기서는 튜플을 반환하는 함수로 구현합니다.

def RotX(X: float, y: float, Z: float, Rot: float) -> tuple[float, float, float]:
    """
    X축을 중심으로 회전합니다. (Rot: degree)
    """
    Rot_rad = Rot * DegtoRad

    # X는 불변
    X_new = X
    # Y1 = y * Cos(Rot) + Z * Sin(Rot)
    y_new = y * math.cos(Rot_rad) + Z * math.sin(Rot_rad)
    # Z1 = -y * Sin(Rot) + Z * Cos(Rot)
    Z_new = -y * math.sin(Rot_rad) + Z * math.cos(Rot_rad)

    return X_new, y_new, Z_new


def RotY(X: float, y: float, Z: float, Rot: float) -> tuple[float, float, float]:
    """
    Y축을 중심으로 회전합니다. (Rot: degree)
    """
    Rot_rad = Rot * DegtoRad

    # Y는 불변
    y_new = y
    # X1 = X * Cos(Rot) - Z * Sin(Rot)
    X_new = X * math.cos(Rot_rad) - Z * math.sin(Rot_rad)
    # Z1 = X * Sin(Rot) + Z * Cos(Rot)
    Z_new = X * math.sin(Rot_rad) + Z * math.cos(Rot_rad)

    return X_new, y_new, Z_new


def RotZ(X: float, y: float, Z: float, Rot: float) -> tuple[float, float, float]:
    """
    Z축을 중심으로 회전합니다. (Rot: degree)
    """
    Rot_rad = Rot * DegtoRad

    # Z는 불변
    Z_new = Z
    # X1 = X * Cos(Rot) + y * Sin(Rot)
    X_new = X * math.cos(Rot_rad) + y * math.sin(Rot_rad)
    # Y1 = -X * Sin(Rot) + y * Cos(Rot)
    y_new = -X * math.sin(Rot_rad) + y * math.cos(Rot_rad)

    return X_new, y_new, Z_new
