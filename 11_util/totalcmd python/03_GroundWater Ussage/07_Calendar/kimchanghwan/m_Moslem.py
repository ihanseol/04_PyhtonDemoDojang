import math

# --- Constants and Mocks (to replace external functions) ---

# Const AH1 As Double = 1948440 '이슬람력의 시작일(헤지라 날짜)
AH1: float = 1948440.0


def GetJD0(jd: float) -> float:
    """
    MOCK: Corresponds to VB's GetJD0.
    Returns the Julian Day for the preceding noon (JD of 00:00 UT) for calendar calculation purposes.
    """
    return math.floor(jd)


def InvJD(JD: float) -> tuple[float, float, float, float, float]:
    """
    MOCK: Corresponds to VB's InvJD.
    Converts Julian Day (JD) to Gregorian/Julian date components (Y, M, D, A, B).
    Returns (gY, gM, gD, a, B).

    Using a simplified approximation for demonstration purposes.
    The actual implementation requires a full JD-to-Gregorian/Julian algorithm.
    """
    # Note: This mock is simplified. A full implementation is required for accuracy.
    if JD < 2299161:  # Julian calendar era
        # Approximating a date near the Hijri start (AH1 = 1948440)
        gY, gM, gD = 622.0, 7.0, 16.5
    else:  # Gregorian calendar era (starting JD 2299161.0)
        # Approximating a date near JD 2451545.0 (2000-01-01)
        gY, gM, gD = 2000.0, 1.0, 1.0

    return gY, gM, gD, 0.0, 0.0  # a and B are unused intermediate values


# --- Calendar Functions ---

def MonthName(mon: int) -> str:
    """Returns the name of the Islamic month (1-based index)."""
    # Dim MonthNm(11) As String '달의 이름
    MonthNm = [
        "Muharram", "Safar", "Rabi'al-Awwal", "Rabi'ath-Thani",
        "Jumada l-Ula", "Jumada t-Tania", "Rajab", "Sha'ban",
        "Ramadan", "Shawwal", "Dhu l-Qa'da", "Dhu l-Hijja"
    ]

    # VB uses 1-based indexing (mon - 1)
    if 1 <= mon <= 12:
        return MonthNm[mon - 1]
    else:
        return ""


def M2JD(mY: int, MM: int, MD: int) -> float:
    """Converts Hijri date (mY, MM, MD) to Julian Day (JD)."""

    # If mY < 0 Or MM < 0 Or MD < 0 Then M2JD = 0: Exit Function
    if mY < 0 or MM < 0 or MD < 0:
        return 0.0

    # 변환 계산 시작
    N = MD + math.floor(29.5001 * (MM - 1) + 0.99)
    Q = math.floor(mY / 30)
    R = mY % 30
    a = math.floor((11 * R + 3) / 30)
    w = 404 * Q + 354 * R + 208 + a
    Q1 = math.floor(w / 1461)
    Q2 = w % 1461
    g = 621 + 4 * math.floor(7 * Q + Q1)
    k = math.floor(Q2 / 365.2422)
    E = math.floor(365.2422 * k)
    j = Q2 - E + N - 1
    X = g + k

    # Leap year adjustment logic
    if (j > 366) and (X % 4 == 0):
        j = j - 366
        X = X + 1
    if (j > 365) and (X % 4 > 0):
        j = j - 365
        X = X + 1

    JD = math.floor(365.25 * (X - 1)) + 1721423 + j
    return JD


def JD2M2(JD: float) -> str:
    """
    Converts Julian Day (JD) to Hijri date string (문자 형식 출력),
    with special strings for Ramadan start/end.
    """
    y, M, D = 0, 0, 0

    # jd0 = GetJD0(JD) + 0.5
    jd0 = GetJD0(JD) + 0.5

    # Call JD2M(jd0, y, M, D)
    # Since Python cannot pass simple integers by reference (like VB 'Call'),
    # we use the returning values from JD2M.
    y, M, D = JD2M(jd0)

    R = ""
    if y == 0:
        R = ""
    else:
        R = f"{M}월 {D}일"
        if M == 9 and D == 1:
            R = "라마단 시작"
        if M == 9 and D == 30:
            R = "라마단 종료"

    return R


def JD2M(JD: float) -> tuple[int, int, int]:
    """
    Converts Julian Day (JD) to Hijri date components (mY, MM, MD).
    Returns (mY, MM, MD).
    """
    mY, MM, MD = 0, 0, 0

    JD12 = 0.5 + GetJD0(JD)

    # 입력받은 날짜가 헤지라 이전이면 계산 안함
    # If JD < AH1 Then mY = 0: MM = 0: MD = 0: Exit Sub
    if JD < AH1:
        return 0, 0, 0

    # Call InvJD(JD12, gY, gM, gD, a, B)
    gY, gM, gD, a_unused, B_unused = InvJD(JD12)

    X1: float = gY
    M1: float = gM
    D1: float = gD

    # 그레고리력이면 율리우스력으로 바꾸기 (Gregorian to Proleptic Julian Conversion)
    if JD12 >= 2299161:
        # Note: gY, gM, gD here are the Gregorian components from InvJD
        if gM < 3:
            gY = gY - 1
            gM = gM + 12

        alp = math.floor(gY / 100)
        Bet = 2 - alp + math.floor(alp / 4)

        # B is the Julian Day Number, relative to the Hijri algorithm's epoch
        B = math.floor(365.25 * gY) + math.floor(30.6001 * (gM + 1)) + gD + 1722519 + Bet

        c = math.floor((B - 122.1) / 365.25)
        D = math.floor(365.25 * c)
        E = math.floor((B - D) / 30.6001)
        D1 = B - D - math.floor(30.6001 * E)

        M1 = 0.0
        if E < 14:
            M1 = E - 1
        if E > 13:
            M1 = E - 13

        X1 = 0.0
        if M1 > 2:
            X1 = c - 4716
        if M1 < 3:
            X1 = c - 4715
    # Else: X1 = gY: M1 = gM: D1 = gD (Already initialized)

    # 이슬람력 계산 (Islamic Calendar Calculation)
    if X1 % 4 == 0:
        w = 1.0
    else:
        w = 2.0

    N = math.floor((275 * M1) / 9) - w * math.floor((M1 + 9) / 12) + D1 - 30
    a = X1 - 623
    B = math.floor(a / 4)
    c_mod = a % 4

    C1 = 365.2501 * c_mod
    C2 = math.floor(C1)
    if C1 - C2 > 0.5:
        C2 = C2 + 1

    D = 1461 * B + 170 + C2
    Q = math.floor(D / 10631)
    R = D % 10631
    j = math.floor(R / 354)
    k = R % 354
    O = math.floor((11 * j + 14) / 30)
    h = 30 * Q + j + 1

    # JJ는 이슬람력에서 당년의 날짜 수임 (JJ is the day number within the current Hijri year)
    JJ = k - O + N - 1

    # Check for leap year adjustment in the calculated Hijri year
    if JJ > 354:
        cl = h % 30
        dl = (11 * cl + 3) % 30

        if dl < 19:  # Simple year (354 days)
            JJ = JJ - 354
            h = h + 1
        elif dl > 18:  # Leap year (355 days)
            JJ = JJ - 355
            h = h + 1

        if JJ == 0:  # If subtraction results in 0, it means it's the last day of the previous year
            JJ = 355  # Set to last day of previous (leap) year
            h = h - 1

    S = math.floor((JJ - 1) / 29.5)

    if JJ == 355:
        mY = int(h)
        MM = 12
        MD = 30
    else:
        mY = int(h)
        MM = int(1 + S)
        MD = int(JJ - 29.5 * S)

    return mY, MM, MD


# --- Example Usage ---
if __name__ == '__main__':
    # Test JD: 2451545.0 (2000-01-01 12:00:00 UT) - This is Gregorian era
    TEST_JD_GREGORIAN = 2451545.0
    # Expected approximate Hijri date for 2000-01-01 is 1420 Shawwal (Month 10)

    # Test JD: 1948440.5 (JD of first day of Hijri era) - This is Julian era
    TEST_JD_HIJRI_START = 1948440.5
    # Expected: AH 1, Muharram 1

    print("--- Islamic Calendar Translation Test ---")

    # 1. Test AH 1, Muharram 1 -> JD (M2JD)
    jd_check = M2JD(mY=1, MM=1, MD=1)
    print(f"Hijri 1/1/1 -> JD: {jd_check:.1f} (Target: {AH1 + 0.5})")

    # 2. Test JD to components (JD2M) - Near Hijri Start
    y, m, d = JD2M(TEST_JD_HIJRI_START)
    print(f"\nJD {TEST_JD_HIJRI_START} -> Hijri: {y}년 {m}월 {d}일 (Expected: 1/1/1 or close)")

    # 3. Test JD to components (JD2M) - Gregorian Era
    y_greg, m_greg, d_greg = JD2M(TEST_JD_GREGORIAN)
    print(f"JD {TEST_JD_GREGORIAN} -> Hijri: {y_greg}년 {m_greg}월 {d_greg}일")
    print(f"Month Name: {MonthName(m_greg)}")

    # 4. Test JD to formatted string (JD2M2) - Ramadan check
    # Let's mock Ramadan start (Month 9, Day 1)
    mock_ramadan_jd = 2451545.0

    # To properly test Ramadan, we need to know the JD of a Ramadan date.
    # Since JD2M is complex, we'll manually set the output for a mock JD to test JD2M2 logic.
    # Note: JD2M2 will call JD2M, which is using the mock InvJD.
    print(f"\nJD {mock_ramadan_jd} -> Formatted Output (JD2M2): {JD2M2(mock_ramadan_jd)}")

    # For testing the month names
    print(f"Month 9 is: {MonthName(9)}")
    print(f"Month 12 is: {MonthName(12)}")
