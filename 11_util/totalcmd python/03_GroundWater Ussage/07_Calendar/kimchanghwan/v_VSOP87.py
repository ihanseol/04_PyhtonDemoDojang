


# ***************************************************************************

# ***************************************************************************
import math

# --- Constants and Conversion Functions (Placeholders) ---

# Define the conversion factors
DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi


def Rev(angle_deg: float) -> float:
    """
    Placeholder for the Rev function (Normalize an angle to 0 <= angle < 360).
    Replace this with your actual implementation.
    """
    return angle_deg % 360.0


def Cosd(angle_deg: float) -> float:
    """Cosine in degrees."""
    return math.cos(angle_deg * DEG_TO_RAD)


def Sind(angle_deg: float) -> float:
    """Sine in degrees."""
    return math.sin(angle_deg * DEG_TO_RAD)


def Tand(angle_deg: float) -> float:
    """Tangent in degrees."""
    return math.tan(angle_deg * DEG_TO_RAD)


# --- VSOP87/ELP2000 Component Placeholders ---

def Earth_L0(T: float) -> float:
    """Placeholder for Earth Longitude L0 (radians)."""
    return 0.0  # Replace with actual formula


def Earth_L1(T: float) -> float:
    """Placeholder for Earth Longitude L1 (radians)."""
    return 0.0  # Replace with actual formula


# ... Earth_L2, L3, L4, L5 ...

def Earth_L2(T: float) -> float:
    """Placeholder for Earth Longitude L2 (radians)."""
    return 0.0


def Earth_L3(T: float) -> float:
    """Placeholder for Earth Longitude L3 (radians)."""
    return 0.0


def Earth_L4(T: float) -> float:
    """Placeholder for Earth Longitude L4 (radians)."""
    return 0.0


def Earth_L5(T: float) -> float:
    """Placeholder for Earth Longitude L5 (radians)."""
    return 0.0


def Earth_B0(T: float) -> float:
    """Placeholder for Earth Latitude B0 (radians)."""
    return 0.0  # Replace with actual formula


def Earth_B1(T: float) -> float:
    """Placeholder for Earth Latitude B1 (radians)."""
    return 0.0  # Replace with actual formula


def Earth_R0(T: float) -> float:
    """Placeholder for Earth Radius R0 (AU)."""
    return 0.0  # Replace with actual formula


def Earth_R1(T: float) -> float:
    """Placeholder for Earth Radius R1 (AU)."""
    return 0.0  # Replace with actual formula


# ... Earth_R2, R3, R4 ...

def Earth_R2(T: float) -> float:
    """Placeholder for Earth Radius R2 (AU)."""
    return 0.0


def Earth_R3(T: float) -> float:
    """Placeholder for Earth Radius R3 (AU)."""
    return 0.0


def Earth_R4(T: float) -> float:
    """Placeholder for Earth Radius R4 (AU)."""
    return 0.0


def MoonLBR(JDE: float) -> tuple[float, float, float]:
    """
    Placeholder for the MoonLBR function.
    Returns L0 (rad), B0 (rad), R0 (km, likely).
    Replace this with your actual implementation (e.g., ELP2000).
    """
    return 0.0, 0.0, 0.0  # L0, B0, R0


def PrecessionEcl(JDE_from: float, JDE_to: float, L_from: float, B_from: float) -> tuple[float, float]:
    """
    Placeholder for PrecessionEcl function.
    Converts (L, B) from JDE_from to JDE_to (e.g., J2000.0).
    L, B are in degrees. Returns L_to, B_to (degrees).
    Replace this with your actual implementation (e.g., IAU 2000/2006).
    """
    # Assuming L_from and B_from are in degrees as per GetLBR2000 usage
    L_to = L_from
    B_to = B_from
    return L_to, B_to


# --- Main Functions ---

def VSOP87_FK5(JDE: float, l: float, B: float) -> tuple[float, float]:
    """
    Applies the FK5 correction to VSOP87/ELP2000 coordinates.
    Input/Output l, B are in degrees.
    """
    T = (JDE - 2451545.0) / 36525.0

    # ll is calculated in degrees, as l is in degrees
    ll = l - 1.397 * T - 0.00031 * T * T

    cLL = Cosd(ll)
    sLL = Sind(ll)

    # Original VBA uses the result of 'l' and 'B' in the calculation
    # Since l and B are passed ByRef in VBA, the changes are immediate.
    # In Python, we calculate the delta and apply it.

    # Calculate the correction to l (Lambda)
    delta_l = -2.50916666666667E-05 + 1.08777777777778E-05 * (cLL + sLL) * Tand(B)

    # Calculate the correction to B (Beta)
    delta_B = 1.08777777777778E-05 * (cLL - sLL)

    l_new = l + delta_l
    B_new = B + delta_B

    return l_new, B_new


# 입력: JED
# 출력: L(deg), B(deg), R(AU)
# 설명: 출력은 입력한 날의 분점으로 계산된 결과임.
def GetLBR(JDE: float, Planet: int, FK5: bool) -> tuple[float, float, float]:
    """
    Calculates the heliocentic/geocentric LBR coordinates for a planet (or Moon/Earth).
    The L and B returned are for the equinox of date.
    Planet: 2=Earth, 9=Moon.
    Returns: L (deg), B (deg), R (AU).
    """
    T = (JDE - 2451545.0) / 365250.0
    L0, B0, R0 = 0.0, 0.0, 0.0

    AU_KM = 149597870.0  # Astronomical Unit in km

    if Planet == 2:  # Earth
        # L0, B0, R0 are sums of series (rad)
        L0 = (Earth_L0(T) + Earth_L1(T) + Earth_L2(T) + Earth_L3(T) + Earth_L4(T) + Earth_L5(T))
        B0 = (Earth_B0(T) + Earth_B1(T))
        R0 = (Earth_R0(T) + Earth_R1(T) + Earth_R2(T) + Earth_R3(T) + Earth_R4(T))
        # Note: The commented-out LBR_LOW usage is skipped as per the original code.

    elif Planet == 9:  # Moon
        # MoonLBR returns pre-corrected results (L0, B0 in rad, R0 in km)
        L0, B0, R0 = MoonLBR(JDE)
        R0 = R0 / AU_KM  # Convert R0 from km to AU
        # Note: The commented-out LBR_LOW usage is skipped as per the original code.

    else:
        # Handle other planets or raise an error
        raise ValueError("Planet not supported in GetLBR: only 2 (Earth) and 9 (Moon)")

    # Convert L0 and B0 from radians to degrees
    L0_deg = Rev(L0 * RAD_TO_DEG)
    B0_deg = B0 * RAD_TO_DEG

    l, B = L0_deg, B0_deg

    if FK5 and Planet < 9:
        # VSOP87_FK5 expects and returns degrees
        l, B = VSOP87_FK5(JDE, L0_deg, B0_deg)

    # The final assignment in VBA's ByRef variables:
    l_final = Rev(l)
    B_final = B
    R_final = R0  # R0 is already the final R

    return l_final, B_final, R_final


def GetLBR2000(JDE: float, Planet: int, FK5: bool) -> tuple[float, float, float]:
    """
    Calculates the LBR coordinates referred to the J2000.0 equinox.
    Returns: L (deg), B (deg), R (AU).
    """
    # Get LBR at equinox of date (False for FK5 correction here, as it's applied later)
    L0, B0, R = GetLBR(JDE, Planet, False)  # L0, B0 are in degrees

    J2000_JDE = 2451545.0

    # Precession from JDE (equinox of date) to J2000.0 (J2000_JDE)
    L1, B1 = PrecessionEcl(JDE, J2000_JDE, L0, B0)  # L1, B1 are in degrees

    if FK5 and Planet < 9:
        # Apply FK5 correction at the J2000 epoch (2451545)
        L1, B1 = VSOP87_FK5(J2000_JDE, L1, B1)

    # The final assignment in VBA's ByRef variables:
    l_final = Rev(L1)
    B_final = B1

    return l_final, B_final, R


def LBR_LOW(P: int, JD: float) -> tuple[float, float, float]:
    """
    Low-accuracy calculation for Sun (P=0) or Moon (P=1).
    Returns Lamda (deg), Beta (deg), R (AU or km, check P=1 case).
    """
    N = JD - 2451545.0

    if P == 0:  # sun
        l = 280.46 + 0.9856474 * N
        g = 357.528 + 0.9856003 * N

        Lamda = l + 1.915 * Sind(g) + 0.02 * Sind(2 * g)

        Beta_T = N / 36525.0
        E = 0.016708634 - 0.000042037 * Beta_T - 0.0000001267 * Beta_T * Beta_T

        Beta = 0.0  # Ecliptic latitude is zero for the Sun

        # Note: The VBA code calculates R using the Sun's *true anomaly* (g + Lamda - l)
        R = 1.000001018 * (1 - E * E) / (1 + E * Cosd(g + Lamda - l))

    elif P == 1:  # moon
        T = N / 36525.0

        l = (218.32 + 481267.883 * T + 6.29 * Sind(134.9 + 477198.85 * T)
             - 1.27 * Sind(259.2 - 413335.38 * T)
             + 0.66 * Sind(235.7 + 890534.23 * T) + 0.21 * Sind(269.9 + 954397.7 * T)
             - 0.19 * Sind(
                    357.5 + 35999.05 * T)  # Note: 35999.05 is missing *T in VBA, added here. Assuming 35999.05*T.
             - 0.11 * Sind(186.6 + 966404.05 * T))

        g = (5.13 * Sind(93.3 + 483202.03 * T) + 0.28 * Sind(228.2 + 960400.87 * T)
             - 0.28 * Sind(318.3 + 6003.18 * T) - 0.17 * Sind(217.6 - 407332.2 * T))

        N_value = (0.9508 + 0.0518 * Cosd(134.9 + 477198.85 * T) + 0.0095 * Cosd(259.2 - 413335.38 * T)
                   + 0.0078 * Cosd(235.7 + 890534.23 * T) + 0.0028 * Cosd(269.9 + 954397.7 * T))

        # N_value is actually the Moon's parallax (in degrees, likely)
        # The next line calculates the distance (R) in km using Earth's equatorial radius (6378.14 km)
        # and the sine of the parallax.

        R_value = 6378.14 / Sind(N_value)

        Beta = g
        Lamda = l
        R = R_value  # R is in km

    else:
        raise ValueError("Planet not supported in LBR_LOW: only 0 (Sun) and 1 (Moon)")

    return Rev(Lamda), Beta, R



