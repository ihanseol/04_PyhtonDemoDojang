import math

# Define constants and utility functions used in astronomical calculations

# Value of Pi for common use
PI = math.pi


# Converts degrees to radians (DegtoRad equivalent)
def deg_to_rad(degrees: float) -> float:
    return degrees * (PI / 180.0)


# Returns the angle restricted to the range [0, 360) (Rev equivalent)
def rev(angle: float) -> float:
    return angle % 360.0


# Returns the sine of an angle in degrees (Sind equivalent)
def sind(degrees: float) -> float:
    return math.sin(deg_to_rad(degrees))


# --- Input Data (Amplitudes and Arguments) ---
# This function replicates the data loading from InputData VBA function.
def input_data():
    """
    Loads the main coefficients for Moon's Longitude, Radius, and Latitude.
    Based on the provided VBA 'InputData' function.

    Returns: Tuple of 12 lists/tuples representing the coefficients.
    """
    # Note: VBA uses 1-based indexing for the arrays, Python uses 0-based.
    # The arrays below are 0-indexed, so we effectively skip the first position
    # and use indices 0 to 59 for the 60 terms.

    # D, M, M1, f: Coefficients for Lunar Longitude (L) and Radius (R) arguments
    # cl, cr: Coefficients (in 10^-7 degrees for L, 10^-3 km for R)
    D = [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1, 1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2,
         4, 0, 3, 2, 4, 0, 2, 2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2, 2]
    M = [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2,
         0, 0, -1, 0, 0, 1, -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0, 0]
    M1 = [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 2, -2, -1, 3, -2, -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0,
          2, 0, -1, 1, 0, -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, -2, 1, -2, -3, 2, 1, -1, 3, -1]
    f = [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2,
         2, 0, 2, 0, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, -2]
    cl = [6288774, 1274027, 658314, 213618, -185116, -114332, 58793, 57066, 53322, 45758, -40923, -34720, -30383, 15327,
          -12528, 10980, 10675, 10034, 8548, -7888, -6766, -5163, 4987, 4036, 3994, 3861, 3665, -2689, -2602, 2390,
          -2348, 2236, -2120, -2069, 2048, -1773, -1595, 1215, -1110, -892, -810, 759, -713, -700, 691, 596, 549, 537,
          520, -487, -399, -381, 351, -340, 330, 327, -323, 299, 294, 0]
    cr = [-20905355, -3699111, -2955968, -569925, 48888, -3149, 246158, -152138, -170733, -204586, -129620, 108743,
          104755, 10321, 0, 79661, -34782, -23210, -21636, 24208, 30824, -8379, -16675, -12831, -10445, -11650, 14403,
          -7003, 0, 10056, 6322, -9884, 5751, 0, -4950, 4130, 0, -3958, 0, 3258, 2616, -1897, -2117, 2354, 0, 0, -1423,
          -1117, -1571, -1739, 0, -4421, 0, 0, 0, 0, 1165, 0, 0, 8752]

    # D1, m1a, m11, F1: Coefficients for Lunar Latitude (B) arguments
    # cb: Coefficients (in 10^-7 degrees)
    D1 = [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 4, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4, 4, 0, 4, 2, 2, 2, 2, 0,
          2, 2, 2, 2, 4, 2, 2, 0, 2, 1, 1, 0, 2, 1, 2, 0, 4, 4, 1, 4, 1, 4, 2]
    m1a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, -1, -1, -1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1,
           0, 0, 0, 0, 1, 1, 0, -1, -2, 0, 1, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0, 0, -1, -2]
    m11 = [0, 1, 1, 0, -1, -1, 0, 2, 1, 2, 0, -2, 1, 0, -1, 0, -1, -1, -1, 0, 0, -1, 0, 1, 1, 0, 0, 3, 0, -1, 1, -2, 0,
           2, 1, -2, 3, 2, -3, -1, 0, 0, 1, 0, 1, 1, 0, 0, -2, -1, 1, -2, 2, -2, -1, 1, 1, -1, 0, 0]
    F1 = [1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 3, 1, 1, 1, -1, -1, -1, 1, -1, 1, -3,
          1, -3, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 3, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1]
    cb = [5128122, 280602, 277693, 173237, 55413, 46271, 32573, 17198, 9266, 8822, 8216, 4324, 4200, -3359, 2463, 2211,
          2065, -1870, 1828, -1794, -1749, -1565, -1491, -1475, -1410, -1344, -1335, 1107, 1021, 833, 777, 671, 607,
          596, 491, -451, 439, 422, 421, -366, -351, 331, 315, 302, -283, -229, 223, 223, -220, -220, -185, 181, -177,
          176, 166, -164, 132, -119, 115, 107]

    return D, M, M1, f, D1, m1a, m11, F1, cl, cr, cb


# --- Main Moon Position Function ---

def moon_lbr(jde: float) -> tuple[float, float, float]:
    """
    Calculates the geocentric longitude (l), latitude (B), and distance (R) of the Moon.
    This function implements a simplified series based on the ELP-2000/82 theory.

    Args:
        jde: Julian Ephemeris Day.

    Returns:
        A tuple (l, B, R) where:
        l: Ecliptic longitude in radians.
        B: Ecliptic latitude in radians.
        R: Geocentric distance in kilometers (km).
    """

    # 1. Load coefficients
    D_list, M_list, M1_list, f_list, D1_list, m1a_list, m11_list, F1_list, cl_list, cr_list, cb_list = input_data()

    # 2. Calculate time variable T and its powers
    T = (jde - 2451545.0) / 36525.0
    T2 = T * T
    T3 = T2 * T
    T4 = T2 * T2

    # 3. Calculate mean arguments (in degrees)
    L1 = 218.3164477 + 481267.88123421 * T - 0.0015786 * T2 + T3 / 538841.0 - T4 / 65194000.0
    D = 297.8501921 + 445267.1114034 * T - 0.0018819 * T2 + T3 / 545868.0 - T4 / 113065000.0
    M = 357.5291092 + 35999.0502909 * T - 0.0001536 * T2 + T3 / 24490000.0
    M1 = 134.9633964 + 477198.8675055 * T + 0.0087414 * T2 + T3 / 69699.0 - T4 / 14712000.0
    f = 93.272095 + 483202.0175233 * T - 0.0036539 * T2 - T3 / 3526000.0 + T4 / 863310000.0

    # Other short period arguments
    A1 = 119.75 + 131.849 * T
    A2 = 53.09 + 479264.29 * T
    A3 = 313.45 + 481266.484 * T

    # Earth's eccentricity related terms
    E = 1.0 - 0.002516 * T - 0.0000074 * T2
    E2 = E * E

    # Normalize angles to [0, 360) degrees
    L1 = rev(L1)
    D = rev(D)
    M = rev(M)
    M1 = rev(M1)
    f = rev(f)
    A1 = rev(A1)
    A2 = rev(A2)
    A3 = rev(A3)

    # 4. Sum the series (60 terms)
    SL = 0.0  # Sum for Longitude
    SR = 0.0  # Sum for Radius
    SB = 0.0  # Sum for Latitude

    for i in range(60):  # Python uses 0-based indexing for 60 terms (0 to 59)
        # --- Longitude and Radius Series Calculation ---

        # k for Longitude and Radius (eccentricity factor)
        k_lr = 1.0
        if abs(M_list[i]) == 1:
            k_lr = E
        elif abs(M_list[i]) == 2:
            k_lr = E2

        # Longitude/Radius Argument (in radians)
        a_lr = deg_to_rad(
            D_list[i] * D + M_list[i] * M + M1_list[i] * M1 + f_list[i] * f
        )

        # Summation for Longitude (using Sine)
        SL += cl_list[i] * math.sin(a_lr) * k_lr

        # Summation for Radius (using Cosine)
        SR += cr_list[i] * math.cos(a_lr) * k_lr

        # --- Latitude Series Calculation ---

        # k for Latitude (eccentricity factor)
        k_b = 1.0
        if abs(m1a_list[i]) == 1:
            k_b = E
        elif abs(m1a_list[i]) == 2:
            k_b = E2

        # Latitude Argument (in degrees) -> Normalize -> Convert to radians
        # The VBA code for 'a' calculation in the latitude part is slightly inconsistent
        # (it uses rev() inside the loop), but we follow the logic:
        a_b_deg = D1_list[i] * D + m1a_list[i] * M + m11_list[i] * M1 + F1_list[i] * f
        a_b = deg_to_rad(rev(a_b_deg))

        # Summation for Latitude (using Sine)
        SB += cb_list[i] * math.sin(a_b) * k_b

    # 5. Add "Correction" Terms (additional sine/cosine terms)
    # The constants (e.g., 3958, 1962) are implicitly scaled by 10^-7 in the VBA code
    # because the main sums (SL, SB) are in 10^-7 degrees.

    # Longitude Corrections (using sind which takes degrees)
    SL += 3958 * sind(A1)
    SL += 1962 * sind(L1 - f)
    SL += 318 * sind(A2)

    # Latitude Corrections (using sind which takes degrees)
    SB -= 2235 * sind(L1)
    SB += 382 * sind(A3)
    SB += 175 * sind(A1 - f)
    SB += 175 * sind(A1 + f)
    SB += 127 * sind(L1 - M1)
    SB -= 115 * sind(L1 + M1)

    # SR is already summed up, no explicit additional terms in this section
    # SR = SR  # (Line removed, as it's redundant)

    # 6. Final Result Calculations

    # Longitude (l): Final Angle in Radians
    # L1 (degrees) + SL (10^-7 degrees) / 1,000,000
    l_deg = rev(L1 + SL / 1000000.0)
    l = deg_to_rad(l_deg)

    # Latitude (B): Final Angle in Radians
    # SB (10^-7 degrees) / 1,000,000
    B_deg = SB / 1000000.0
    B = deg_to_rad(B_deg)

    # Radius (R): Final Distance in km
    # R0 (385000.56 km) + SR (10^-3 km) / 1,000
    R = 385000.56 + SR / 1000.0

    return l, B, R
