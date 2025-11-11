import math
from typing import List, Tuple, Dict, Any

# --- External Dependencies (Placeholders - MUST BE IMPLEMENTED) ---

# Global variables/constants simulated
E: List[float] = []  # Array to hold Julian Day times of phenomena
S: List[str] = []  # Array to hold descriptions of phenomena
TIME_ZONE: float = 9.0  # Placeholder for TimeZone (e.g., KST = +9.0 hours)


def inv_jd(jd: float) -> Tuple[float, float, float, float, float]:
    """
    Placeholder for InvJD: Converts Julian Day to date components and two constants (A1, B1).
    Returns: (Year, Month, Day, A1_out, B1_out)
    """
    # *** Replace with actual JD to date conversion and constant derivation logic ***
    return 2000.0, 1.0, 1.0, 0.0, 0.0


def sind(degree: float) -> float:
    """Placeholder for Sind: Sine function for input in Degrees."""
    return math.sin(math.radians(degree))


def cosd(degree: float) -> float:
    """Placeholder for Cosd: Cosine function for input in Degrees."""
    return math.cos(math.radians(degree))


def get_moon(jd: float, phase_angle_deg: float, tz: float) -> float:
    """
    Placeholder for GetMoon: Calculates the Julian Day of a specific moon phase.
    Phase Angle: 0=New, 90=First Quarter, 180=Full, 270=Last Quarter (Approx.)
    """
    # *** Replace with actual moon phase calculation logic ***
    # The return value is expected to be in JD, relative to TZ
    return jd + 5.0  # Dummy value


# --- Core Functions ---

def set_const(p: int, j: int) -> Tuple[float, float, float, float]:
    """
    VBA Sub SetConst: Sets constants for the period of the synodic cycle (B),
    mean anomaly rate (M1), and the epoch reference (A1, M0).
    Args:
        p (int): Planet ID (1=Mercury, 2=Venus, ..., 7=Neptune)
        j (int): Phenomenon type (0 or 1)
    Returns: (A1, B1, M0, M1)
    """
    A1, B1, M0, M1 = 0.0, 0.0, 0.0, 0.0

    if p == 1:  # Mercury (수성)
        B1, M1 = 115.8774771, 114.2088742
        if j == 0:  # Inferior Conjunction (내합) / Elongation E
            A1, M0 = 2451612.023, 63.5867
        elif j == 1:  # Superior Conjunction (외합) / Elongation W
            A1, M0 = 2451554.084, 6.4822
    elif p == 2:  # Venus (금성)
        B1, M1 = 583.921361, 215.513058
        if j == 0:  # Inferior Conjunction (내합) / Elongation E
            A1, M0 = 2451996.706, 82.7311
        elif j == 1:  # Superior Conjunction (외합) / Elongation W
            A1, M0 = 2451704.746, 154.9745
    elif p == 3:  # Mars (화성)
        B1, M1 = 779.936104, 48.705244
        if j == 0:  # Opposition (충)
            A1, M0 = 2452097.382, 181.9573
        elif j == 1:  # Conjunction (합)
            A1, M0 = 2451707.414, 157.6047
    elif p == 4:  # Jupiter (목성)
        B1, M1 = 398.884046, 33.140229
        if j == 0:  # Opposition (충)
            A1, M0 = 2451870.628, 318.4681
        elif j == 1:  # Conjunction (합)
            A1, M0 = 2451671.186, 121.898
    elif p == 5:  # Saturn (토성)
        B1, M1 = 378.091904, 12.647487
        if j == 0:  # Opposition (충)
            A1, M0 = 2451870.17, 318.0172
        elif j == 1:  # Conjunction (합)
            A1, M0 = 2451681.124, 131.6934
    elif p == 6:  # Uranus (천왕성)
        B1, M1 = 369.656035, 4.333093
        if j == 0:  # Opposition (충)
            A1, M0 = 2451764.317, 213.6884
        elif j == 1:  # Conjunction (합)
            A1, M0 = 2451579.489, 31.5219
    elif p == 7:  # Neptune (해왕성)
        B1, M1 = 367.486703, 2.194998
        if j == 0:  # Opposition (충)
            A1, M0 = 2451753.122, 202.6544
        elif j == 1:  # Conjunction (합)
            A1, M0 = 2451569.379, 21.5569

    # Note: VBA passes a and B by reference for all planets, but only P=1,2 modifies B.
    # We return B1 here, following the function signature.
    return A1, B1, M0, M1


def cor_time(p: int, j: int, T: float, M: float, a: float, b: float, c: float, d: float, e: float, f: float,
             g: float) -> float:
    """
    VBA Function CorTime: Calculates the correction time (in days) for Conjunction/Opposition.
    Uses terms based on T (Julian Century) and M (Mean Anomaly).
    """
    T2 = T * T
    sm1, cm1 = sind(M), cosd(M)
    sm2, cm2 = sind(2 * M), cosd(2 * M)
    sm3, cm3 = sind(3 * M), cosd(3 * M)
    sm4, cm4 = sind(4 * M), cosd(4 * M)
    sm5, cm5 = sind(5 * M), cosd(5 * M)
    R = 0.0

    # Mercury (수성): 1
    if p == 1 and j == 0:  # 내합 (Inferior Conjunction)
        R = 0.0545 + 0.0002 * T
        R += sm1 * (-6.2008 + 0.0074 * T + 0.00003 * T2) + cm1 * (-3.275 - 0.0197 * T + 0.00001 * T2)
        R += sm2 * (0.4737 - 0.0052 * T - 0.00001 * T2) + cm2 * (0.8111 + 0.0033 * T - 0.00002 * T2)
        R += sm3 * (0.0037 + 0.0018 * T) + cm3 * (-0.1768 + 0.00001 * T2)
        R += sm4 * (-0.0211 - 0.0004 * T) + cm4 * (0.0326 - 0.0003 * T)
        R += sm5 * (0.0083 + 0.0001 * T) + cm5 * (-0.004 + 0.0001 * T)
    elif p == 1 and j == 1:  # 외합 (Superior Conjunction)
        R = -0.0548 - 0.0002 * T
        R += sm1 * (7.3894 - 0.01 * T - 0.00003 * T2) + cm1 * (3.22 + 0.0197 * T - 0.00001 * T2)
        R += sm2 * (0.8383 - 0.0064 * T - 0.00001 * T2) + cm2 * (0.9666 + 0.0039 * T - 0.00003 * T2)
        R += sm3 * (0.077 - 0.0026 * T) + cm3 * (0.2758 + 0.0002 * T - 0.00002 * T2)
        R += sm4 * (-0.0128 - 0.0008 * T) + cm4 * (0.0734 - 0.0004 * T - 0.00001 * T2)
        R += sm5 * (-0.0122 - 0.0002 * T) + cm5 * (0.0173 - 0.0002 * T2)

    # Venus (금성): 2
    elif p == 2 and j == 0:  # 내합 (Inferior Conjunction)
        R = -0.0096 + 0.0002 * T - 0.00001 * T2
        R += sm1 * (2.0009 - 0.0033 * T - 0.00001 * T2) + cm1 * (0.598 - 0.0104 * T + 0.00001 * T2)
        R += sm2 * (0.0967 - 0.0016 * T - 0.00003 * T2) + cm2 * (0.0913 + 0.0009 * T - 0.00002 * T2)
        R += sm3 * (0.0046 - 0.0002 * T) + cm3 * (0.0079 + 0.0001 * T)
    elif p == 2 and j == 1:  # 외합 (Superior Conjunction)
        R = 0.0099 - 0.0002 * T - 0.00001 * T2
        R += sm1 * (4.1991 - 0.0121 * T - 0.00003 * T2) + cm1 * (-0.6095 + 0.0102 * T - 0.00002 * T2)
        R += sm2 * (0.25 - 0.0028 * T - 0.00003 * T2) + cm2 * (0.0063 + 0.0025 * T - 0.00002 * T2)
        R += sm3 * (0.0232 - 0.0005 * T - 0.00001 * T2) + cm3 * (0.0031 + 0.0004 * T)

    # Mars (화성): 3
    elif p == 3 and j == 0:  # 충 (Opposition)
        R = -0.3088 + 0.00002 * T2
        R += sm1 * (-17.6965 + 0.0363 * T + 0.00005 * T2) + cm1 * (18.3131 + 0.0467 * T - 0.00006 * T2)
        R += sm2 * (-0.2162 - 0.0198 * T - 0.00001 * T2) + cm2 * (-4.5028 - 0.0019 * T + 0.00007 * T2)
        R += sm3 * (0.8987 + 0.0058 * T - 0.00002 * T2) + cm3 * (0.7666 - 0.005 * T - 0.00003 * T2)
        R += sm4 * (-0.3636 - 0.0001 * T + 0.00002 * T2) + cm4 * (0.0402 + 0.0032 * T)
        R += sm5 * (0.0737 - 0.0008 * T) + cm5 * (-0.098 - 0.0011 * T)
    elif p == 3 and j == 1:  # 합 (Conjunction)
        R = 0.3102 - 0.0001 * T + 0.00001 * T2
        R += sm1 * (9.7273 - 0.0156 * T + 0.00001 * T) + cm1 * (-18.3195 - 0.0467 * T + 0.00009 * T2)
        R += sm2 * (-1.6488 - 0.0133 * T + 0.00001 * T2) + cm2 * (-2.6117 - 0.002 * T + 0.00004 * T2)
        R += sm3 * (-0.6827 - 0.0026 * T + 0.00001 * T2) + cm3 * (0.0281 + 0.0035 * T + 0.00001 * T2)
        R += sm4 * (-0.0823 + 0.0006 * T + 0.00001 * T2) + cm4 * (0.1584 + 0.0013 * T)
        R += sm5 * (0.027 + 0.0005 * T) + cm5 * 0.0433

    # Jupiter (목성): 4
    elif p == 4 and j == 0:  # 충 (Opposition)
        R = -0.1029 - 0.00009 * T2
        R += sm1 * (-1.9658 - 0.0056 * T + 0.00007 * T2) + cm1 * (6.1537 + 0.021 * T - 0.00006 * T2)
        R += sm2 * (-0.2081 - 0.0013 * T) + cm2 * (-0.1116 - 0.001 * T)
        R += sm3 * (0.0074 + 0.0001 * T) + cm3 * (-0.0097 - 0.0001 * T)
        R += sind(a) * (0.0144 * T - 0.00008 * T2) + cosd(a) * (0.3642 - 0.0019 * T - 0.00029 * T2)
    elif p == 4 and j == 1:  # 합 (Conjunction)
        R = 0.1027 - 0.0002 * T - 0.00009 * T2
        R += sm1 * (-2.2637 + 0.0163 * T - 0.00003 * T2) + cm1 * (-6.154 - 0.021 * T - 0.00003 * T2)
        R += sm2 * (-0.2021 - 0.0017 * T + 0.00001 * T2) + cm2 * (0.131 - 0.0008 * T)
        R += sm3 * 0.0086 + cm3 * (0.0087 + 0.0002 * T)
        R += sind(a) * (0.0144 * T - 0.00008 * T2) + cosd(a) * (0.3642 - 0.0019 * T - 0.00029 * T2)

    # Saturn (토성): 5
    elif p == 5 and j == 0:  # 충 (Opposition)
        R = -0.0209 + 0.0006 * T + 0.00023 * T2
        R += sm1 * (4.5795 - 0.0312 * T - 0.00017 * T2) + cm1 * (1.1462 - 0.0351 * T + 0.00011 * T2)
        R += sm2 * (0.0985 - 0.0015 * T) + cm2 * (0.0733 - 0.0031 * T + 0.00001 * T2)
        R += sm3 * (0.0025 - 0.0001 * T) + cm3 * (0.005 - 0.0002 * T)
        R += sind(a) * (-0.0337 * T + 0.00018 * T2) + cosd(a) * (-0.851 + 0.0044 * T + 0.00068 * T2)
        R += sind(b) * (-0.0064 * T + 0.00004 * T2) + cosd(b) * (0.2397 - 0.0012 * T - 0.00008 * T2)
        R += sind(c) * (-0.001 * T) + cosd(c) * (0.1245 + 0.0006 * T)
        R += sind(d) * (0.0024 * T - 0.00003 * T2) + cosd(d) * (0.0477 - 0.0005 * T - 0.00006 * T2)
    elif p == 5 and j == 1:  # 합 (Conjunction)
        R = 0.0172 - 0.0006 * T + 0.00023 * T2
        R += sm1 * (-8.5885 + 0.0411 * T + 0.0002 * T2) + cm1 * (-1.147 + 0.0352 * T - 0.00011 * T2)
        R += sm2 * (0.3331 - 0.0034 * T - 0.00001 * T2) + cm2 * (0.1145 - 0.0045 * T + 0.00002 * T2)
        R += sm3 * (-0.0169 + 0.0002 * T) + cm3 * (-0.0109 + 0.0004 * T)
        R += sind(a) * (-0.0337 * T + 0.00018 * T2) + cosd(a) * (-0.851 + 0.0044 * T + 0.00068 * T2)
        R += sind(b) * (-0.0064 * T + 0.00004 * T2) + cosd(b) * (0.2397 - 0.0012 * T - 0.00008 * T2)
        R += sind(c) * (-0.001 * T) + cosd(c) * (0.1245 + 0.0006 * T)
        R += sind(d) * (0.0024 * T - 0.00003 * T2) + cosd(d) * (0.0477 - 0.0005 * T - 0.00006 * T2)

    # Uranus (천왕성): 6
    elif p == 6 and j == 0:  # 충 (Opposition)
        R = 0.0844 - 0.0006 * T
        R += sm1 * (-0.1048 + 0.0246 * T) + cm1 * (-5.1221 + 0.0104 * T + 0.00003 * T2)
        R += sm2 * (-0.1428 + 0.0005 * T) + cm2 * (-0.0148 - 0.0013 * T)
        R += cm3 * 0.0055
        R += cosd(e) * 0.885 + cosd(f) * 0.2153
    elif p == 6 and j == 1:  # 합 (Conjunction)
        R = -0.0859 + 0.0003 * T
        R += sm1 * (-3.8179 - 0.0148 * T + 0.00003 * T2) + cm1 * (5.1228 - 0.0105 * T - 0.00002 * T2)
        R += sm2 * (-0.0803 + 0.0011 * T) + cm2 * (-0.1905 - 0.0006 * T)
        R += sm3 * (0.0088 + 0.0001 * T)
        R += cosd(e) * 0.885 + cosd(f) * 0.2153

    # Neptune (해왕성): 7
    elif p == 7 and j == 0:  # 충 (Opposition)
        R = -0.014 + 0.00001 * T2
        R += sm1 * (-1.3486 + 0.001 * T + 0.00001 * T2) + cm1 * (0.8597 + 0.0037 * T)
        R += sm2 * (-0.0082 - 0.0002 * T + 0.00001 * T2) + cm2 * (0.0037 - 0.0003 * T)
        R += cosd(e) * -0.5964 + cosd(g) * 0.0728
    elif p == 7 and j == 1:  # 합 (Conjunction)
        R = 0.0168
        R += sm1 * (-2.5606 + 0.0088 * T + 0.00002 * T2) + cm1 * (-0.8611 - 0.0037 * T + 0.00002 * T2)
        R += sm2 * (0.0118 - 0.0004 * T - 0.00001 * T2) + cm2 * (0.0307 - 0.0003 * T)
        R += cosd(e) * -0.5964 + cosd(g) * 0.0728

    return R


def cor_time2(p: int, j: int, T: float, M: float) -> float:
    """
    VBA Function CorTime2: Calculates the correction time (in days) for Greatest Elongation (Mercury, Venus).
    """
    T2 = T * T
    sm1, cm1 = sind(M), cosd(M)
    sm2, cm2 = sind(2 * M), cosd(2 * M)
    sm3, cm3 = sind(3 * M), cosd(3 * M)
    sm4, cm4 = sind(4 * M), cosd(4 * M)
    sm5, cm5 = sind(5 * M), cosd(5 * M)
    R = 0.0

    # Mercury (수성): 1
    if p == 1 and j == 0:  # 동방최대이각 (Greatest Eastern Elongation)
        R = -21.6101 + 0.0002 * T
        R += sm1 * (-1.9803 - 0.006 * T + 0.00001 * T2) + cm1 * (1.4151 - 0.0072 * T - 0.00001 * T2)
        R += sm2 * (0.5528 - 0.0005 * T - 0.00001 * T2) + cm2 * (0.2905 + 0.0034 * T + 0.00001 * T2)
        R += sm3 * (-0.1121 - 0.0001 * T + 0.00001 * T2) + cm3 * (-0.0098 - 0.0015 * T)
        R += sm4 * 0.0192 + cm4 * (0.0111 + 0.0004 * T)
        R += sm5 * -0.0061 + cm5 * (-0.0032 - 0.0001 * T)
    elif p == 1 and j == 1:  # 서방최대이각 (Greatest Western Elongation)
        R = 21.6249 - 0.0002 * T
        R += sm1 * (0.1306 + 0.0065 * T) + cm1 * (-2.7661 - 0.0011 * T + 0.00001 * T2)
        R += sm2 * (0.2438 - 0.0024 * T - 0.00001 * T2) + cm2 * (0.5767 + 0.0023 * T)
        R += sm3 * 0.1041 + cm3 * (-0.0184 + 0.0007 * T)
        R += sm4 * (-0.0051 - 0.0001 * T) + cm4 * (0.0048 + 0.0001 * T)
        R += sm5 * 0.0026 + cm5 * 0.0037

    # Venus (금성): 2
    elif p == 2 and j == 0:  # 동방최대이각 (Greatest Eastern Elongation)
        R = -70.76 + 0.0002 * T - 0.00001 * T2
        R += sm1 * (1.0282 - 0.001 * T - 0.00001 * T2) + cm1 * (0.2761 - 0.006 * T)
        R += sm2 * (-0.0438 - 0.0023 * T + 0.00002 * T2) + cm2 * (0.166 - 0.0037 * T - 0.00004 * T2)
        R += sm3 * (0.0036 + 0.0001 * T) + cm3 * (-0.0011 + 0.00001 * T2)
    elif p == 2 and j == 1:  # 서방최대이각 (Greatest Western Elongation)
        R = 70.7462 - 0.00001 * T2
        R += sm1 * (1.1218 - 0.0025 * T - 0.00001 * T2) + cm1 * (0.4538 - 0.0066 * T)
        R += sm2 * (0.132 + 0.002 * T - 0.00003 * T2) + cm2 * (-0.0702 + 0.0022 * T + 0.00004 * T2)
        R += sm3 * (0.0062 - 0.0001 * T) + cm3 * (0.0015 - 0.00001 * T2)

    return R


def cor_time3(p: int, j: int, T: float, M: float, a: float, b: float, c: float, d: float) -> float:
    """
    VBA Function CorTime3: Calculates the correction time (in days) for Stationary Points (유).
    P=1, 2, 3, 4, 5 (Mercury to Saturn). j=0: 1st Stationary, j=1: 2nd Stationary.
    """
    T2 = T * T
    sm1, cm1 = sind(M), cosd(M)
    sm2, cm2 = sind(2 * M), cosd(2 * M)
    sm3, cm3 = sind(3 * M), cosd(3 * M)
    sm4, cm4 = sind(4 * M), cosd(4 * M)
    sm5, cm5 = sind(5 * M), cosd(5 * M)
    R = 0.0

    # Mercury (수성): 1
    if p == 1 and j == 0:  # 1st Stationary (First Station)
        R = -11.0761 + 0.0003 * T
        R += sm1 * (-4.7321 + 0.0023 * T + 0.00002 * T2) + cm1 * (-1.323 - 0.0156 * T2)
        R += sm2 * (0.227 - 0.0046 * T) + cm2 * (0.7184 + 0.0013 * T - 0.00002 * T2)
        R += sm3 * (0.0638 + 0.0016 * T) + cm3 * (-0.1655 + 0.0007 * T)
        R += sm4 * (-0.0395 - 0.0003 * T) + cm4 * (0.0247 - 0.0006 * T)
        R += sm5 * 0.0131 + cm3 * (0.0008 + 0.0002 * T)
    elif p == 1 and j == 1:  # 2nd Stationary (Second Station)
        R = 11.1343 - 0.0001 * T
        R += sm1 * (-3.9137 + 0.0073 * T + 0.00002 * T2) + cm1 * (-3.3861 - 0.0128 * T + 0.00001 * T2)
        R += sm2 * (0.5222 - 0.004 * T - 0.00002 * T2) + cm2 * (0.5929 + 0.0039 * T - 0.00002 * T2)
        R += sm3 * (-0.0593 + 0.0018 * T) + cm3 * (-0.1733 - 0.0007 * T + 0.00001 * T2)
        R += sm4 * (-0.0053 - 0.0006 * T) + cm4 * (0.0476 - 0.0001 * T)
        R += sm5 * (0.007 + 0.0002 * T) + cm5 * (-0.0115 + 0.0001 * T)

    # Venus (금성): 2
    elif p == 2 and j == 0:  # 1st Stationary
        R = -21.0672 + 0.0002 * T - 0.00001 * T2
        R += sm1 * (1.9396 - 0.0029 * T - 0.00001 * T2) + cm1 * (1.0727 - 0.0102 * T)
        R += sm2 * (0.0404 - 0.0023 * T - 0.00001 * T2) + cm2 * (0.1305 - 0.0004 * T - 0.00003 * T2)
        R += sm3 * (-0.0007 - 0.0002 * T) + cm3 * 0.0098
    elif p == 2 and j == 1:  # 2nd Stationary
        R = 21.0623 - 0.00001 * T2
        R += sm1 * (1.9913 - 0.004 * T - 0.00001 * T2) + cm1 * (-0.0407 - 0.0077 * T)
        R += sm2 * (0.1351 - 0.0009 * T - 0.00004 * T2) + cm2 * (0.0303 + 0.0019 * T)
        R += sm3 * (0.0089 - 0.0002 * T) + cm3 * (0.0043 + 0.0001 * T)

    # Mars (화성): 3
    elif p == 3 and j == 0:  # 1st Stationary
        R = -37.079 - 0.0009 * T + 0.00002 * T2
        R += sm1 * (-20.0651 + 0.0228 * T + 0.00004 * T2) + cm1 * (14.5205 + 0.0504 * T - 0.00001 * T2)
        R += sm2 * (1.1737 - 0.0169 * T) + cm2 * (-4.255 - 0.0075 * T + 0.00008 * T2)
        R += sm3 * (0.4897 + 0.0074 * T - 0.00001 * T2) + cm3 * (1.1151 - 0.0021 * T - 0.00005 * T2)
        R += sm4 * (-0.3636 - 0.002 * T + 0.00001 * T2) + cm4 * (-0.1769 + 0.0028 * T + 0.00002 * T2)
        R += sm5 * (0.1437 - 0.0004 * T) + cm5 * (-0.0383 - 0.0016 * T)
    elif p == 3 and j == 1:  # 2nd Stationary
        R = 36.7191 + 0.0016 * T + 0.00003 * T2
        R += sm1 * (-12.6163 + 0.0417 * T - 0.00001 * T2) + cm1 * (20.1218 + 0.0379 * T - 0.00006 * T2)
        R += sm2 * (-1.636 - 0.019 * T) + cm2 * (-3.9657 + 0.0045 * T + 0.00007 * T2)
        R += sm3 * (1.1546 + 0.0029 * T - 0.00003 * T2) + cm3 * (0.2888 - 0.0073 * T - 0.00002 * T2)
        R += sm4 * (-0.3128 + 0.0017 * T + 0.00002 * T2) + cm4 * (0.2513 + 0.0026 * T - 0.00002 * T2)
        R += sm5 * (-0.0021 - 0.0016 * T) + cm5 * (-0.1497 - 0.0006 * T)

    # Jupiter (목성): 4
    elif p == 4 and j == 0:  # 1st Stationary
        R = -60.367 - 0.0001 * T - 0.00009 * T2
        R += sm1 * (-2.3144 - 0.0124 * T + 0.00007 * T2) + cm1 * (6.7439 + 0.0166 * T - 0.00006 * T2)
        R += sm2 * (-0.2259 - 0.001 * T) + cm2 * (-0.1497 - 0.0014 * T)
        R += sm3 * (0.0105 + 0.0001 * T) + cm3 * -0.0098
        R += sind(a) * (0.0144 * T - 0.00008 * T2) + cosd(a) * (0.3642 - 0.0019 * T - 0.00029 * T2)
    elif p == 4 and j == 1:  # 2nd Stationary
        R = 60.3023 + 0.0002 * T - 0.00009 * T2
        R += sm1 * (0.3506 - 0.0034 * T + 0.00004 * T2) + cm1 * (5.3635 + 0.0274 * T - 0.00007 * T2)
        R += sm2 * (-0.1872 - 0.0016 * T) + cm2 * (-0.0037 - 0.0005 * T)
        R += sm3 * (0.0012 + 0.0001 * T) + cm3 * (-0.0096 - 0.0001 * T)
        R += sind(a) * (0.0144 * T - 0.00008 * T2) + cosd(a) * (0.3642 - 0.0019 * T - 0.00029 * T2)

    # Saturn (토성): 5
    elif p == 5 and j == 0:  # 1st Stationary
        R = -68.884 + 0.0009 * T + 0.00023 * T2
        R += sm1 * (5.5452 - 0.0279 * T - 0.0002 * T2) + cm1 * (3.0727 - 0.043 * T + 0.00007 * T2)
        R += sm2 * (0.1101 - 0.0006 * T - 0.00001 * T2) + cm2 * (0.1654 - 0.0043 * T + 0.00001 * T2)
        R += sm3 * (0.001 + 0.0001 * T) + cm3 * (0.0095 - 0.0003 * T)
        R += sind(a) * (-0.0337 * T + 0.00018 * T2) + cosd(a) * (-0.851 + 0.0044 * T + 0.00068 * T2)
        R += sind(b) * (-0.0064 * T + 0.00004 * T2) + cosd(b) * (0.2397 - 0.0012 * T - 0.00008 * T2)
        R += sind(c) * (-0.001 * T) + cosd(c) * (0.1245 + 0.0006 * T)
        R += sind(d) * (0.0024 * T - 0.00003 * T2) + cosd(d) * (0.0477 - 0.0005 * T - 0.00006 * T2)
    elif p == 5 and j == 1:  # 2nd Stationary
        R = 68.872 - 0.0007 * T + 0.00023 * T2
        R += sm1 * (5.9399 - 0.04 * T - 0.00015 * T2) + cm1 * (-0.7998 - 0.0266 * T + 0.00014 * T2)
        R += sm2 * (0.1738 - 0.0032 * T) + cm2 * (-0.0039 - 0.0024 * T + 0.00001 * T2)
        R += sm3 * (0.0073 - 0.0002 * T) + cm3 * (0.002 - 0.0002 * T)
        R += sind(a) * (-0.0337 * T + 0.00018 * T2) + cosd(a) * (-0.851 + 0.0044 * T + 0.00068 * T2)
        R += sind(b) * (-0.0064 * T + 0.00004 * T2) + cosd(b) * (0.2397 - 0.0012 * T - 0.00008 * T2)
        R += sind(c) * (-0.001 * T) + cosd(c) * (0.1245 + 0.0006 * T)
        R += sind(d) * (0.0024 * T - 0.00003 * T2) + cosd(d) * (0.0477 - 0.0005 * T - 0.00006 * T2)

    return R


def find_planet(jd: float, p: int, j: int) -> float:
    """
    VBA Function FindPlanet: Calculates the Julian Day of the next Conjunction/Opposition.
    p: Planet ID (1-7), j: Type (0=Inf. Conj./Opp., 1=Sup. Conj./Conj.)
    """

    # 1. Get Initial Constants and Interpolation Parameters
    y, mo, da, A1, B1_dummy = inv_jd(jd)  # InvJD is assumed to return A1, B1
    y += mo / 12.0 + da / 365.0

    A1, B1, M0, M1 = set_const(p, j)  # Get the correct A1, B1, M0, M1 based on P and J

    # 2. Calculate k (number of cycles passed) and JDE0 (approximate JD)
    k = math.floor((365.2425 * y + 1721060.0 - A1) / B1)
    JDE0 = A1 + k * B1
    M = M0 + k * M1  # Mean Anomaly

    # 3. Calculate Julian Century T
    T = (JDE0 - 2451545.0) / 36525.0

    # 4. Calculate Perturbation Terms (a, B, c, d, E, f, g)
    a, b, c, d, e, f, g = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    if p == 4:  # Jupiter
        a = 82.74 + 40.76 * T
    elif p == 5:  # Saturn
        a = 82.74 + 40.76 * T
        b = 29.86 + 1181.36 * T
        c = 14.13 + 590.68 * T
        d = 220.02 + 1262.87 * T
    elif p == 6:  # Uranus
        e = 207.83 + 8.51 * T
        f = 108.84 + 419.96 * T
    elif p == 7:  # Neptune
        e = 207.83 + 8.51 * T
        g = 276.74 + 209.98 * T

    # 5. Apply Correction Time (ct)
    ct = cor_time(p, j, T, M, a, b, c, d, e, f, g)
    R = JDE0 + ct

    return R


def elong_planet(jd: float, p: int, j: int) -> float:
    """
    VBA Function ElongPlanet: Calculates the Julian Day of the next Greatest Elongation (Mercury, Venus).
    p: Planet ID (1=Mercury, 2=Venus), j: Type (0=Greatest Eastern, 1=Greatest Western)
    """

    y, mo, da, A1_dummy, B1_dummy = inv_jd(jd)
    y += mo / 12.0 + da / 365.0

    # SetConst for Elongation uses j=0 for A1/M0/B1/M1 determination regardless of actual j
    A1, B1, M0, M1 = set_const(p, 0)

    k = math.floor((365.2425 * y + 1721060.0 - A1) / B1)
    JDE0 = A1 + k * B1
    M = M0 + k * M1

    T = (JDE0 - 2451545.0) / 36525.0
    ct = cor_time2(p, j, T, M)  # CorTime2 handles the two j cases (0 or 1)
    R = JDE0 + ct

    return R


def station_planet(jd: float, p: int, j: int) -> float:
    """
    VBA Function StationPlanet: Calculates the Julian Day of the next Stationary Point (Mercury to Saturn).
    p: Planet ID (1-5), j: Type (0=1st Stationary, 1=2nd Stationary)
    """

    y, mo, da, A1_dummy, B1_dummy = inv_jd(jd)
    y += mo / 12.0 + da / 365.0

    # SetConst for Stationary uses j=0 for A1/M0/B1/M1 determination regardless of actual j
    A1, B1, M0, M1 = set_const(p, 0)

    k = math.floor((365.2425 * y + 1721060.0 - A1) / B1)
    JDE0 = A1 + k * B1
    M = M0 + k * M1

    T = (JDE0 - 2451545.0) / 36525.0

    # Calculate Perturbation Terms (a, B, c, d)
    a, b, c, d = 0.0, 0.0, 0.0, 0.0
    if p == 4:  # Jupiter
        a = 82.74 + 40.76 * T
    elif p == 5:  # Saturn
        a = 82.74 + 40.76 * T
        b = 29.86 + 1181.36 * T
        c = 14.13 + 590.68 * T
        d = 220.02 + 1262.87 * T

    ct = cor_time3(p, j, T, M, a, b, c, d)  # CorTime3 handles the two j cases (0 or 1)
    R = JDE0 + ct

    return R


def find_p_pheno(begin_jd: float, end_jd: float):
    """
    VBA Sub FindPPheno: Finds and sorts major planetary phenomena and moon phases within a given JD range.
    (VBA passes E and S by global/module reference; Python uses global lists)
    """
    global E, S, TIME_ZONE  # Use global lists/constants

    if end_jd <= begin_jd:
        return

    PN = "수성,금성,화성,목성,토성,천왕성,해왕성"
    PNA = PN.split(",")

    # Determine array size (l) based on duration, max 50 years (approx 18262 days)
    # The VBA calculation Int((EndJD - BeginJD) / 365.25) * 600 determines the size
    duration_years = (end_jd - begin_jd) / 365.25
    l = int(duration_years * 600)

    if l < 600:
        l = 600
    if l > 30000:
        # In a real environment, you might raise an error or handle it differently
        print("Error: The selected period is too long (over ~50 years). Truncating size.")
        l = 30000
        # return # Use return instead of MsgBox if running non-interactively

    l += 50

    # Initialize arrays
    E = [9999999999.0] * (l + 1)
    S = ["x"] * (l + 1)

    N = 0

    # --- 1. Planetary Phenomena Loop (Iterative Search) ---
    D = begin_jd - 90.0
    while D <= end_jd + 90.0:
        for i in range(1, 8):  # Planet ID: 1 (Mercury) to 7 (Neptune)
            for j in range(2):  # Phenomenon Type: 0 or 1
                PN = PNA[i - 1]

                # A. Conjunction/Opposition (합/충)
                X = find_planet(D, i, j)  # Note: TimeZone adjustment handled in VBA logic if uncommented

                if j == 0:
                    PSTR = f"{PN} 내합" if i < 3 else f"{PN} 충"
                else:  # j == 1
                    PSTR = f"{PN} 외합" if i < 3 else f"{PN} 합"

                if begin_jd <= X <= end_jd:
                    if N < len(E):
                        E[N] = X
                        S[N] = PSTR
                        N += 1

                # B. Stationary Points (유) - For inner/outer planets up to Saturn (P < 6)
                if i < 6:
                    y = station_planet(D, i, j)
                    PSTR = f"{PN} 유"
                    if begin_jd <= y <= end_jd:
                        if N < len(E):
                            E[N] = y
                            S[N] = PSTR
                            N += 1

                # C. Greatest Elongation (최대이각) - For inner planets (P < 3)
                if i < 3:
                    Z = elong_planet(D, i, j)
                    if j == 0:
                        PSTR = f"{PN} 동방최대이각"
                    else:  # j == 1
                        PSTR = f"{PN} 서방최대이각"

                    if begin_jd <= Z <= end_jd:
                        if N < len(E):
                            E[N] = Z
                            S[N] = PSTR
                            N += 1

        D += 30.0  # Move to the next 30-day interval

    # --- 2. Moon Phase Loop (Iterative Search) ---
    D = begin_jd - 20.0
    while D <= end_jd + 50.0:
        for i in range(4):  # 0=New, 1=First Q, 2=Full, 3=Last Q
            # GetMoon is assumed to return JD relative to TimeZone,
            # so the TimeZone subtraction might be used to convert back to TT/UT,
            # depending on the implementation of GetMoon.
            X = round(get_moon(D, i * 90.0, TIME_ZONE), 4) - TIME_ZONE / 24.0

            if i == 0:
                PSTR = "그믐"  # New Moon (삭)
            elif i == 1:
                PSTR = "상현"  # First Quarter
            elif i == 2:
                PSTR = "보름"  # Full Moon (망)
            elif i == 3:
                PSTR = "하현"  # Last Quarter

            if begin_jd <= X <= end_jd:
                if N < len(E):
                    E[N] = X
                    S[N] = PSTR
                    N += 1

        D += 27.0  # Approx. synodic period (29.5 days), using 27 as an arbitrary step

    # --- 3. Sorting (Bubble Sort Implementation) ---
    # The VBA code uses a Bubble Sort-like logic (Selection Sort variant) to sort by E(M)
    for M in range(N):
        EEE = E[M]
        MM = M
        for O in range(M + 1, N):  # Only iterate up to N (the number of found events)
            if E[O] < EEE:
                EEE = E[O]
                MM = O

        # Swap E[M] and E[MM], S[M] and S[MM]
        E[M], E[MM] = E[MM], E[M]
        S[M], S[MM] = S[MM], S[M]

    # --- 4. Remove Duplicates (Exact JD match) ---
    # Note: The VBA code iterates up to l-1 (the full initial array size) which is error-prone.
    # We will iterate up to N-2 to safely compare M with M+1
    for M in range(N - 1):
        if E[M] == E[M + 1]:
            S[M] = "x"

    # --- 5. Condense Array and Final Resize ---
    # N is reset to 0 for condensing
    N_condensed = 0
    for M in range(N):  # Iterate over the actual found events
        if S[M] != "x":
            S[N_condensed] = S[M]
            E[N_condensed] = E[M]
            N_condensed += 1

    if N_condensed > 0:
        E = E[:N_condensed]
        S = S[:N_condensed]
    else:
        E = []
        S = []

# Example of how to use the implemented functions (requires filling placeholders)
# find_p_pheno(2454466.0, 2454832.0) # Example: Jan 1, 2008 to Dec 31, 2008
# print(E)
# print(S)
